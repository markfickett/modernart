import logging
import random

import analysis
import modernart_pb2
import printing


MIN_PLAYERS = 3
MAX_PLAYERS = 5

_NUM_ROUNDS = 4
_INITIAL_MONEY = 100
_NUM_TO_END_ROUND = 5
_ARTIST_VALUES = [30, 20, 10]


class GameMaster(object):
  """Tracks game state and controls game flow according to the rules.

  The GM is also responsible communicating with the Players (telling them as
  public events take place during the game, asking them for cards and bids), as
  well as keeping private, authoritative records of what the players have (cards
  and money) and making sure the Players don't cheat.

  The GM logs informational messages to produce a record of the game. A subset
  of these are also communicated to the Players.

  Aside from the Player objects, most of the GM's state is stored in a
  modernart_pb2.Board proto and its various submessages. This is to facilitate
  sharing board state easily with Players, for their decision-making.
  """

  def __init__(self, player_objs):
    """Sets up: picks which player will go first."""
    youngest_index = player_objs.index(
        min(player_objs, key=lambda p: p.size))
    self._players = player_objs[youngest_index:] + player_objs[:youngest_index]
    self._players_by_name = dict((p.name, p) for p in self._players)
    logging.info(
        'Player order is: %s',
        ', '.join(p.name for p in self._players))
    self._next_seller_index = 0
    self._AUCTION_RUNNERS = {
      modernart_pb2.AuctionType.SEALED: self._RunAuctionSealed,
      modernart_pb2.AuctionType.FIXED: self._RunAuctionFixed,
      modernart_pb2.AuctionType.ONCE_AROUND: self._RunAuctionOnceAround,
      modernart_pb2.AuctionType.OPEN: self._RunAuctionOpen,
    }

  def Play(self):
    """Runs a game, returning the winning player."""
    self._board = modernart_pb2.Board(
        deck=_MakeDeck())
    for player in self._players:
      self._board.player_holdings.add(
          name=player.name,
          money=_INITIAL_MONEY)
      player.AcceptMoney(_INITIAL_MONEY)

    for round_index in range(_NUM_ROUNDS):
      self._PlayRound(round_index)

    return self._PickWinner()

  def _PlayRound(self, round_index):
    """Runs one round of the game: deals cards, runs auctions, pays."""
    logging.info('Starting round number %d.', round_index + 1)
    new_card_count = _GetNewCardCount(round_index, len(self._players))
    for holding in self._board.player_holdings:
      new_cards = _TakeCards(self._board.deck, new_card_count)
      holding.hand.extend(new_cards)
      self._players_by_name[holding.name].AcceptCards(new_cards)
    while True:
      self._StartAuction()
      auction = self._board.auction
      if auction.ends_round:
        break
      if not auction.winner_name:
        self._AUCTION_RUNNERS[auction.cards[-1].auction_type](
            auction,
            self._players_by_name[auction.seller_names[-1]])
      self._CompleteAuction()
    self._RecordPlacings()
    self._AssignWinningsAndClearPurchases()

  def _StartAuction(self):
    """Gets the next card for auction from a Player.

    Queries the next seller Player for a painting/card (or two, if one is a
    double) for auction. If it's an open double, also gets the second card and
    seller.

    Updates the state of the auction submessage in the board, possibly ending
    the round or assigning a de facto winner.
    """
    logging.info('Starting a new auction.')
    self._board.ClearField('auction')

    # Get a card from the next seller and validate it.
    cards = []
    skipped = 0
    while not cards and skipped < len(self._players):
      seller = self._players[self._next_seller_index]
      self._next_seller_index = self._NextPlayerIndex(self._next_seller_index)
      cards = seller.GetCardsForAuction(self._board)
      logging.info(
          '%s puts %s up for auction.', seller.name, printing.Cards(cards))
      skipped += 1
    if not cards:
      raise _FoulPlayException(None, 'Nobody put cards up for auction.')
    if len(cards) > 2:
      raise _FoulPlayException(seller, 'provided > 2 cards for auction')
    seller_holdings = self._GetHoldings(seller)
    if not all(card in seller_holdings.hand for card in cards):
      raise _FoulPlayException(
          seller,
          'put up %s for auction without having them (hand was %s)'
          % (printing.Cards(cards), printing.Cards(seller_holdings.hand)))
    is_double = any(card.auction_type == modernart_pb2.AuctionType.DOUBLE
                    for card in cards)
    if len(cards) == 2 and not is_double:
      raise _FoulPlayException(
          seller, 'provided two cards for auction, but no double')

    # Do the bookkeeping to accept the card from the seller.
    self._board.auction.seller_names.append(seller.name)
    _MoveCards(cards, seller_holdings.hand, self._board.auction.cards)

    self._CheckAndMaybeSetAuctionEndsRound()
    if not self._board.auction.ends_round and is_double and len(cards) == 1:
      self._AddSecondSeller()

  def _NextPlayerIndex(self, i):
    return (i + 1) % len(self._players)

  def _CheckAndMaybeSetAuctionEndsRound(self):
    """If current purchases + cards for auction are enough, ends the round."""
    per_artist_counts = analysis.CountPurchasesPerArtist(
        self._board.player_holdings)
    for card in self._board.auction.cards:
      per_artist_counts[card.artist] += 1
    for artist, count in per_artist_counts.iteritems():
      if count >= _NUM_TO_END_ROUND:
        self._board.auction.ends_round = True
        logging.info(
            'Round ends with %d from %s.', count, printing.ArtistName(artist))
        return

    cards_left = False
    for holdings in self._board.player_holdings:
      cards_left |= len(holdings.hand) > 0
    if not cards_left:
      self._board.auction.ends_round = True
      logging.info('Round ends because everyone is out of cards.')

  def _GetHoldings(self, player):
    """Returns the record of what a Player has, as a PlayerHoldings proto."""
    for holding in self._board.player_holdings:
      if player.name == holding.name:
        return holding
    raise ValueError(
        'player %s (name %s) not in recorded holdings'
        % (player, player.name))

  def _AddSecondSeller(self):
    """In the case of an unclaimed double, finds the second seller."""
    while True:
      potential_seller = self._players[self._next_seller_index]
      self._next_seller_index = self._NextPlayerIndex(self._next_seller_index)
      if potential_seller.name == self._board.auction.seller_names[0]:
        logging.info(
            '%s gets the %s for free.',
            potential_seller.name,
            printing.Cards(self._board.auction.cards))
        self._board.auction.winner_name = potential_seller.name
        return

      cards = potential_seller.GetCardsForAuction(self._board)
      if not cards:
        logging.info(
            '%s passes on the %s.',
            potential_seller.name,
            printing.Cards(self._board.auction.cards))
        continue

      if len(cards) != 1:
        raise _FoulPlayException(
            potential_seller, 'provided > 1 card on a double')
      card = cards[0]
      logging.info(
          '%s adds a card: %s',
          potential_seller.name,
          printing.Cards([card]))
      if card.auction_type == modernart_pb2.AuctionType.DOUBLE:
        raise _FoulPlayException(
            potential_seller, 'played a double on a double')
      if card.artist != self._board.auction.cards[0].artist:
        raise _FoulPlayException(
            potential_seller,
            'played a %s on a %s (different artist)'
            % (printing.Cards([card]),
               printing.Cards([self._board.auction.cards[0]])))

      holdings = self._GetHoldings(potential_seller)
      _MoveCards([card], holdings.hand, self._board.auction.cards)
      self._board.auction.seller_names.append(potential_seller.name)
      self._CheckAndMaybeSetAuctionEndsRound()
      return

  def _GetIndependantBidsInOrder(self):
    # Go in order to resolve ties by play-order.
    max_bid = None
    winner = None
    for player in (
        self._players[self._next_seller_index:] +
        self._players[:self._next_seller_index]):
      bid = player.GetBidForAuction(self._board)
      if bid is None:
        logging.info('Simultaneously, %s passes.', player.name)
      else:
        logging.info('Simultaneously, %s bids %s.', player.name, bid)
        if bid > max_bid:
          max_bid = bid
          winner = player
    return winner, max_bid

  def _RunAuctionSealed(self, auction, seller):
    winner, max_bid = self._GetIndependantBidsInOrder()
    if not winner:
      logging.info('every passed, seller wins by default.')
      winner = seller
      max_bid = 0
    logging.info('%s wins with a bid of %d.', winner.name, max_bid)
    auction.winner_name = winner.name
    auction.winning_bid = max_bid

  def _RunAuctionFixed(self, auction, seller):
    fixed_price = seller.GetBidForAuction(self._board, as_seller=True)
    if fixed_price is None:
      raise _FoulPlayException(seller, 'did not set fixed price')
    auction.winning_bid = fixed_price
    logging.info('%s fixes the price at %d.', seller.name, fixed_price)
    next_buyer_index = self._next_seller_index
    while True:
      buyer = self._players[next_buyer_index]
      next_buyer_index = self._NextPlayerIndex(next_buyer_index)
      if buyer.name == seller.name:
        logging.info('%s has to buy the painting back.', buyer.name)
        break
      bid = buyer.GetBidForAuction(self._board)
      if bid is None:
        logging.info('%s passes.', buyer.name)
      elif bid < fixed_price:
        raise _FoulPlayException(
            buyer,
            'underbid the fixed price of %d with %d' % (fixed_price, bid))
      else:
        logging.info('%s buys it.', buyer.name)
        break
    auction.winner_name = buyer.name

  def _RunAuctionOnceAround(self, auction, seller):
    next_buyer_index = self._next_seller_index
    buyer = None
    auction.winning_bid = 0
    while buyer != seller:
      buyer = self._players[next_buyer_index]
      next_buyer_index = self._NextPlayerIndex(next_buyer_index)
      bid = buyer.GetBidForAuction(self._board)
      if bid is None:
        logging.info('%s passes.', buyer.name)
        continue
      if bid <= auction.winning_bid:
        raise _FoulPlayException(
            buyer,
            'tried to bid %d, not more than the previous bid of %d'
            % (bid, auction.winning_bid))
      logging.info('%s bids %s.', buyer.name, bid)
      auction.winning_bid = bid
      auction.winner_name = buyer.name
    if not auction.winner_name:
      logging.info('every passed, seller wins by default.')
      auction.winner_name = seller.name

  def _RunAuctionOpen(self, auction, seller):
    """Conducts an open auction.

    An open auction is simulated by having sealed auctions, taking the maximum
    of the sealed / pseudo-simultaneous bids each time, and repeating until
    the information given to the Players does not change (that is, until there
    have been two successive rounds where no Player bid more).

    Updates the current Auction's winner_name and winning_bid.

    Args:
      seller: For convenience, the player who put the card up for auction. (For
          doubles with two sellers, this is the Player that contributed the
          second card.)
    """
    auction.winner_name = seller.name
    auction.winning_bid = 0
    all_passed_count = 0
    while all_passed_count < 2:  # Wait until no information changes.
      bidder, bid = self._GetIndependantBidsInOrder()
      if bid is None:
        all_passed_count += 1
        continue
      if bid <= auction.winning_bid:
        raise _FoulPlayException(
            bidder,
            'bid %d which is not more than %d'
            % (bid, auction.winning_bid))
      logging.info('%s increases the bid to %d.' % (bidder.name, bid))
      all_passed_count = 0
      auction.winning_bid = bid
      auction.winner_name = bidder.name
    logging.info(
        '%s wins with a bid of %d.',
        auction.winner_name, auction.winning_bid)

  def _CompleteAuction(self):
    """Conducts the payments following an auction."""
    winner = self._players_by_name[self._board.auction.winner_name]
    winner_holdings = self._GetHoldings(winner)
    bid = self._board.auction.winning_bid
    logging.info(
        '%s pays %d for %s.',
        winner.name, bid, printing.Cards(self._board.auction.cards))
    if bid > winner_holdings.money:
      raise _FoulPlayException(
          winner,
          'bid %d and won but only has %d' % (bid, winner_holdings.money))
    winner_holdings.money -= bid
    winner.PayMoney(bid)
    logging.info(
        '%s pays %d and has %d left.',
        winner_holdings.name, bid, winner_holdings.money)
    winner_holdings.purchases.extend(self._board.auction.cards)
    winner.AcceptCards(self._board.auction.cards, from_auction=True)

    num_sellers = len(self._board.auction.seller_names)
    if num_sellers == 1:
      payouts = [bid]
    elif num_sellers == 2:
      # Split between the two, favoring the first (who played the double).
      # Note that some instructions say second seller takes all.
      payouts = [(bid + 1) / 2, bid / 2]
    else:
      raise RuntimeError('should be 1 or 2 sellers, but had %d', num_sellers)
    for seller_name, payout in zip(self._board.auction.seller_names, payouts):
      if seller_name == winner.name:
        logging.info('The bank takes %d.', payout)
        continue
      seller = self._players_by_name[seller_name]
      seller_holdings = self._GetHoldings(seller)
      seller_holdings.money += payout
      logging.info(
          '%s gets paid %d and now has %d.',
          seller_name, payout, seller_holdings.money)
      seller.AcceptMoney(payout)

  def _RecordPlacings(self):
    """Records which artists' paintings placed (in order) this round."""
    per_artist_counts = analysis.CountPurchasesPerArtist(
        self._board.player_holdings)
    rankings = sorted(
        [(n, artist) for artist, n in per_artist_counts.iteritems()])
    outcome = self._board.round_outcomes.add()
    for (_, artist), value in zip(rankings, _ARTIST_VALUES):
      logging.info('%s garners %d.', printing.ArtistName(artist), value)
      outcome.artist_outcomes.add(artist=artist, value=value)

  def _AssignWinningsAndClearPurchases(self):
    """Calculates cumulative painting values, pays players for purchases."""
    values = analysis.GetFinishingArtistValues(self._board.round_outcomes)
    for artist, value in values.iteritems():
      logging.info(
          '%s is worth %d this round.', printing.ArtistName(artist), value)

    for holdings in self._board.player_holdings:
      winnings = 0
      for card in holdings.purchases:
        winnings += values.get(card.artist, 0)
      player = self._players_by_name[holdings.name]
      logging.info(
          '%s gets paid %d for: %s',
          player.name, winnings, printing.Cards(holdings.purchases))
      del holdings.purchases[:]
      holdings.money += winnings
      player.AcceptMoney(winnings)

  def _PickWinner(self):
    """Returns the player with the most money."""
    winner_info = None
    for holdings in self._board.player_holdings:
      logging.info('%s finishes with %d', holdings.name, holdings.money)
      if winner_info is None or holdings.money > winner_info.money:
        winner_info = holdings
    logging.info('%s is the winner!', winner_info.name)
    return self._players_by_name[winner_info.name]


def _GetNewCardCount(round_index, num_players):
  """Returns the number of new cards each player should get this round."""
  player_count_index = max(0, min(2, num_players - 3))
  clamped_round_index = max(0, min(3, round_index))
  return (
    (10, 6, 6, 0),
    (9, 4, 4, 0),
    (8, 3, 3, 0))[player_count_index][clamped_round_index]


def _TakeCards(source_cards, num):
  """Removes num cards from source_cards and returns them."""
  if num > len(source_cards):
    raise ValueError('Cannot take more than all cards.')
  cards = list(source_cards)
  del source_cards[:]
  taken_cards = cards[:num]
  source_cards.extend(cards[num:])
  return taken_cards


def _MoveCards(cards, src, dst):
  for card in cards:
    try:
      src.remove(card)
    except ValueError:
      logging.error('%s not in %s', printing.Cards([card]), printing.Cards(src))
      raise
  dst.extend(cards)


# Definition of how many of what cards there are in the deck.
# acc. http://boardgamegeek.com/thread/239213/card-distribution-count
_CARD_SPECS = {
  modernart_pb2.Artist.LITE_METAL: {
    modernart_pb2.AuctionType.SEALED: 3,
    modernart_pb2.AuctionType.FIXED: 2,
    modernart_pb2.AuctionType.ONCE_AROUND: 2,
    modernart_pb2.AuctionType.OPEN: 3,
    modernart_pb2.AuctionType.DOUBLE: 2,
  },
  modernart_pb2.Artist.YOKO: {
    modernart_pb2.AuctionType.SEALED: 2,
    modernart_pb2.AuctionType.FIXED: 3,
    modernart_pb2.AuctionType.ONCE_AROUND: 3,
    modernart_pb2.AuctionType.OPEN: 3,
    modernart_pb2.AuctionType.DOUBLE: 2,
  },
  modernart_pb2.Artist.CHRISTIN_P: {
    modernart_pb2.AuctionType.SEALED: 3,
    modernart_pb2.AuctionType.FIXED: 3,
    modernart_pb2.AuctionType.ONCE_AROUND: 3,
    modernart_pb2.AuctionType.OPEN: 3,
    modernart_pb2.AuctionType.DOUBLE: 2,
  },
  modernart_pb2.Artist.KARL_GITTER: {
    modernart_pb2.AuctionType.SEALED: 3,
    modernart_pb2.AuctionType.FIXED: 3,
    modernart_pb2.AuctionType.ONCE_AROUND: 3,
    modernart_pb2.AuctionType.OPEN: 3,
    modernart_pb2.AuctionType.DOUBLE: 3,
  },
  modernart_pb2.Artist.KRYPTO: {
    modernart_pb2.AuctionType.SEALED: 3,
    modernart_pb2.AuctionType.FIXED: 3,
    modernart_pb2.AuctionType.ONCE_AROUND: 3,
    modernart_pb2.AuctionType.OPEN: 4,
    modernart_pb2.AuctionType.DOUBLE: 3,
  },
}


def _MakeDeck():
  """Sets up a shuffled deck of new cards for the game."""
  cards = []
  for artist, counts in _CARD_SPECS.iteritems():
    artist_cards = []
    for auction_type, count in counts.iteritems():
      for _ in xrange(count):
        artist_cards.append(modernart_pb2.Card(
            artist=artist, auction_type=auction_type))
    logging.debug(
        '%d cards of %s',
        len(artist_cards), printing.ArtistName(artist))
    cards.extend(artist_cards)
  logging.debug('Prepared a %d card deck.', len(cards))
  random.shuffle(cards)
  return cards


class _FoulPlayException(RuntimeError):
  """A Player has broken the rules or done something nonsensical."""

  def __init__(self, player, reason):
    if player:
      msg = '%s %s: foul play ends the game!' % (player.name, reason)
    else:
      msg = reason
    super(_FoulPlayException, self).__init__(msg)

import collections
import logging
import random

import modernart_pb2
import printing


MIN_PLAYERS = 3
MAX_PLAYERS = 5

_NUM_ROUNDS = 4
_INITIAL_MONEY = 100
_NUM_TO_END_ROUND = 5
_ARTIST_VALUES = [30, 20, 10]


class GameMaster(object):
  """Track game state and control game flow according to the rules."""

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
      if self._board.auction.ends_round:
        break
      self._RunAuction()
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
    seller = self._players[self._next_seller_index]
    self._next_seller_index = (self._next_seller_index + 1) % len(self._players)
    cards = seller.GetCardsForAuction(self._board.auction)
    logging.info(
        '%s puts %s up for auction.', seller.name, printing.Cards(cards))
    if not cards:
      raise _FoulPlayException(seller, 'provided no cards for auction')
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

  def _CheckAndMaybeSetAuctionEndsRound(self):
    """If current purchases + cards for auction are enough, ends the round."""
    per_artist_counts = _CountPurchasesPerArtist(self._board.player_holdings)
    for card in self._board.auction.cards:
      per_artist_counts[card.artist] += 1
    for artist, count in per_artist_counts.iteritems():
      if count >= _NUM_TO_END_ROUND:
        self._board.auction.ends_round = True
        logging.info(
            'Round ends with %d from %s.', count, printing.ArtistName(artist))

  def _GetHoldings(self, player):
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
      self._next_seller_index = (
          self._next_seller_index + 1) % len(self._players)
      if potential_seller.name == self._board.auction.seller_names[0]:
        logging.info(
            '%s gets the %s for free.',
            potential_seller.name,
            printing.Cards(self._board.auction.cards))
        self._board.auction.winner_name = potential_seller.name
        return

      cards = potential_seller.GetCardsForAuction(self._board.auction)
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
      if card.artist != self._board.auction.cards[0]:
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

  def _RunAuction(self):
    # FIXME
    next_buyer_index = self._next_seller_index
    buyer = self._players[next_buyer_index]
    self._board.auction.winner_name = buyer.name
    self._board.auction.winning_bid = 1
    logging.info('Bogus auction! %s bids 1 and wins instantly.', buyer.name)

  def _CompleteAuction(self):
    winner = self._players_by_name[self._board.auction.winner_name]
    winner_holdings = self._GetHoldings(winner)
    bid = self._board.auction.winning_bid
    logging.info(
        '%s pays %d for %s.',
        winner.name, bid, printing.Cards(self._board.auction.cards))
    if bid > winner_holdings.money:
      raise _FoulPlayException(
          winner,
          'bid %d and won but only has %d' % bid, winner_holdings.money)
    winner_holdings.money -= bid
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
      seller = self._players_by_name[seller_name]
      self._GetHoldings(seller).money += payout
      seller.AcceptMoney(payout)

  def _RecordPlacings(self):
    """Records which artists' paintings placed (in order) this round."""
    per_artist_counts = _CountPurchasesPerArtist(self._board.player_holdings)
    rankings = sorted(
        [(n, artist) for artist, n in per_artist_counts.iteritems()])
    outcome = self._board.round_outcomes.add()
    for (_, artist), value in zip(rankings, _ARTIST_VALUES):
      logging.info('%s garners %d.', printing.ArtistName(artist), value)
      outcome.artist_outcomes.add(artist=artist, value=value)

  def _AssignWinningsAndClearPurchases(self):
    """Calculates cumulative painting values, pays players for purchases."""
    values = {}
    outcomes = self._board.round_outcomes
    for outcome in outcomes[-1].artist_outcomes:
      values[outcome.artist] = outcome.value
    for round_outcome in outcomes[:-1]:
      for outcome in round_outcome.artist_outcomes:
        if outcome.artist in values:
          values[outcome.artist] += outcome.value
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


def _MakeDeck(shuffled=True):
  """Sets up a (shuffled) deck of new cards for the game."""
  cards = []
  for artist, counts in _CARD_SPECS.iteritems():
    artist_cards = []
    for auction_type, count in counts.iteritems():
      for _ in xrange(count):
        artist_cards.append(modernart_pb2.Card(
            artist=artist, auction_type=auction_type))
    logging.debug(
        '%d cards for %s',
        len(artist_cards), printing.ArtistName(artist))
    cards.extend(artist_cards)
  logging.debug('Prepared a %d card deck.', len(cards))
  if shuffled:
    random.shuffle(cards)
  return cards


def _CountPurchasesPerArtist(holdings):
  """Counts how many of each artist were (cumulatively) purchased this round.

  Args:
    holdings: An iterable of PlayerHoldings, of which the purchases fields will
        be read.

  Returns:
    A defaultdict of {Artist.Id: int} (default value 0).
  """
  counts = collections.defaultdict(lambda: 0)
  for holding in holdings:
    for card in holding.purchases:
      counts[card.artist] += 1
  return counts


class _FoulPlayException(RuntimeError):

  def __init__(self, player, reason):
    super(_FoulPlayException, self).__init__(
        '%s %s: foul play ends the game!' % (player.name, reason))

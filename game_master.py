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
    self._next_buyer_index = 0


  def Play(self):
    """Runs a game, returning the winning player."""
    self._board = modernart_pb2.Board(
        deck=_MakeDeck())
    for player in self._players:
      self._board.player_holdings.add(
          name=player.name,
          money=_INITIAL_MONEY)

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
      per_artist_counts = _CountPurchasesPerArtist(self._board.player_holdings)
      if any(count > _NUM_TO_END_ROUND
             for count in per_artist_counts.values()):
        break
      self._RunAuction()
    self._RecordPlacings(per_artist_counts)
    self._AssignWinningsAndClearPurchases()


  def _StartAuction(self):
    raise NotImplementedError()


  def _RunAuction(self):
    raise NotImplementedError()


  def _RecordPlacings(self, per_artist_counts):
    """Records which artists' paintings placed (in order) this round."""
    rankings = sorted(n, artist for artist, n in per_artist_counts.iteritems())
    outcome = self._board.round_outcomes.add()
    for (_, artist), value in zip(rankings, _ARTIST_VALUES):
      outcome.artist_outcomes.add(artist=artist, value=value)


  def _AssignWinningsAndClearPurchases(self):
    """Calculates cumulative painting values, pays players for purchases."""
    values = {}
    outcomes = self._board.round_outcomes
    for outcome in outcomes[-1]:
      values[outcome.artist] = outcome.value
    for round_outcome in outcomes[:-1]:
      for outcome in round_outcome:
        if outcome.artist in values:
          values[outcome.artist] += outcome.value

    for holdings in self._board.player_holdings:
      winnings = 0
      for card in holdings.purchases:
        winnings += values.get(card.artist, 0)
      del holdings.purchases[:]
      holdings.money += winnings


  def _PickWinner(self):
    """Returns the player with the most money."""
    winner_info = None
    for holding in self._board.player_holdings:
      if winner_info is None or holding.money > winner_info.money:
        winner_info = holding
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

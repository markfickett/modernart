import logging
import random

import modernart_pb2
import printing


MIN_PLAYERS = 3
MAX_PLAYERS = 5

_NUM_ROUNDS = 4


class GameMaster(object):

  def __init__(self, player_objs):
    youngest_index = player_objs.index(
        min(player_objs, key=lambda p: p.size))
    self._players = player_objs[youngest_index:] + player_objs[:youngest_index]
    self._next_seller_index = 0

  def Play(self):
    self._board = modernart_pb2.Board(
        deck=_MakeDeck())
    for player in self._players:
      self._board.player_holdings.add(
          name=player.name,
          money=100)
    logging.debug('Starting board: %s', self._board)

    for round_index in range(_NUM_ROUNDS):
      self._PlayRound(round_index)

    return self._PickWinner()


  def _PlayRound(self, round_index):
    for holding in self._board.player_holdings:
      holding.hand.extend(_TakeCards(
          self._board.deck,
          _GetNewCardCount(round_index, len(self._players))))


  def _PickWinner(self):
    winner_info = None
    for holding in self._board.player_holdings:
      if winner_info is None or holding.money > winner_info.money:
        winner_info = holding
    for player in self._players:
      if winner_info.name == player.name:
        return player
    raise RuntimeError(
        'Holdings name %r corresponds to no Player.', winner_info.name)


def _GetNewCardCount(round_index, num_players):
  player_count_index = max(0, min(2, num_players - 3))
  clamped_round_index = max(0, min(3, round_index))
  return (
    (10, 6, 6, 0),
    (9, 4, 4, 0),
    (8, 3, 3, 0))[player_count_index][clamped_round_index]


def _TakeCards(source_cards, num):
  if num > len(source_cards):
    raise ValueError('Cannot take more than all cards.')
  cards = list(source_cards)
  del source_cards[:]
  taken_cards = cards[:num]
  source_cards.extend(cards[num:])
  return taken_cards


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

import logging
import random

import modernart_pb2
import printing


MIN_PLAYERS = 3
MAX_PLAYERS = 5

_INITIAL_CARDS = 13


class GameMaster(object):

  def __init__(self, player_objs):
    self._players = player_objs

  def Play(self):
    self._board = modernart_pb2.Board(
        deck=_MakeDeck())
    for player in self._players:
      self._board.player_holdings.add(
          name=player.name,
          money=100,
          hand=_TakeCards(self._board.deck, _INITIAL_CARDS))
    logging.debug('Starting board: %s', self._board)
    return self._players[0]


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

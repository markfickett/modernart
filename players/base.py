import logging

import modernart_pb2


class PlayerWrapper(object):
  """Insulates the game from the (untrustworhy / 3rd party) Players."""

  def __init__(self, player_obj, size):
    self._wrapped = player_obj
    self.name = player_obj.name
    self.size = size

  def AcceptCards(self, cards, from_auction=False):
    try:
      self._wrapped.AcceptCards(
          self._CopyCards(cards), from_auction=from_auction)
    except:
      logging.error('Player failed to receive cards.', exc_info=True)

  def AcceptMoney(self, money):
    try:
      self._wrapped.AcceptMoney(money)
    except:
      logging.error('Player failed to receive money.', exc_info=True)

  def GetCardsForAuction(self, auction):
    try:
      return self._CopyCards(
          self._wrapped.GetCardsForAuction(self._CopyAuction(auction)))
    except:
      logging.error('Player did not provide cards for auction.', exc_info=True)
      return []

  @staticmethod
  def _CopyCards(cards):
    copies = []
    for card in cards:
      copy = modernart_pb2.Card()
      copy.CopyFrom(card)
      copies.append(card)
    return copies

  @staticmethod
  def _CopyAuction(auction):
    copy = modernart_pb2.Auction()
    copy.CopyFrom(auction)
    return copy


class Player(object):
  """A reference implementation (and potential base class) Player."""
  _inst_count = 0

  def __init__(self):
    self._name = 'Naive %s' % Player._inst_count
    Player._inst_count += 1
    self._cards_in_hand = []
    self._money = 0

  @property
  def name(self):
    return self._name

  def AcceptCards(self, cards, from_auction=False):
    if not from_auction:
      self._cards_in_hand += cards

  def AcceptMoney(self, money):
    self._money += money

  def GetCardsForAuction(self, auction):
    # Playing on a double is hard: skip it! Otherwise just play any card.
    return [] if auction.cards else [self._cards_in_hand.pop()]

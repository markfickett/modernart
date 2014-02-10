import logging


class PlayerWrapper(object):

  def __init__(self, player_obj, size):
    self._wrapped = player_obj
    self.name = player_obj.name
    self.size = size

  def AcceptCards(self, cards):
    try:
      self._wrapped.AcceptCards(card.Copy() for card in cards)
    except:
      logging.error('Player failed to receive cards.', exc_info=True)


class Player(object):
  _inst_count = 0

  def __init__(self):
    self._name = 'Naive %s' % Player._inst_count
    Player._inst_count += 1
    self._cards = []

  @property
  def name(self):
    return self._name

  def AcceptCards(self, cards):
    self._cards += cards

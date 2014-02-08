MIN_PLAYERS = 3
MAX_PLAYERS = 5

class GameMaster(object):

  def __init__(self, players):
    self._players = players

  def Play(self):
    return self._players[0]

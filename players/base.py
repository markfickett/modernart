class Player(object):
  _inst_count = 0

  def __init__(self):
    self._name = 'Naive %s' % Player._inst_count
    Player._inst_count += 1

  @property
  def name(self):
    return self._name

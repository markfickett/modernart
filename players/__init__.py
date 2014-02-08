import importlib
import logging
import os
import random

def LoadPlayers():
  module_files = os.listdir(os.path.dirname(__file__))
  module_names = set(
      os.path.splitext(name)[0] for name in module_files
      if not name.startswith('_'))
  modules = []
  for module_name in module_names:
    try:
      player_module = importlib.import_module('.' + module_name, __name__)
    except:
      logging.error('Failure importing player module.', exc_info=True)
      continue
    modules.append(player_module)
  return _InstantiatePlayers(modules)


def _InstantiatePlayers(modules):
  n = min(5, max(3, len(modules)))
  ok_modules = list(modules)
  random.shuffle(ok_modules)
  i = 0
  player_objs = []
  while n > 0:
    if not ok_modules:
      raise RuntimeError('Not enough players instantiable.')
    try:
      player = ok_modules[i].Player()
      i = (i + 1) % len(ok_modules)
      n -= 1
      player_objs.append(player)
    except:
      del ok_modules[i]
      logging.error('Failure instantiating player.', exc_info=True)
  return player_objs
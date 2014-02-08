import base
import importlib
import logging
import os
import random


def LoadPlayers(min_players, max_players):
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
  return _InstantiatePlayers(modules, min_players, max_players)


def _InstantiatePlayers(modules, min_players, max_players):
  n = min(max_players, max(min_players, len(modules)))
  ok_modules = list(modules)
  random.shuffle(ok_modules)
  i = 0
  player_objs = []
  used_names = set()
  while n > 0:
    if not ok_modules:
      raise RuntimeError('Not enough players instantiable.')
    try:
      raw_player = ok_modules[i].Player()
      player = base.PlayerWrapper(
          raw_player, os.stat(ok_modules[i].__file__).st_size)
      if player.name in used_names:
        raise RuntimeError('Name %r already used.', player.name)
      used_names.add(player.name)
      i = (i + 1) % len(ok_modules)
      n -= 1
      player_objs.append(player)
    except:
      del ok_modules[i]
      logging.error('Failure instantiating player.', exc_info=True)
  return player_objs

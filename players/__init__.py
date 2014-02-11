"""The Players competing in the game.

The base module defines functions to load the Players, as well as a
PlayerWrapper to insulate the game from any errors (or malicious behavior) in
the Players, and an example naive Player.

More Players may be added by placing a module (either as source or bytecode) in the players/ directory; such modules must define a Player class similar to (or subclassing) base.Player.

When a game is started, Players are loaded/instantiated. If necessary to fill out a game, more than one instance of the Player from any module may be used; if too many modules are present, a random subset is used.
"""

import importlib
import logging
import os
import random

import base


def LoadPlayers(min_players, max_players):
  """Loads, instantiates, and returns Players to compete in a game."""
  logging.info('Gathering the players.')
  module_files = os.listdir(os.path.dirname(__file__))
  module_names = set(
      os.path.splitext(name)[0] for name in module_files
      if not (name.startswith('_') or name.startswith('.')))
  modules = []
  for module_name in module_names:
    try:
      player_module = importlib.import_module('.' + module_name, __name__)
    except:
      logging.error(
          'Failure importing player module %r relative to %r.',
          '.' + module_name,
          __name__,
          exc_info=True)
      continue
    modules.append(player_module)
  return _InstantiatePlayers(modules, min_players, max_players)


def _InstantiatePlayers(modules, min_players, max_players):
  """Given modules defining Players, instantiates Players and returns them."""
  n = min(max_players, max(min_players, len(modules)))
  logging.info('Instantiating %d players.', n)
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

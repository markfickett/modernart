"""The Players competing in the game.

The base module defines functions to load the Players, as well as a
PlayerWrapper to insulate the game from any errors (or malicious behavior) in
the Players, and an example naive Player.

More Players may be added by placing a module (either as source or bytecode) in
the players/ directory; such modules must define a Player class similar to (or
subclassing) base.Player.

When a game is started, Players are loaded/instantiated. If necessary to fill
out a game, more than one instance of the Player from any module may be used; if
 too many modules are present, a random subset is used.
"""

import importlib
import logging
import os
import random

import base
import interactive


MIN_PLAYERS = 3
MAX_PLAYERS = 5


def LoadPlayers(num_players=None, num_interactive=0):
  """Loads, instantiates, and returns Players to compete in a game."""
  VerifyPlayerCounts(num_players, num_interactive)

  logging.debug('Gathering the players.')
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
  return _InstantiatePlayers(modules, num_players, num_interactive)


def _InstantiatePlayers(modules, num_players, num_interactive_orig):
  """Given modules defining Players, instantiates Players and returns them."""
  if num_players is None:
    n = max(MIN_PLAYERS, min(MAX_PLAYERS, len(modules)))
  else:
    n = num_players
  logging.debug('Instantiating %d players.', n)

  player_objs = []
  num_interactive = num_interactive_orig
  while num_interactive > 0:
    num_interactive -= 1
    try:
      player_objs.append(base.PlayerWrapper(
          interactive.Player(), os.stat(interactive.__file__).st_size))
    except:
      logging.error('Could not set up an interactive player.', exc_info=True)
      break
    n -= 1

  ok_modules = list(m for m in modules if m is not interactive)
  random.shuffle(ok_modules)
  i = 0
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
      logging.error('Failure instantiating player.', exc_info=True)
      del ok_modules[i]
      i = i % len(ok_modules)
  return player_objs


def VerifyPlayerCounts(num_players, num_interactive):
  if num_players is None:
    if num_interactive > MAX_PLAYERS:
      raise ValueError(
          '%d interactive is more than max of %d players'
          % (num_interactive, MAX_PLAYERS))
  else:
    if num_interactive > num_players:
      raise ValueError(
          'cannot have %d interactive with only %d players'
          % (num_interactive, num_players))

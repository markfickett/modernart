import logging

import game_master
import modernart_pb2
import players


logging.basicConfig(
    format='\t%(message)s',
    level=logging.DEBUG)


if __name__ == '__main__':
  player_objs = players.LoadPlayers(
      game_master.MIN_PLAYERS, game_master.MAX_PLAYERS)
  gm = game_master.GameMaster(player_objs)
  gm.Play()

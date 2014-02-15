import argparse
import logging

import game_master
import modernart_pb2
import players


logging.basicConfig(
    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
    level=logging.DEBUG)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--num_players', '-n', type=int,
      choices=range(players.MIN_PLAYERS, players.MAX_PLAYERS + 1),
      help='The number of Players, in [3, 5]. If too many Player modules are'
           ' available, duplicates some. If too many are available, omits'
           ' some.')
  args = parser.parse_args()

  player_objs = players.LoadPlayers(num_players=args.num_players)
  gm = game_master.GameMaster(player_objs)
  gm.Play()

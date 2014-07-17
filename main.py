import argparse
import logging

import game_master
import modernart_pb2
import players


logging.basicConfig(
    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
    level=logging.INFO)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--num_players', '-n', type=int,
      choices=range(players.MIN_PLAYERS, players.MAX_PLAYERS + 1),
      help='The number of Players, in [3, 5]. If too many Player modules are'
           ' available, duplicates some. If too many are available, omits'
           ' some.')
  parser.add_argument(
      '--interactive', '-i', action='count',
      help='Include an interactive player. Repeate for multiple interactives.')
  args = parser.parse_args()
  try:
    players.VerifyPlayerCounts(args.num_players, args.interactive)
  except ValueError, e:
    parser.error(e.message)

  player_objs = players.LoadPlayers(
      num_players=args.num_players, num_interactive=args.interactive)
  gm = game_master.GameMaster(player_objs)
  gm.Play()

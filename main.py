import argparse
import collections
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
  parser.add_argument(
      '--batch', '-b', type=int, default=1,
      help='Run multiple games. Logging is reduced and aggregate stats shown.')
  args = parser.parse_args()
  if args.interactive and args.batch > 1:
    parser.error('No interactives allowed in batch runs.')
  try:
    players.VerifyPlayerCounts(args.num_players, args.interactive)
  except ValueError, e:
    parser.error(e.message)

  win_counts = collections.defaultdict(lambda: 0)
  for game_num in xrange(args.batch):
    player_objs = players.LoadPlayers(
        num_players=args.num_players, num_interactive=args.interactive)
    gm = game_master.GameMaster(player_objs)
    if args.batch > 1:
      gm.log.setLevel(logging.WARNING)
    winner = gm.Play()
    win_counts[winner.GetWrappedModuleName()] += 1
    if args.batch > 1:
      logging.info(
          '%4d: %s' % (
              game_num,
              ' '.join(
                  '%8s: %3d %3d%%' % (name, wins, 100.0 * wins/(game_num + 1.0))
                  for name, wins in sorted(win_counts.items()))))

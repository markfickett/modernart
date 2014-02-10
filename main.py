import game_master
import logging
import modernart_pb2
import players

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
    level=logging.DEBUG)


if __name__ == '__main__':
  player_objs = players.LoadPlayers(
      game_master.MIN_PLAYERS, game_master.MAX_PLAYERS)
  gm = game_master.GameMaster(player_objs)
  winner = gm.Play()

import logging
import modernart_pb2
import players

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
    level=logging.INFO)


if __name__ == '__main__':
  logging.info('Welcome To Modern Art')
  player_objs = players.LoadPlayers()
  logging.info(
      'The players are: %s',
      ', '.join(player.name for player in player_objs))

import logging
import random

import modernart_pb2


class PlayerWrapper(object):
  """Insulates the game from the (untrustworhy / 3rd party) Players."""

  def __init__(self, player_obj, size):
    self._wrapped = player_obj
    self.name = player_obj.name
    self.size = size

  def AcceptCards(self, cards, from_auction=False):
    if not hasattr(self._wrapped, 'AcceptCards'):
      return
    try:
      self._wrapped.AcceptCards(
          self._CopyCards(cards), from_auction=from_auction)
    except:
      logging.error('Player failed to receive cards.', exc_info=True)

  def AcceptMoney(self, money):
    if not hasattr(self._wrapped, 'AcceptMoney'):
      return
    try:
      self._wrapped.AcceptMoney(money)
    except:
      logging.error('Player failed to receive money.', exc_info=True)

  def PayMoney(self, money):
    if not hasattr(self._wrapped, 'PayMoney'):
      return
    try:
      self._wrapped.PayMoney(money)
    except:
      logging.error('Player failed to pay money.', exc_info=True)

  def GetCardsForAuction(self, board):
    try:
      return self._CopyCards(
          self._wrapped.GetCardsForAuction(self._SanitizeBoard(board)))
    except:
      logging.error('Player did not provide cards for auction.', exc_info=True)
      return []

  def GetBidForAuction(self, board, as_seller=False):
    try:
      bid = self._wrapped.GetBidForAuction(
          self._SanitizeBoard(board), as_seller=as_seller)
      return None if bid is None else max(0, int(bid))
    except:
      logging.error('Player did not provide bid for auction.', exc_info=True)
      return 0

  def _SanitizeBoard(self, board):
    copy = modernart_pb2.Board()
    copy.CopyFrom(board)
    copy.ClearField('deck')
    for holdings in copy.player_holdings:
      if holdings.name != self.name:
        holdings.ClearField('hand')
        holdings.ClearField('money')
    return copy

  @staticmethod
  def _CopyCards(cards):
    copies = []
    for card in cards:
      copy = modernart_pb2.Card()
      copy.CopyFrom(card)
      copies.append(card)
    return copies


class Player(object):
  """A reference implementation (and potential base class) Player."""
  _inst_count = 0

  def __init__(self):
    """Initializes the Player with a unique name and an empty hand/wallet."""
    self._name = 'Naive %s' % Player._inst_count
    Player._inst_count += 1
    self._cards_in_hand = []
    self._money = 0

  @property
  def name(self):
    """The Player's name, which must be unique within a game.

    Note that more than one instance of any Player class may participate in the
    same game, depending on how many different Player classes are available.
    """
    return self._name

  def AcceptCards(self, cards, from_auction=False):
    """Called when a Player gets cards, either dealt or from purchases.

    Args:
      cards: Copies of the Card objects.
      from_auction: If False, the cards are for the Player's hand (dealt at the
          beginning of a round). Otherwise they are purchases/winnings.
    """
    if not from_auction:
      self._cards_in_hand += cards

  def AcceptMoney(self, money):
    """Called when a player gets money.

    This may be the initial balance, for purchases from another Player, or for
    purchases by the bank at the end of a round.

    Args:
      money: An integer amount of money.
    """
    self._money += money

  def PayMoney(self, money):
    """Called when a player pays out money to another Player or the bank."""
    self._money -= money

  def GetCardsForAuction(self, board):
    """Called when an auction is beginning.

    Args:
      board: A sanitized view of the board, with the current/empty auction. If a
          previous player started with a double and no other card, the double
          will be in board.auction.cards.

    Returns:
      A list of zero, one or two Cards. Returning zero cards skips this Player's
      turn as seller.
    """
    auction = board.auction
    if not self._cards_in_hand:
      return []
    if auction.cards:  # an unclaimed double
      return self._GetCardsForDouble(auction.cards[0].artist)
    else:
      cards = [self._cards_in_hand.pop()]
      if cards[0].auction_type == modernart_pb2.AuctionType.DOUBLE:
        cards += self._GetCardsForDouble(cards[0].artist)
      return cards

  def _GetCardsForDouble(self, artist):
    """Picks a card (or no card) to play on/with a double. Returns a list."""
    if random.random() < .5:
      return []
    for i, card in enumerate(self._cards_in_hand):
      if (card.artist == artist and
          card.auction_type != modernart_pb2.AuctionType.DOUBLE):
        del self._cards_in_hand[i]
        return [card]
    return []

  def GetBidForAuction(self, board, as_seller=False):
    """Called during an auction to bid on cards.

    Args:
      board: A copy of the Board with only Player-visible details, including
          the in-progress Auction.
      as_seller: If False, this Player is bidding to buy the painting. If True,
          this Player is setting the bid for a fixed-price auction.

    Returns:
      An integer >= 0, or None to pass.
    """
    auction = board.auction
    if as_seller:
      # We are setting a fixed-price auction's cost. Don't set it at more than
      # we have, just in case we have to buy it back.
      return min(self._money, random.randint(5, 50))
    else:
      # Just pass 10% of the time, or if we can't bid enough.
      if random.random() < 0.1 or (
          auction.winning_bid and auction.winning_bid >= self._money):
        return None

      atype = auction.cards[-1].auction_type
      if atype == modernart_pb2.AuctionType.SEALED:
        bid = min(self._money, random.randint(1, 50))
      elif atype == modernart_pb2.AuctionType.FIXED:
        bid = auction.winning_bid if random.random() < .4 else None
      elif atype == modernart_pb2.AuctionType.ONCE_AROUND:
        bid = min(self._money, auction.winning_bid + random.randint(1, 20))
        bid = bid if random.random() < .8 else None
      else:  # open
        bid = min(self._money, auction.winning_bid + random.randint(1, 10))
        bid = None if random.random() < (.01 * bid) else bid
      return None if bid == 0 else bid

      return min(self._money, random.randint(1, 10))

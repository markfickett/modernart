import logging

import modernart_pb2
import printing


class Player(object):
  """A player which prompts on stdin to make all decisions."""

  def __init__(self):
    """Initializes the Player with a unique name and an empty hand/wallet."""
    self.name = raw_input('What is your name? ')

  def GetCardsForAuction(self, board):
    """Summarizes the board, then prompts for a card (or two) for auction.

    Returns:
      A list of zero (to pass), one or two Cards.
    """
    hand = self._Summarize(board)
    cards = []
    try:
      card_index = raw_input('Card # for auction [pass]? ')
      cards.append(hand[int(card_index)])
      if cards[0].auction_type == modernart_pb2.AuctionType.DOUBLE:
        card_index = raw_input('Second card # [none]? ')
        cards.append(hand[int(card_index)])
      return cards
    except ValueError:
      return cards

  def GetBidForAuction(self, board, as_seller=False):
    """Summarizes the board (w/ the current auction), prompts for a bid.

    Returns:
      An integer >= 0, or None to pass.
    """
    self._Summarize(board)
    try:
      bid = raw_input(
          '%s bid [pass]: '
          % ('Starting' if as_seller else 'Your'))
      return int(bid)
    except ValueError:
      return None

  def _Summarize(self, board):
    summary = 'Current state of the board:'
    summary += '\nPurchases:'
    for holdings in board.player_holdings:
      is_self = holdings.name == self.name
      summary += (
          '\n\t%s %s purchased %s.' % (
          '*You' if is_self else holdings.name,
          'have' if is_self else 'has',
          printing.Cards(holdings.purchases)))
      if is_self:
        self_holdings = holdings

    summary += '\nYou have %d and your hand is:' % self_holdings.money
    sorted_hand = sorted(
        self_holdings.hand,
        key=lambda c: (c.artist, c.auction_type))
    for i, card in enumerate(sorted_hand):
      summary += '\n%d\t%s' % (i, printing.Cards([card]))

    if board.auction.cards:
      auction = board.auction
      summary += '\nAuction:'
      summary += (
          '\n\t%s selling %s' % (
          ', '.join(auction.seller_names),
          printing.Cards(auction.cards)))
      if board.auction.winner_name:
        summary += (
            '\n\tHigh bid from %s is %d.'
            % (auction.winner_name, auction.winning_bid))
      else:
        summary += '\n\tNo bid yet.'
    else:
      summary += '\nNo auction in progress yet.'
    logging.info(summary)
    return sorted_hand

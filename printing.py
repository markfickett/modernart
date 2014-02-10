"""Utilities for printing values."""

import modernart_pb2


def ArtistName(artist_id):
  """Format an Artist.Id as a capitlized name."""
  name = modernart_pb2.Artist.Id.Name(artist_id)
  name_parts = (
      part.upper() + '.' if len(part) == 1 else part.capitalize()
      for part in name.split('_'))
  return ' '.join(name_parts)


def AuctionName(auction_id):
  name = modernart_pb2.AuctionType.Id.Name(auction_id)
  return '-'.join(part.capitalize() for part in name.split('_'))


def Cards(cards):
  descriptions = []
  for card in cards:
    descriptions.append(
        '%s %s' % (AuctionName(card.auction_type), ArtistName(card.artist)))
  return ', '.join(descriptions) if descriptions else 'no Cards'

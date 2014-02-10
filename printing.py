"""Utilities for printing values."""

import modernart_pb2


def ArtistName(artist_id):
  """Format an Artist.Id as a capitlized name."""
  name = modernart_pb2.Artist.Id.Name(artist_id)
  name_parts = (
      part.upper() + '.' if len(part) == 1 else part.capitalize()
      for part in name.split('_'))
  return ' '.join(name_parts)

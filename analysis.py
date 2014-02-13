"""Functions for simple analysis of Board state."""

import collections


def CountPurchasesPerArtist(holdings):
  """Counts how many of each artist were (cumulatively) purchased this round.

  Args:
    holdings: An iterable of PlayerHoldings, of which the purchases fields will
        be read.

  Returns:
    A defaultdict of {Artist.Id: int} (default value 0).
  """
  counts = collections.defaultdict(lambda: 0)
  for holding in holdings:
    for card in holding.purchases:
      counts[card.artist] += 1
  return counts


def GetFinishingArtistValues(outcomes):
  """Finds the end-of-round value of paintings by each artist.

  Args:
    outcomes: An iterable of RoundOutcomes (each of which has a list of
        ArtistOutcomes, the value assigned to an artist).

  Returns:
    A dict of {Artist.Id: int} for artists which placed in the latest round.
  """
  values = {}
  for outcome in outcomes[-1].artist_outcomes:
    values[outcome.artist] = outcome.value
  for round_outcome in outcomes[:-1]:
    for outcome in round_outcome.artist_outcomes:
      if outcome.artist in values:
        values[outcome.artist] += outcome.value
  return values

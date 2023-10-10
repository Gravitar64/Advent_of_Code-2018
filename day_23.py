import time
import re


class Vec(tuple):
  """Vektor-Klasse für 2 bis n-dimensionale Koordinaten."""

  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __add__(self, other):
    return Vec(*tuple(a + b for a, b in zip(self, other)))

  def abstand(self, other):
    """Liefert den Manhatten-Abstand (https://de.wikipedia.org/wiki/Manhattan-Metrik) zwischen 2 Vektoren"""
    return sum(abs(a - b) for a, b in zip(self, other))


def load(file):
  with open(file) as f:
    return [list(map(int, re.findall('-?\d+', row))) for row in f]


def solve(p):
  p = [(r, Vec(x, y, z)) for x, y, z, r in p]
  r, pos = max(p)
  part1 = sum([pos.abstand(pos2) <= r for _, pos2 in p])

  transitions = []
  for r, pos in p:
    d = pos.abstand((0, 0, 0))
    transitions.append((max(0, d - r), 1))
    transitions.append((d + r + 1, -1))

  transitions.sort()

  count = maxCount = maxD = 0
  for d, e in transitions:
    count += e
    if count > maxCount:
      maxCount, maxD = count, d

  return part1, maxD


start = time.perf_counter()
puzzle = load('day_23.txt')
part1, part2 = solve(puzzle)
print(f'Part1: {part1}')
print(f'Part2: {part2}')
print(f'Ermittelt in {time.perf_counter()-start:.5f}')

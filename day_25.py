import time
import re
import itertools
import networkx as nx


def load(file):
  with open(file) as f:
    return [tuple(map(int, re.findall('-?\d+', row))) for row in f]


def solve(p):
  g = nx.Graph()
  for p1, p2 in itertools.product(p, repeat=2):
    if sum(abs(a - b) for a, b in zip(p1, p2)) > 3: continue
    g.add_edge(p1, p2)
  return nx.number_connected_components(g)


start = time.perf_counter()
puzzle = load('day_25.txt')
print(f'Part1: {solve(puzzle)}')
print(f'Ermittelt in {time.perf_counter()-start:.5f}')
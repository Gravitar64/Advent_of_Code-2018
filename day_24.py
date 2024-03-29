import time
import re


def load(file):
  with open(file) as f:
    return [[group for group in block.split('\n')] for block in f.read().split('\n\n')]


def parse(p):
  groups = []
  for army in p:
    name = army[0][:-1]
    for i, group in enumerate(army[1:], start=1):
      numbers = map(int, re.findall('\d+', group))
      dtype = re.findall('(\w+) damage', group)[0]
      
      immune = re.findall(r'immune to ([\w, ]+)[;\)]', group)
      weak = re.findall(r'weak to ([\w, ]+)[;\)]', group)
      
      if immune: immune = set(immune[0].split(', '))
      if weak:  weak = set(weak[0].split(', '))
      
      groups.append([i, name, *numbers, dtype, immune, weak, False])
  return groups


def real_damage(enemie, defender):
  if enemie[NAME] == defender[NAME] or enemie[DTYPE] in defender[IMMUNE]: return 0
  if enemie[DTYPE] in defender[WEAK]: return enemie[UNITS] * enemie[DAMAGE] * 2
  return enemie[UNITS] * enemie[DAMAGE]


def target_selection(groups):
  battles = []
  for enemie in sorted(groups, key=lambda g: (-g[UNITS] * g[DAMAGE], -g[INIT])):
    remaining_targets = [g for g in groups if not g[SELECT] and real_damage(enemie, g)]
    if not remaining_targets: continue
    defender = max(remaining_targets, key=lambda g: (real_damage(enemie, g), g[UNITS] * g[DAMAGE], g[INIT]))
    defender[SELECT] = True
    battles.append((enemie, defender))
  return battles


def attack(enemie, defender):
  damage = real_damage(enemie, defender)
  kills = min(defender[UNITS], damage // defender[HP])
  defender[UNITS] -= kills
  return kills


def solve(p,part2):
  loops = 2000 if part2 else 1
  for boost in range(loops):
    groups = parse(p)
    if part2:
      for g in groups:
        if g[NAME] == 'Infection': continue
        g[DAMAGE] += boost
    
    while True:
      pairs = target_selection(groups)
      attacking_sequenz = sorted(pairs, key=lambda pair: -pair[0][INIT])
      kills = [attack(enemie, defender) == 0 for enemie,defender in attacking_sequenz]
      
      if all(kills): break
      groups = [g for g in groups if g[UNITS] > 0]
      for g in groups: g[SELECT] = False
      armies = set([g[NAME] for g in groups])
      
      if part2 and armies == {'Infection'}: break
      if not part2 and len(armies) == 1 or part2 and armies == {'Immune System'}:
        return sum(g[UNITS] for g in groups)
      

start = time.perf_counter()
ID, NAME, UNITS, HP, DAMAGE, INIT, DTYPE, IMMUNE, WEAK, SELECT = range(10)
puzzle = load('day_24.txt')
print(f'Part1: {solve(puzzle,False)}')
print(f'Part2: {solve(puzzle,True)}')
print(f'Ermittelt in {time.perf_counter()-start:.5f}')
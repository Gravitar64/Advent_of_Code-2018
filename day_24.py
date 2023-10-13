import time
import re


class Group:
  def __init__(self,id,army,units,hp,damage,init,dtype,immune,weak):
    self.id = id
    self.army = army
    self.units = units
    self.hp = hp
    self.damage = damage
    self.dtype = dtype
    self.immune = immune
    self.weak = weak
    self.init = init
    self.power = units * damage
    self.selected = False
    

  def damage_to(self, defender):
    if self.dtype in defender.immune: return 0
    if self.dtype in defender.weak: return self.power * 2
    return self.power

  def attacked_by(self, attacker):
    damage = attacker.damage_to(self)
    kills = damage // self.hp
    self.units = max(0, self.units - kills)
    self.power = self.units * self.damage
    return kills == 0
    

def load(file):
  with open(file) as f:
    return [[group for group in block.split('\n')] for block in f.read().split('\n\n')]
  

def parse(p):
  groups = []
  for army in p:
    name = army[0][:-1]
    for i,group in enumerate(army[1:],start=1):
      numbers = map(int,re.findall('\d+',group))
      dtype = re.findall('(\w+) damage',group)[0]
      weak = re.findall(r'weak to ([a-z, ]*){?|\)}',group)
      if weak: weak = weak[0].split(', ')
      immune = re.findall(r'immune to ([a-z, ]*){?|\)}',group)
      if immune: immune = immune[0].split(', ')
      groups.append(Group(i, name, *numbers, dtype, immune, weak))
  return groups


def target_selection(groups):
  groups = sorted(groups,key=lambda x: (-x.power,-x.init))
  pairs = []
  for attacker in groups:
    remaining_targets = [g for g in groups if attacker.army != g.army and not g.selected]
    if not remaining_targets: continue
    defender = max(remaining_targets, key=lambda g: (attacker.damage_to(g), g.power, g.init))
    defender.selected = True
    pairs.append((attacker,defender))
  return pairs  


def solve(p):
  groups = parse(p)
  
  while True:
    pairs = target_selection(groups)
    pairs = sorted(pairs,key=lambda x: -x[0].init)
    kills = []
    for attacker, defender in pairs:
      kills.append(defender.attacked_by(attacker))
    if all(kills): break
    
    groups = [group for group in groups if group.units > 0]
    for g in groups: g.selected = False          
    armies = {g.army for g in groups}
    if len(armies) == 1:
      part1 =  sum(g.units for g in groups)
      break

  for boost in range(2000):
    groups = parse(p)

    for g in groups: 
      if g.army == 'Immune System': 
        g.damage += boost
        g.power = g.units * g.damage
    
    while True:
      pairs = target_selection(groups)
      pairs = sorted(pairs,key=lambda x: -x[0].init)
      for attacker, defender in pairs:
        defender.attacked_by(attacker)
      
      groups = [group for group in groups if group.units > 0]
      for g in groups: g.selected = False          
      armies = {g.army for g in groups}
      if armies == {'Infection'}: break  
      if armies == {'Immune System'}: 
        print(boost)
        return part1, sum(g.units for g in groups)
        
        
    
    
    
      
      


       

  

start = time.perf_counter()
puzzle = load('day_24.txt')
part1, part2 = solve(puzzle)
print(f'Part1: {part1}')
print(f'Part2: {part2}')
print(f'Ermittelt in {time.perf_counter()-start:.5f}')

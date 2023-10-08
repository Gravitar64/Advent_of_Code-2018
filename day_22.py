import time
import heapq


def bfs(cave, target):
  queue, best, target = [(0, 0, 0, 1)], {}, (*target,1)
  while queue:
    minutes, x, y, cannot = heapq.heappop(queue)
    best_key = (x, y, cannot)
    if best_key in best and best[best_key] <= minutes: continue
    best[best_key] = minutes
    if best_key == target: return minutes

    for i in range(3):
      if i == cannot or i == cave[x, y]: continue
      heapq.heappush(queue, (minutes + 7, x, y, i))

    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
      if (nx, ny) not in cave or cave[nx, ny] == cannot: continue
      heapq.heappush(queue, (minutes + 1, nx, ny, cannot))


def solve(depth, tx, ty):
  cave = {(0, 0): depth}
  for x in range(tx + 30):
    for y in range(ty + 30):
      if (x, y) in ((0, 0), (tx, ty)): geo = 0
      elif x == 0: geo = y * 48271
      elif y == 0: geo = x * 16807
      else:        geo = cave[x - 1, y] * cave[x, y - 1]
      cave[x, y] = (geo + depth) % 20183
  
  cave = {pos: erosion % 3 for pos, erosion in cave.items()}
  part1 = sum(risk for (x, y), risk in cave.items() if x <= tx and y <= ty)
  return part1, bfs(cave, (tx, ty))


start = time.perf_counter()
part1,part2 = solve(depth=3558, tx=15, ty=740)
print(f'Part1: {part1}')
print(f'Part2: {part2}')
print(f'Ermittelt in {time.perf_counter()-start:.5f}')

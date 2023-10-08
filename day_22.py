import time
import heapq


def bfs(cave, target):
  tools = {0:{1,2}, 1:{0,2}, 2:{0,1}}
  queue, best, target = [(0, 0, 0, 1)], {}, (*target,1)
  while queue:
    minutes, x, y, tool = heapq.heappop(queue)
    best_key = (x, y, tool)
    if best_key in best and best[best_key] <= minutes: continue
    best[best_key] = minutes
    if best_key == target: return minutes

    for new_tool in tools[cave[x,y]]-{tool}:
      heapq.heappush(queue, (minutes + 7, x, y, new_tool))

    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
      #tool == cave[nx,ny]; actual tool ist the forbidden one and will catch in next while-loop +7
      if (nx, ny) not in cave or tool == cave[nx, ny]: continue 
      heapq.heappush(queue, (minutes + 1, nx, ny, tool))


def solve(depth, tx, ty, cave = {}):
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

import time


def solve(row9, row13):
  d, s, solutions, steps = 0, set(), [], 0
  while True:
    e = d | 0x10000
    d = row9
    while True:
      steps += 1
      c = e & 0xFF
      d = (((d + c) & 0xFFFFFF) * row13) & 0xFFFFFF
      if e < 256:
        if d not in s:
          solutions.append(d)
          s.add(d)
          steps = 0
        break
      e = e // 256
      if steps > 100:
        return solutions


start = time.perf_counter()
solutions = solve(row9=4843319, row13=65899) # your numbers in row 9 (seti) and row 13 (bori)
print(f'Part1: {solutions[0]}')
print(f'Part2: {solutions[-1]}')
print(f'Ermittelt in {time.perf_counter()-start:.5f}')
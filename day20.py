from collections import deque, defaultdict
from functools import partial
from itertools import combinations

from utils import run_solution_pretty

EXAMPLE = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip()

M = list[list[str]]
C = tuple[int, int]
T = tuple[M, C, C]


def parse_input(input_str: str) -> T:
    m = [list(x) for x in input_str.strip().splitlines()]
    s = 0, 0
    e = 0, 0
    for i in range(len(m) - 1):
        for j in range(len(m[0]) - 1):
            if m[i][j] == 'S':
                s = i, j
                m[i][j] = "."
            elif m[i][j] == 'E':
                e = i, j
                m[i][j] = '.'

    if s == (0, 0) or e == (0, 0):
        raise ValueError("Start or End not found")

    return m, s, e


def get_distances(m: M, start: C) -> dict[C, int]:
    distances: dict[C, int] = {}
    to_visit: deque[tuple[int, int, int]] = deque([(0, start[0], start[1])])

    while to_visit:
        d, i, j = to_visit.popleft()
        cell = m[i][j]
        if cell == "#":
            continue

        if (i, j) in distances and distances[i, j] < d:
            continue

        distances[i, j] = d

        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            to_visit.append((d + 1, i + di, j + dj))

    return distances


def get_cheats(distances: dict[C, int], max_distance: int) -> defaultdict[int, int]:
    cheats: defaultdict[int, int] = defaultdict(int)
    combs = combinations(sorted(distances.items(), key=lambda x: x[1]), 2)

    for ((i1, j1), d1), ((i2, j2), d2) in combs:
        d = abs(i1 - i2) + abs(j1 - j2)
        saved: int = d2 - d1 - d
        if d > max_distance or saved <= 0:
            continue
        cheats[saved] += 1

    return cheats


def puzzle(data: T, max_distance: int) -> int:
    m, start, end = data
    distances = get_distances(m, start)
    cheats: defaultdict[int, int] = get_cheats(distances, max_distance)
    return sum(value for key, value in cheats.items() if key >= 100)


if __name__ == "__main__":
    run_solution_pretty(
        day=20,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=partial(puzzle, max_distance=2),
        puzzle_2=partial(puzzle, max_distance=20),
    )

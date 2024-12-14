import re
from collections import defaultdict, Counter
from functools import reduce
from operator import itemgetter
from statistics import stdev

from utils import run_solution_pretty

EXAMPLE = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()


T = list[tuple[tuple[int, int], tuple[int, int]]]


def parse_input(input_str: str) -> T:
    regex = r"p=(\d+)\,(\d+) v=(\-?\d+)\,(\-?\d+)"
    matches = map(lambda x: x.groups(), re.finditer(regex, input_str, re.MULTILINE))
    guards: T = [
        ((int(px), int(py)), (int(vx), int(vy))) for (px, py, vx, vy) in matches
    ]
    return guards


def solve(
    px: int, py: int, vx: int, vy: int, sx: int, sy: int, sec: int
) -> tuple[int, int]:
    x = (px + vx * sec) % sx
    y = (py + vy * sec) % sy
    return x, y


def calculate_positions(data: T, sx: int, sy: int, secs: int) -> list[tuple[int, int]]:
    return [solve(px, py, vx, vy, sx, sy, secs) for (px, py), (vx, vy) in data]


def puzzle_1(data: T) -> int:
    sx, sy, secs = 101, 103, 100
    final_pos = calculate_positions(
        data=data,
        sx=sx,
        sy=sy,
        secs=secs,
    )

    by_quadrant: dict[tuple[int, int], int] = defaultdict(int)
    for px, py in final_pos:
        if px > sx // 2:
            qx = +1
        elif px < sx // 2:
            qx = -1
        else:
            qx = 0

        if py > sy // 2:
            qy = +1
        elif py < sy // 2:
            qy = -1
        else:
            qy = 0

        if qy != 0 and qx != 0:
            by_quadrant[(qx, qy)] += 1

    return reduce(lambda a, b: a * b, by_quadrant.values(), 1)


def puzzle_2(data: T) -> int:
    sx, sy = 101, 103
    if len(data) < 20:
        return 0

    all_positions = []
    std_devs = []
    for secs in range(10_000):
        final_pos = calculate_positions(
            data=data,
            sx=sx,
            sy=sy,
            secs=secs,
        )
        all_positions.append(final_pos)
        std_dev_x = stdev(map(itemgetter(0), final_pos))
        std_dev_y = stdev(map(itemgetter(1), final_pos))
        std_devs.append((secs, std_dev_x, std_dev_y))

    best_candidate, _, _ = min(std_devs, key=lambda x: x[1] + x[2])
    print_matrix(all_positions[best_candidate], sx, sy)
    return best_candidate


def print_matrix(positions: list[tuple[int, int]], sx: int, sy: int) -> None:
    c = Counter(positions)
    for y in range(sy):
        for x in range(sx):
            print(c.get((x, y), "."), end="")
        print()


if __name__ == "__main__":
    run_solution_pretty(
        day=14,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

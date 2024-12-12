from collections import deque

from utils import run_solution_pretty

EXAMPLE = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()

T = list[list[str]]


def parse_input(input_str: str) -> T:
    lines = input_str.split("\n")
    return [list(line) for line in lines]


def print_matrix(data: T) -> None:
    for row in data:
        for cell in row:
            print(cell, end="")
        print()


def is_inside(data: T, pos: tuple[int, int]) -> bool:
    i, j = pos
    return 0 <= i <= (len(data) - 1) and 0 <= j <= (len(data[0]) - 1)


def puzzle_1(data: T) -> int:
    to_visit_inside: deque[tuple[int, int]] = deque([(0, 0)])
    to_visit_outside: deque[tuple[int, int]] = deque()
    visited_plots: set[tuple[int, int]] = set()

    region_areas: list[int] = []
    region_perimeters: list[int] = []

    area = 0
    perimeter = 0

    while to_visit_outside or to_visit_inside:
        if not to_visit_inside:
            to_visit_inside.append(to_visit_outside.pop())

            if area != 0 and perimeter != 0:
                region_areas.append(area)
                region_perimeters.append(perimeter)
                area = 0
                perimeter = 0

        i, j = to_visit_inside.pop()
        if (i, j) in visited_plots:
            continue

        t = data[i][j]
        visited_plots.add((i, j))

        area += 1

        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ii, jj = i + di, j + dj
            tt = data[ii][jj] if is_inside(data, (ii, jj)) else None
            if t == tt and (ii, jj) not in visited_plots and is_inside(data, (ii, jj)):
                to_visit_inside.append((ii, jj))
            elif t != tt and (ii, jj) not in visited_plots and is_inside(data, (ii, jj)):
                to_visit_outside.append((ii, jj))

            if t != tt:
                perimeter += 1

    total = 0
    for a, p in zip(region_areas, region_perimeters):
        total += a * p

    return total


def puzzle_2(data: T) -> int:
    # oof this is ugly
    to_visit_inside: deque[tuple[int, int]] = deque([(0, 0)])
    to_visit_outside: deque[tuple[int, int]] = deque()
    visited_plots: set[tuple[int, int]] = set()

    regions: list[list[tuple[int, int]]] = []
    current_region: list[tuple[int, int]] = []

    while to_visit_outside or to_visit_inside:
        if not to_visit_inside:
            to_visit_inside.append(to_visit_outside.pop())

            if current_region:
                regions.append(current_region)
                current_region = []

        i, j = to_visit_inside.pop()
        if (i, j) in visited_plots:
            continue

        t = data[i][j]
        visited_plots.add((i, j))
        current_region.append((i, j))

        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ii, jj = i + di, j + dj
            tt = data[ii][jj] if is_inside(data, (ii, jj)) else None
            if t == tt and (ii, jj) not in visited_plots and is_inside(data, (ii, jj)):
                to_visit_inside.append((ii, jj))
            elif t != tt and (ii, jj) not in visited_plots and is_inside(data, (ii, jj)):
                to_visit_outside.append((ii, jj))

    region_areas: list[int] = []
    region_sides: list[int] = []
    corners = [
        ((-1, 0), (0, -1)),  # Top-Left
        ((-1, 0), (0, +1)),  # Top-Right
        ((+1, 0), (0, +1)),  # Bottom-Right
        ((+1, 0), (0, -1)),  # Bottom-Left
    ]
    for region in regions:
        region_areas.append(len(region))

        count_corners = 0
        for i, j in region:
            t = data[i][j]

            for (di1, dj1), (di2, dj2) in corners:
                t1 = data[i + di1][j + dj1] if is_inside(data, (i + di1, j + dj1)) else "."
                t2 = data[i + di2][j + dj2] if is_inside(data, (i + di2, j + dj2)) else "."
                t3 = data[i + di1][j + dj2] if is_inside(data, (i + di1, j + dj2)) else ""

                if t != t1 and t != t2:
                    count_corners += 1

                if (t == t1 and t == t2) and t3 != t:
                    count_corners += 1

        region_sides.append(count_corners)

    total = 0
    for a, p in zip(region_areas, region_sides):
        total += a * p

    return total


if __name__ == "__main__":
    run_solution_pretty(
        day=12,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

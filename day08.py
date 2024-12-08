import copy
from collections import defaultdict
from itertools import permutations, count

from utils import run_solution_pretty

EXAMPLE = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()


T = list[list[str]]


def parse_input(input_str: str) -> T:
    lines = input_str.split("\n")
    return [list(line) for line in lines]


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def mul(a: tuple[int, int], b: int) -> tuple[int, int]:
    return a[0] * b, a[1] * b


def is_inside(data: T, pos: tuple[int, int]) -> bool:
    i, j = pos
    return 0 <= i <= (len(data) - 1) and 0 <= j <= (len(data[0]) - 1)


def print_matrix(data: T, antinodes: set[tuple[int, int]]) -> None:
    data = copy.deepcopy(data)
    for i, j in antinodes:
        if data[i][j] == ".":
            data[i][j] = "#"

    for row in data:
        print("".join(row))
    print()


def get_antennas(data: T) -> dict[str, list[tuple[int, int]]]:
    ant_char = defaultdict(list)
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == ".":
                continue

            ant_char[data[i][j]].append((i, j))

    return ant_char


def puzzle_1(data: T) -> int:
    ant_char = get_antennas(data)
    anti_nodes: set[tuple[int, int]] = set()
    for _, ants in ant_char.items():
        for a, b in permutations(ants, 2):
            c = add(a, sub(a, b))
            if is_inside(data, c):
                anti_nodes.add(c)

    print_matrix(data, anti_nodes)
    return len(anti_nodes)


def puzzle_2(data: T) -> int:
    ant_char = get_antennas(data)
    anti_nodes: set[tuple[int, int]] = set()
    for _, ants in ant_char.items():
        for a, b in permutations(ants, 2):
            anti_nodes.add(a)
            anti_nodes.add(b)
            for i in count(1):
                c = add(a, mul(sub(a, b), i))
                if not is_inside(data, c):
                    break
                anti_nodes.add(c)

    print_matrix(data, anti_nodes)
    return len(anti_nodes)


if __name__ == "__main__":
    run_solution_pretty(
        day=8,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

from collections import deque

from utils import run_solution_pretty

EXAMPLE = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

T = list[list[int]]


def parse_input(input_str: str) -> T:
    return [
        list(map(lambda x: int(x) if x != "." else -1, line))
        for line in input_str.split("\n")
    ]


def print_blocks(data: T) -> None:
    for row in data:
        for cell in row:
            if cell == -1:
                print(".", end="")
            else:
                print(cell, end="")
        print()


def find_trailheads(data: T) -> list[tuple[int, int]]:
    q = list()
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == 0:
                q.append((i, j))
    return q


def search_neighbours(data: T, i: int, j: int) -> list[tuple[int, int]]:
    q = list()
    h = data[i][j]
    if i > 0 and (data[i - 1][j] - h) == 1:
        q.append((i - 1, j))
    if j > 0 and (data[i][j - 1] - h) == 1:
        q.append((i, j - 1))
    if i < (len(data) - 1) and (data[i + 1][j] - h) == 1:
        q.append((i + 1, j))
    if j < (len(data) - 1) and (data[i][j + 1] - h) == 1:
        q.append((i, j + 1))
    return q


def puzzle_1(data: T) -> int:
    trailheads = find_trailheads(data)
    ends: set[tuple[int, int, int, int]] = set()
    for th in trailheads:
        q = deque([th])
        while len(q) > 0:
            i, j = q.pop()
            h = data[i][j]
            if h == 9:
                ends.add((th[0], th[1], i, j))
                continue

            q.extend(search_neighbours(data, i, j))

    return len(ends)


def puzzle_2(data: T) -> int:
    trailheads = find_trailheads(data)
    total = 0
    for th in trailheads:
        q = deque([th])
        while len(q) > 0:
            i, j = q.pop()
            h = data[i][j]
            if h == 9:
                total += 1
                continue

            q.extend(search_neighbours(data, i, j))

    return total


if __name__ == "__main__":
    run_solution_pretty(
        day=10,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

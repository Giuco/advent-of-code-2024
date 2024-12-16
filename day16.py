from collections import deque

from utils import run_solution_pretty

EXAMPLE = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()

A = list[list[str]]
T = tuple[A, tuple[int, int], tuple[int, int]]


def parse_input(input_str: str) -> T:
    grid = [list(x) for x in input_str.splitlines()]
    start, end = (0, 0), (0, 0)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                start = i, j
                grid[i][j] = "."
            elif cell == "E":
                end = i, j
                grid[i][j] = "."

    if start == (0, 0) or end == (0, 0):
        raise ValueError("Start or end not found")

    return grid, start, end


def puzzle_1(data: T) -> int:
    grid, start, end = data

    already_visited: dict[tuple[tuple[int, int], tuple[int, int]], int] = dict()
    to_visit: deque[tuple[int, tuple[int, int], tuple[int, int]]] = deque(
        [(0, (0, 1), start)]
    )
    points: set[int] = set()

    while to_visit:
        cp, (di, dj), (i, j) = to_visit.popleft()
        cell = grid[i][j]
        if cell == "#" or cp >= already_visited.get(((di, dj), (i, j)), float("inf")):
            continue

        if (i, j) == end:
            points.add(cp)
            continue

        if di != 0:
            to_visit.extend(
                [
                    (cp + 1, (di, dj), (i + di, j)),
                    (cp + 1001, (0, +1), (i, j + 1)),
                    (cp + 1001, (0, -1), (i, j - 1)),
                ]
            )
        else:
            to_visit.extend(
                [
                    (cp + 1, (di, dj), (i, j + dj)),
                    (cp + 1001, (+1, 0), (i + 1, j)),
                    (cp + 1001, (-1, 0), (i - 1, j)),
                ]
            )

        already_visited[((di, dj), (i, j))] = cp

    return min(points)


def puzzle_2(data: T) -> int:
    grid, start, end = data

    to_visit: deque[
        tuple[int, tuple[int, int], tuple[int, int], list[tuple[int, int]]]
    ] = deque([(0, (0, 1), start, [])])
    already_visited: dict[tuple[tuple[int, int], tuple[int, int]], int] = dict()
    points: list[tuple[int, list[tuple[int, int]]]] = list()
    min_points: int = puzzle_1(data)

    while to_visit:
        cp, (di, dj), (i, j), path = to_visit.pop()
        cell = grid[i][j]
        if (
            cell == "#"
            or cp > already_visited.get(((di, dj), (i, j)), min_points)
            or (i, j) in path
        ):
            continue

        path = [*path, (i, j)]
        if (i, j) == end:
            points.append((cp, path))
            continue

        if di != 0:
            to_visit.extend(
                [
                    (cp + 1, (di, dj), (i + di, j), path),
                    (cp + 1001, (0, +1), (i, j + 1), path),
                    (cp + 1001, (0, -1), (i, j - 1), path),
                ]
            )
        else:
            to_visit.extend(
                [
                    (cp + 1, (di, dj), (i, j + dj), path),
                    (cp + 1001, (+1, 0), (i + 1, j), path),
                    (cp + 1001, (-1, 0), (i - 1, j), path),
                ]
            )

        already_visited[((di, dj), (i, j))] = cp

    best_spots: set[tuple[int, int]] = set()

    for p, spots in points:
        for spot in spots:
            best_spots.add(spot)

    return len(best_spots)


if __name__ == "__main__":
    run_solution_pretty(
        day=16,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

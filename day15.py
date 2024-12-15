import copy
from operator import itemgetter

from utils import run_solution_pretty

EXAMPLE = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()


A = list[list[str]]
B = list[tuple[int, int]]
T = tuple[A, B]


def parse_input(input_str: str) -> T:
    raw_grid, raw_directions = input_str.split("\n\n")
    grid = [list(x) for x in raw_grid.splitlines()]

    directions: B = []
    for arrow in list(raw_directions.replace("\n", "")):
        if arrow == "^":
            directions.append((-1, 0))
        elif arrow == ">":
            directions.append((0, 1))
        elif arrow == "v":
            directions.append((1, 0))
        elif arrow == "<":
            directions.append((0, -1))
        else:
            raise ValueError(f"Invalid direction: {arrow}")

    return grid, directions


def print_grid(grid: A) -> None:
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()


def get_initial_pos(data: A) -> tuple[int, int]:
    return [
        (y, x)
        for y, row in enumerate(data)
        for x, cell in enumerate(row)
        if cell == "@"
    ][0]


def get_dir(di: int, dj: int) -> str:
    return {
        (-1, 0): "^",
        (+1, 0): "v",
        (0, -1): "<",
        (0, +1): ">",
    }[(di, dj)]


def is_inside(data: A, pos: tuple[int, int]) -> bool:
    i, j = pos
    return 0 <= i <= (len(data) - 1) and 0 <= j <= (len(data[0]) - 1)


def move_boxes(grid: A, i: int, j: int, di: int, dj: int) -> tuple[A, int, int]:
    grid = copy.deepcopy(grid)
    if di != 0:
        affected_positions = [
            (ii, j) for ii in range(i, len(grid) if di == 1 else 0, di)
        ]
    else:
        affected_positions = [
            (i, jj) for jj in range(j, len(grid[0]) if dj == 1 else 0, dj)
        ]

    to_move = []
    is_movable = True
    for ii, jj in affected_positions:
        if grid[ii][jj] == ".":
            break
        elif grid[ii][jj] == "#":
            is_movable = False
        to_move.append((ii, jj))

    # No space to move anything
    if len(to_move) == len(affected_positions):
        is_movable = False

    if not is_movable:
        return grid, i, j

    for ii, jj in reversed(to_move):
        grid[ii + di][jj + dj] = grid[ii][jj]

    grid[i][j] = "."
    return grid, i + di, j + dj


def move_boxes_wide(grid: A, i: int, j: int, di: int, dj: int) -> tuple[A, int, int]:
    to_move: set[tuple[int, int]] = {(i, j)}
    to_search: set[tuple[int, int]] = {(i + di, j + dj)}

    while to_search:
        ii, jj = to_search.pop()
        c = grid[ii][jj]

        if (ii, jj) in to_move or not is_inside(grid, (ii, jj)):
            continue
        elif c == "[":
            to_search.add((ii, jj + 1))
            to_search.add((ii + di, jj + dj))
        elif c == "]":
            to_search.add((ii, jj - 1))
            to_search.add((ii + di, jj + dj))

        to_move.add((ii, jj))

    for n, (ii, jj) in enumerate(to_move):
        if grid[ii][jj] == "#":
            return grid, i, j

        if not is_inside(grid, (ii + di, jj + dj)):
            return grid, i, j

    to_move = set(filter(lambda x: grid[x[0]][x[1]] in {"[", "]", "@"}, to_move))
    new_grid = copy.deepcopy(grid)

    for ii, jj in sorted(
        list(to_move),
        key=itemgetter(0) if di != 0 else itemgetter(1),
        reverse=max(di, dj) == 1,
    ):
        c = grid[ii][jj]
        if c in {"[", "]", "@"}:
            new_grid[ii + di][jj + dj] = c
            new_grid[ii][jj] = "."

    return new_grid, i + di, j + dj


def puzzle_1(data: T) -> int:
    data = copy.deepcopy(data)
    grid, directions = data
    i, j = get_initial_pos(grid)

    for n, (di, dj) in enumerate(directions, start=1):
        ii, jj = i + di, j + dj
        c = grid[ii][jj]
        if c == ".":
            grid[i][j] = "."
            grid[ii][jj] = "@"
            i, j = ii, jj
        elif c == "O":
            grid, i, j = move_boxes(grid, i, j, di, dj)
        elif c == "#":
            pass
        else:
            raise ValueError(f"Invalid cell: {c}")

    return sum(
        i * 100 + j
        for i, row in enumerate(grid)
        for j, cell in enumerate(row)
        if cell == "O"
    )


def expand_grid(grid: A) -> A:
    d = {"#": "##", "O": "[]", ".": "..", "@": "@."}
    new_grid: A = []
    for row in grid:
        new_row: list[str] = []
        for cell in row:
            new_row.extend(d[cell])
        new_grid.append(new_row)
    return new_grid


def puzzle_2(data: T) -> int:
    data = copy.deepcopy(data)
    grid, directions = expand_grid(data[0]), data[1]
    i, j = get_initial_pos(grid)

    for n, (di, dj) in enumerate(directions, start=1):
        ii, jj = i + di, j + dj
        c = grid[ii][jj]
        if c == ".":
            grid[i][j] = "."
            grid[ii][jj] = "@"
            i, j = ii, jj
        elif c in {"[", "]"}:
            grid, i, j = move_boxes_wide(grid, i, j, di, dj)
        elif c == "#":
            pass
        else:
            raise ValueError(f"Invalid cell: {c}")

    return sum(
        i * 100 + j
        for i, row in enumerate(grid)
        for j, cell in enumerate(row)
        if cell == "["
    )


if __name__ == "__main__":
    run_solution_pretty(
        day=15,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

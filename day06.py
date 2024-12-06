import copy

from utils import run_solution_pretty

EXAMPLE = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

T = list[list[str]]

ALL_DIRECTIONS = {
    (-1, 0): (0, +1),
    (0, +1): (+1, 0),
    (+1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def get_next_direction(current_direction: tuple[int, int]) -> tuple[int, int]:
    return ALL_DIRECTIONS[current_direction]


def parse_input(input_str: str) -> T:
    lines = input_str.split("\n")
    return [list(line) for line in lines]


def print_matrix(matrix: T) -> None:
    for row in matrix:
        print("".join(row))
    print()


def walk_till_exit(data: T, initial_pos: tuple[int, int]) -> True:
    data = copy.deepcopy(data)
    pos = initial_pos
    direction = (-1, 0)

    visited_cells: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    while True:
        data[pos[0]][pos[1]] = "X"
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos[0] > (len(data) - 1) or next_pos[1] > (len(data[0]) - 1) or next_pos[0] < 0 or next_pos[1] < 0:
            return False, data
        elif (pos, direction) in visited_cells:
            return True, data

        visited_cells.add((pos, direction))
        next_cell = data[next_pos[0]][next_pos[1]]
        if next_cell in {".", "X"}:
            pos = next_pos
        elif next_cell == "#":
            direction = get_next_direction(direction)
            continue


def get_initial_pos(data: T) -> tuple[int, int]:
    return [
        (y, x)
        for y, row in enumerate(data)
        for x, cell in enumerate(row)
        if cell == "^"
    ][0]


def puzzle_1(data: T) -> int:
    _, path_taken = walk_till_exit(data, get_initial_pos(data))

    return sum(
        [
            1 for row in path_taken
            for cell in row
            if cell == "X"
        ]
    )


def puzzle_2(data: T) -> int:
    # Super slow 41s... But it works
    initial_pos = get_initial_pos(data)
    _, path_taken = walk_till_exit(data, initial_pos)

    visited_cells = {
        (y, x)
        for y, row in enumerate(path_taken)
        for x, cell in enumerate(row)
        if cell == "X" and (y, x) != initial_pos
    }

    total = 0
    for i, pos in enumerate(visited_cells):
        modified_map = copy.deepcopy(data)
        modified_map[pos[0]][pos[1]] = "#"
        is_loop, _ = walk_till_exit(modified_map, initial_pos=initial_pos)
        total += is_loop

    return total


if __name__ == "__main__":
    run_solution_pretty(
        day=6,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

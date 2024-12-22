from functools import cache, partial
from itertools import permutations, pairwise

from utils import run_solution_pretty

EXAMPLE = """
029A
980A
179A
456A
379A
""".strip()

T = list[str]
C = tuple[int, int]

NUM_KEYBOARD: dict[str, C] = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

ARROW_KEYBOARD: dict[str, C] = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

ARROWS: dict[str, C] = {
    "^": (-1, +0),
    ">": (+0, +1),
    "v": (+1, +0),
    "<": (+0, -1),
}


def parse_input(input_str: str) -> T:
    return input_str.splitlines()


def passes_through_gap(start: str, path: str, num: bool) -> bool:
    keyboard = NUM_KEYBOARD if num else ARROW_KEYBOARD

    i, j = keyboard[start]
    for instruction in path:
        di, dj = ARROWS[instruction]
        i, j = i + di, j + dj

        if num and (i, j) == (3, 0):
            return True

        if not num and (i, j) == (0, 0):
            return True

    return False


@cache
def generate_paths(start: str, end: str, num: bool) -> set[str]:
    keyboard = NUM_KEYBOARD if num else ARROW_KEYBOARD

    start_pos = keyboard[start]
    end_pos = keyboard[end]

    di, dj = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    moves = "v" * di if di >= 0 else "^" * -di
    moves += ">" * dj if dj >= 0 else "<" * -dj

    combos = set(map("".join, permutations(moves)))
    combos = {
        combo + "A" for combo in combos if not passes_through_gap(start, combo, num)
    }
    return combos


@cache
def get_movements(start: str, end: str, num: bool, depth: int) -> int:
    if depth == 0:
        return min(map(len, generate_paths(start, end, False)))

    paths = generate_paths(start, end, num)
    best_count = 1 << 60
    for path in paths:
        count = sum(
            get_movements(a, b, num=False, depth=depth - 1)
            for a, b in pairwise("A" + path)
        )
        best_count = min(best_count, count)

    return best_count


def get_password_movements(password: str, n_robots: int) -> int:
    return sum(
        get_movements(a, b, num=True, depth=n_robots)
        for a, b in pairwise("A" + password)
    )


def puzzle(data: T, n_robots: int) -> int:
    return sum(
        get_password_movements(password, n_robots) * int(password[:-1])
        for password in data
    )


if __name__ == "__main__":
    run_solution_pretty(
        day=21,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=partial(puzzle, n_robots=2),
        puzzle_2=partial(puzzle, n_robots=25),
    )

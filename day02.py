from itertools import pairwise
from utils import run_solution_pretty

EXAMPLE = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()

T = list[list[int]]


def parse_input(input_str: str) -> T:
    return [list(map(int, line.split())) for line in input_str.split("\n")]


def is_safe(levels: list[int]) -> bool:
    diffs = [b - a for a, b in pairwise(levels)]
    all_same_direction = all(d > 0 for d in diffs) or all(d < 0 for d in diffs)
    valid_range = all(1 <= abs(d) <= 3 for d in diffs)
    return all_same_direction and valid_range


def variants_with_one_removed(levels: list[int]) -> list[list[int]]:
    return [levels[:i] + levels[i + 1:] for i in range(len(levels))]


def puzzle_1(data: T) -> int:
    return sum(is_safe(levels) for levels in data)


def puzzle_2(data: T) -> int:
    return sum(
        is_safe(levels) or any(is_safe(variant) for variant in variants_with_one_removed(levels))
        for levels in data
    )


if __name__ == "__main__":
    run_solution_pretty(
        day=2,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

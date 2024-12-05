from utils import run_solution_pretty
from itertools import pairwise

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
    lines = input_str.split("\n")
    return [list(map(int, line.split())) for line in lines]


def is_safe(row: list[int]) -> bool:
    diff = [x - y for x, y in pairwise(row)]
    rule1 = all(d > 0 for d in diff) or all(d < 0 for d in diff)
    rule2 = all(1 <= abs(d) <= 3 for d in diff)
    return rule1 and rule2


def remove_1(row: list[int]) -> list[list[int]]:
    return [
        row[:i] + row[i + 1:]
        for i in range(len(row))
    ]


def puzzle_1(data: T) -> int:
    return sum(is_safe(row) for row in data)


def puzzle_2(data: T) -> int:
    n_safe = 0
    for row in data:
        if is_safe(row):
            n_safe += 1
        else:
            for new_row in remove_1(row):
                if is_safe(new_row):
                    n_safe += 1
                    break

    return n_safe


if __name__ == "__main__":
    run_solution_pretty(
        day=2,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

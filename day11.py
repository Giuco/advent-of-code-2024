from collections import defaultdict
from functools import cache, partial

from utils import run_solution_pretty

EXAMPLE = """
125 17
""".strip()

T = list[int]


def parse_input(input_str: str) -> T:
    return list(map(int, input_str.split()))


@cache
def blink_stone(n: int) -> tuple[int, int]:
    s = str(n)
    if n == 0:
        re = (1, -1)
    elif len(s) % 2 == 0:
        re = (int(s[:len(s) // 2]), int(s[len(s) // 2:]))
    else:
        re = (n * 2024, -1)
    return re


def puzzle(data: T, n_blinks: int) -> int:
    count: defaultdict[int, int] = defaultdict(lambda: 0)
    for n in data:
        count[n] += 1

    for _ in range(n_blinks):
        new_count: defaultdict[int, int] = defaultdict(lambda: 0)

        for n, c in count.items():
            r1, r2 = blink_stone(n)
            new_count[r1] += c
            if r2 != -1:
                new_count[r2] += c

        count = new_count.copy()

    return sum(count.values())


if __name__ == "__main__":
    run_solution_pretty(
        day=11,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=partial(puzzle, n_blinks=25),
        puzzle_2=partial(puzzle, n_blinks=75),
    )

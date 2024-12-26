from collections import defaultdict, deque
from functools import cache
from pprint import pprint

from utils import run_solution_pretty

EXAMPLE = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".strip()

A = list[list[str]]
T = list[A]


def parse_input(input_str: str) -> T:
    pins = []
    for raw_pins in input_str.split("\n\n"):
        pins.append([list(x) for x in raw_pins.splitlines()])
    return pins


def single_convert_to_int(m: A) -> list[int]:
    t = []
    for i in range(len(m[0])):
        t.append([x[i] for x in m].count("#") - 1)
    return t


def convert_to_int(pins: T) -> tuple[list[list[int]], list[list[int]]]:
    keys, locks = [], []
    for pp in pins:
        if set(pp[0]) == {"#"}:
            locks.append(single_convert_to_int(pp))
        elif set(pp[-1]) == {"#"}:
            keys.append(single_convert_to_int(pp))
        else:
            raise ValueError("other")
    return keys, locks


def does_it_fit(key: list[int], lock: list[int]):
    for p1, p2 in zip(key, lock):
        if p1 + p2 > 5:
            return False
    return True


def puzzle_1(data: T) -> int:
    keys, locks = convert_to_int(data)
    ans = 0
    for key in keys:
        for lock in locks:
            if does_it_fit(key=key, lock=lock):
                ans += 1
    return ans


def puzzle_2(data: T) -> str:
    pass


if __name__ == "__main__":
    run_solution_pretty(
        day=25,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

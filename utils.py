import os
from pathlib import Path

BASE_PATH = Path(__file__).parent

from typing import Callable


def run_solution(
    day: int,
    parse_input: Callable,
    puzzle_1: Callable,
    puzzle_2: Callable,
    example: str,
) -> None:
    data = parse_input(get_input(day))
    example = parse_input(example.strip())

    print(f"Day {day}")
    print("Puzzle 1")
    print("Example:", puzzle_1(example))
    print("Result:", puzzle_1(data))

    print("Puzzle 2")
    print("Example:", puzzle_2(example))
    print("Result:", puzzle_2(data))


def run_solution_pretty(
    day: int,
    parse_input: Callable,
    puzzle_1: Callable,
    puzzle_2: Callable,
    example: str,
) -> None:
    """The same as above but better formatted and using colors"""
    data = parse_input(get_input(day))
    example = parse_input(example.strip())
    only_example = os.getenv("ONLY_EXAMPLE", "false").lower() == "true"


    print(f"\033[1mDay {day}\033[0m")
    print("\n", end="")
    print("\033[1mPuzzle 1\033[0m")
    print("\033[1mExample:\033[0m", puzzle_1(example))
    if not only_example:
        print("\033[1mResult:\033[0m", puzzle_1(data))

    print("\n", end="")
    print("\033[1mPuzzle 2\033[0m")
    print("\033[1mExample:\033[0m", puzzle_2(example))
    if not only_example:
        print("\033[1mResult:\033[0m", puzzle_2(data))


def get_input(day: int) -> str:
    with open(BASE_PATH / "data" / f"{day:02}.txt") as f:
        return f.read().strip()

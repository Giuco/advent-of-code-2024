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
    parse_input_1: Callable,
    puzzle_1: Callable,
    puzzle_2: Callable,
    example_1: str,
    parse_input_2: Callable = None,
    example_2: str = None,
) -> None:
    """The same as above but better formatted and using colors"""
    if parse_input_2 is None:
        parse_input_2 = parse_input_1

    data_1 = parse_input_1(get_input(day))
    data_2 = parse_input_2(get_input(day))
    example_1 = parse_input_1(example_1.strip())
    example_2 = parse_input_2(example_2.strip()) if example_2 else example_1
    only_example = os.getenv("ONLY_EXAMPLE", "false").lower() == "true"


    print(f"\033[1mDay {day}\033[0m")
    print("\n", end="")
    print("\033[1mPuzzle 1\033[0m")
    print("\033[1mExample:\033[0m", puzzle_1(example_1))
    if not only_example:
        print("\033[1mResult:\033[0m", puzzle_1(data_1))

    print("\n", end="")
    print("\033[1mPuzzle 2\033[0m")
    print("\033[1mExample:\033[0m", puzzle_2(example_2))
    if not only_example:
        print("\033[1mResult:\033[0m", puzzle_2(data_2))


def get_input(day: int) -> str:
    with open(BASE_PATH / "data" / f"{day:02}.txt") as f:
        return f.read().strip()

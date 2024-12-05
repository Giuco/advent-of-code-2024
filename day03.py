from dataclasses import dataclass
import re
from typing import Union

from utils import run_solution_pretty

EXAMPLE_1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".strip()
EXAMPLE_2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()


@dataclass
class Mul:
    x: int
    y: int


T = list[Union[Mul, bool]]


def parse_input_1(input_str: str) -> T:
    expr = r"mul\((\d{1,3}\,\d{1,3})\)"
    ops = []
    for op in re.findall(expr, input_str):
        x, y = op.split(",")
        ops.append(Mul(int(x), int(y)))
    return ops


def parse_input_2(input_str: str) -> T:
    expr = r"mul\((\d{1,3}\,\d{1,3})\)|(don\'t)|(do)"
    ops = []
    for op in re.findall(expr, input_str):
        if op[0]:
            x, y = op[0].split(",")
            ops.append(Mul(int(x), int(y)))
        elif op[1]:
            ops.append(False)
        elif op[2]:
            ops.append(True)
    return ops


def puzzle_1(data: T) -> int:
    return sum(op.x * op.y for op in data)


def puzzle_2(data: T) -> int:
    enabled = True
    total = 0
    for op in data:
        if isinstance(op, Mul):
            total += op.x * op.y if enabled else 0
        elif isinstance(op, bool):
            enabled = op
        else:
            raise ValueError(f"Invalid type: {type(op)}")
    return total


if __name__ == "__main__":
    run_solution_pretty(
        day=3,
        example_1=EXAMPLE_1,
        example_2=EXAMPLE_2,
        parse_input_1=parse_input_1,
        parse_input_2=parse_input_2,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

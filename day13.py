import re
from dataclasses import dataclass, replace

from utils import run_solution_pretty

EXAMPLE = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()


@dataclass
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]


T = list[Machine]


def parse_input(input_str: str) -> T:
    regex = r"Button A: X\+(\d+)\, Y\+(\d+)\nButton B: X\+(\d+)\, Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    matches = map(lambda x: x.groups(), re.finditer(regex, input_str, re.MULTILINE))
    parsed_machines: T = [
        Machine(
            button_a=(int(x1), int(y1)),
            button_b=(int(x2), int(y2)),
            prize=(int(x3), int(y3)),
        )
        for (x1, y1, x2, y2, x3, y3) in matches
    ]

    return parsed_machines


def solve(ax: int, bx: int, x: int, ay: int, by: int, y: int) -> float:
    return (ay * x - ax * y) / (ay * bx - ax * by)


def resolve_machine(machine: Machine) -> int | None:
    a = solve(
        machine.button_b[0], machine.button_a[0], machine.prize[0],
        machine.button_b[1], machine.button_a[1], machine.prize[1],
    )
    b = solve(
        machine.button_a[0], machine.button_b[0], machine.prize[0],
        machine.button_a[1], machine.button_b[1], machine.prize[1],
    )
    if a.is_integer() and b.is_integer():
        return int(a * 3 + b)
    else:
        return None


def puzzle_1(data: T) -> int:
    total_cost = 0
    for m in data:
        cost = resolve_machine(m)
        if cost:
            total_cost += cost

    return total_cost


def puzzle_2(data: T) -> int:
    to_add = 10_000_000_000_000
    data = [replace(m, prize=(m.prize[0] + to_add, m.prize[1] + to_add)) for m in data]
    return puzzle_1(data)


if __name__ == "__main__":
    run_solution_pretty(
        day=13,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

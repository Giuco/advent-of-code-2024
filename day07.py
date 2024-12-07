from itertools import product

from utils import run_solution_pretty

EXAMPLE = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()

T = dict[int, list[int]]


def parse_input(input_str: str) -> T:
    equations = {}
    for line in input_str.splitlines():
        test_value_str, numbers_str = line.split(": ")
        equations[int(test_value_str)] = list(map(int, numbers_str.strip().split(" ")))
    return equations


def evaluate(a: int, b: int, o: str) -> int:
    if o == "+":
        return a + b
    elif o == "*":
        return a * b
    elif o == "||":
        return int(str(a) + str(b))
    else:
        raise ValueError("Op not valid", o)


def evaluate_n(numbers: list[int], ops: list[str]) -> int:
    if len(numbers) != (len(ops) + 1):
        raise ValueError("Invalid number of ops")
    numbers = numbers.copy()
    total = numbers.pop(0)
    for op in ops:
        total = evaluate(total, numbers.pop(0), op)
    return total


def test_equation(
    expected_result: int, numbers: list[int], possible_ops: list[str]
) -> bool:
    possible_ops = product(possible_ops, repeat=len(numbers) - 1)
    for op_combination in possible_ops:
        if expected_result == evaluate_n(numbers, list(op_combination)):
            return True
    return False


def puzzle_1(data: T) -> int:
    total = 0
    for expected_result, numbers in data.items():
        if test_equation(expected_result, numbers, possible_ops=["*", "+"]):
            total += expected_result
    return total


def puzzle_2(data: T) -> int:
    total = 0
    for expected_result, numbers in data.items():
        if test_equation(expected_result, numbers, possible_ops=["*", "+", "||"]):
            total += expected_result
    return total


if __name__ == "__main__":
    run_solution_pretty(
        day=7,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

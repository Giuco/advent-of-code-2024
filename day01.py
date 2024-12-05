from collections import Counter

from utils import run_solution_pretty

EXAMPLE = """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip()


def parse_input(input_str: str) -> tuple[list[int], list[int]]:
    lines = input_str.split("\n")
    a = []
    b = []
    for line in lines:
        x, y = line.split()
        a.append(int(x))
        b.append(int(y))
    return a, b


def puzzle_1(data: tuple[list[int], list[int]]) -> int:
    total: int = 0
    for x, y in zip(sorted(data[0]), sorted(data[1])):
        total += abs(x - y)
    return total


def puzzle_2(data: tuple[list[int], list[int]]) -> int:
    freq = Counter(data[1])

    total: int = 0
    for x in data[0]:
        total += x * freq.get(x, 0)

    return total



if __name__ == "__main__":
    run_solution_pretty(
        day=1,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

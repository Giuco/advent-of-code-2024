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

T = tuple[list[int], list[int]]


def parse_input(input_str: str) -> T:
    pairs = [line.split() for line in input_str.split("\n")]
    left, right = zip(*pairs)
    return list(map(int, left)), list(map(int, right))


def puzzle_1(data: T) -> int:
    left, right = data
    return sum(abs(x - y) for x, y in zip(sorted(left), sorted(right)))


def puzzle_2(data: T) -> int:
    left, right = data
    freq = Counter(right)
    return sum(x * freq[x] for x in left)



if __name__ == "__main__":
    run_solution_pretty(
        day=1,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

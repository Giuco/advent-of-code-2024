from collections import Counter

from utils import run_solution_pretty

EXAMPLE_1 = """
1
10
100
2024
""".strip()

EXAMPLE_2 = """
1
2
3
2024
""".strip()

# EXAMPLE = "123"

T = list[int]


def parse_input(input_str: str) -> T:
    return list(map(int, input_str.splitlines()))


def get_next(n: int) -> int:
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n


def get_nn(n: int, i: int) -> int:
    for _ in range(i):
        n = get_next(n)
    return n


def count_sequences(secret_number: int) -> dict[tuple[int, int, int, int], int]:
    seqs: dict[tuple[int, int, int, int], int] = {}
    diffs: list[int] = []
    new_price = int(str(secret_number)[-1])

    for i in range(2000):
        secret_number = get_next(secret_number)

        old_price = new_price
        new_price = int(str(secret_number)[-1])
        diffs.append(new_price - old_price)

        if len(diffs) < 4:
            continue

        key = diffs[0], diffs[1], diffs[2], diffs[3]
        if key not in seqs:
            seqs[key] = new_price

        diffs.pop(0)

    return seqs


def puzzle_1(data: T) -> int:
    nums = []
    for n in data:
        nums.append(get_nn(n, 2000))
    return sum(nums)


def puzzle_2(data: T) -> int:
    psum = Counter()
    for number in data:
        psum += count_sequences(number)

    return max(psum.values())


if __name__ == "__main__":
    run_solution_pretty(
        day=22,
        example_1=EXAMPLE_1,
        example_2=EXAMPLE_2,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

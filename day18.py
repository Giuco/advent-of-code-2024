from collections import deque, defaultdict

from utils import run_solution_pretty

EXAMPLE = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()

T = list[tuple[int, int]]


def parse_input(input_str: str) -> T:
    parsed: T = []
    for row in input_str.splitlines():
        x, y = row.split(",")
        parsed.append((int(x), int(y)))
    return parsed


def puzzle_1(data: T, n: int | None = None) -> int:
    s = 6 if len(data) < 100 else 70
    if not n:
        n = 12 if len(data) < 100 else 1024

    corrupted: set[tuple[int, int]] = set(data[:n])
    end = s, s
    visited: dict[tuple[int, int], int] = defaultdict(lambda: s * s)
    to_visit: deque[tuple[int, int, int]] = deque([(0, 0, 0)])

    min_steps = s * s
    while to_visit:
        c, x, y = to_visit.popleft()
        if x < 0 or x > s or y < 0 or y > s:
            continue

        if c >= visited[(x, y)] or (x, y) in corrupted:
            continue

        if (x, y) == end and c < min_steps:
            min_steps = c

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            to_visit.append((c + 1, x + dx, y + dy))

        visited[(x, y)] = c

    return min_steps


def puzzle_2(data: T) -> str:
    s = 6 if len(data) < 100 else 70
    n = 0
    for n in range(len(data)):
        min_steps = puzzle_1(data, n)

        if min_steps == s * s:
            break

    x, y = data[n - 1]
    return f"{x},{y}"


if __name__ == "__main__":
    run_solution_pretty(
        day=18,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

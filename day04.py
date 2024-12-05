from utils import run_solution_pretty

EXAMPLE = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".strip()

T = list[list[str]]


def parse_input(input_str: str) -> T:
    lines = input_str.split("\n")
    return [list(line) for line in lines]


def count_xmas(m: T, x: int, y: int) -> int:
    horizontal_lr = m[y][x] + m[y][x + 1] + m[y][x + 2] + m[y][x + 3]
    horizontal_rl = m[y][x] + m[y][x - 1] + m[y][x - 2] + m[y][x - 3]

    vertical_ud = m[y][x] + m[y + 1][x] + m[y + 2][x] + m[y + 3][x]
    vertical_du = m[y][x] + m[y - 1][x] + m[y - 2][x] + m[y - 3][x]

    diagonal_ud_lr = m[y][x] + m[y + 1][x + 1] + m[y + 2][x + 2] + m[y + 3][x + 3]
    diagonal_du_rl = m[y][x] + m[y - 1][x - 1] + m[y - 2][x - 2] + m[y - 3][x - 3]

    diagonal_ud_rl = m[y][x] + m[y + 1][x - 1] + m[y + 2][x - 2] + m[y + 3][x - 3]
    diagonal_du_lr = m[y][x] + m[y - 1][x + 1] + m[y - 2][x + 2] + m[y - 3][x + 3]

    return sum(
        [
            horizontal_lr == "XMAS",
            horizontal_rl == "XMAS",
            vertical_ud == "XMAS",
            vertical_du == "XMAS",
            diagonal_ud_lr == "XMAS",
            diagonal_du_rl == "XMAS",
            diagonal_ud_rl == "XMAS",
            diagonal_du_lr == "XMAS",
        ]
    )


def check_cross_xmas(m: T, x: int, y: int) -> bool:
    combs = [
        ((-1, -1), (1, 1)),
        ((1, 1), (-1, -1)),
        ((-1, 1), (1, -1)),
        ((1, -1), (-1, 1)),
    ]

    chars: list[str] = [
        m[y + comb[0][0]][x + comb[0][1]] + "A" + m[y + comb[1][0]][x + comb[1][1]]
        for comb in combs
    ]
    return sum([char == "MAS" for char in chars]) == 2


def pad_matrix(m: T) -> T:
    for i in range(len(m)):
        m[i] = ["."] * 3 + m[i] + ["."] * 3

    m = [["."] * len(m[0])] * 3 + m + [["."] * len(m[0])] * 3
    return m


def puzzle_1(data: T) -> int:
    data = pad_matrix(data)
    n_xmas = 0
    for y in range(3, len(data) - 3):
        for x in range(3, len(data[0]) - 3):
            if data[y][x] == "X":
                n_xmas += count_xmas(data, x, y)
    return n_xmas


def puzzle_2(data: T) -> int:
    data = pad_matrix(data)
    n_xmas = 0
    for y in range(3, len(data) - 3):
        for x in range(3, len(data[0]) - 3):
            if data[y][x] == "A":
                n_xmas += check_cross_xmas(data, x, y)
    return n_xmas


if __name__ == "__main__":
    run_solution_pretty(
        day=4,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

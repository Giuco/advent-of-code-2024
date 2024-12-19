from functools import cache

from utils import run_solution_pretty

EXAMPLE = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()

T = tuple[tuple[str, ...], list[str]]


def parse_input(input_str: str) -> T:
    raw_towels, raw_designs = input_str.split("\n\n")
    towels = tuple(t.strip() for t in raw_towels.split(", "))
    designs = [d.strip() for d in raw_designs.splitlines()]
    return towels, designs


@cache
def get_n_designs_rec(design: str, towels: tuple[str]) -> int:
    if design == "":
        return 1

    return sum(
        get_n_designs_rec(design[len(tw):], towels)
            for tw in towels
            if design.startswith(tw)
    )


def puzzle_1(data: T) -> int:
    towels, designs = data
    return sum(
        1 for d in designs
            if get_n_designs_rec(d, towels) > 0
    )


def puzzle_2(data: T) -> int:
    towels, designs = data
    return sum(get_n_designs_rec(d, towels) for d in designs)


if __name__ == "__main__":
    run_solution_pretty(
        day=19,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

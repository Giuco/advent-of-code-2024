import copy
from itertools import pairwise

from utils import run_solution_pretty

EXAMPLE = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()

A = set[tuple[int, int]]
B = list[list[int]],

T = tuple[A, B]


def parse_input(input_str: str) -> T:
    part1, part2 = input_str.split("\n\n")

    part1_final = {
        (int(line.split("|")[0]), int(line.split("|")[1]))
        for line in part1.split("\n")
    }

    part2_final = [
        list(map(int, line.split(",")))
        for line in part2.split("\n")
    ]

    return part1_final, part2_final


def order_using_custom_order(rules: A, pages: list[int]) -> list[int]:
    pages = copy.deepcopy(pages)

    in_order = False
    while not in_order:
        in_order = True
        for i in range(len(pages) - 1):
            a, b = pages[i], pages[i + 1]

            if (b, a) in rules:
                pages[i], pages[i + 1] = b, a
                in_order = False

    return pages


def puzzle_1(data: T) -> int:
    rules, all_pages = data
    total = 0
    for pages in all_pages:
        ordered_pages = order_using_custom_order(rules, pages)

        if pages == ordered_pages:
            middle_page = pages[(len(pages) - 1) // 2]
            total += middle_page

    return total


def puzzle_2(data: T) -> int:
    rules, all_pages = data
    total = 0
    for pages in all_pages:
        ordered_pages = order_using_custom_order(rules, pages)

        if pages != ordered_pages:
            middle_page = ordered_pages[(len(ordered_pages) - 1) // 2]
            total += middle_page

    return total


if __name__ == "__main__":
    run_solution_pretty(
        day=5,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

from collections import defaultdict, deque
from functools import cache

from utils import run_solution_pretty

EXAMPLE = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()

T = list[tuple[str, str]]


def parse_input(input_str: str) -> T:
    return [(x.split("-")[0], x.split("-")[1]) for x in input_str.splitlines()]


def puzzle_1(data: T) -> int:
    mm: defaultdict[str, list[str]] = defaultdict(list)
    for a, b in data:
        mm[a].append(b)
        mm[b].append(a)

    @cache
    def find(connection: tuple[str, ...]) -> list[tuple[str, str, str]]:
        if len(connection) == 3:
            connection = sorted(connection)
            return [(connection[0], connection[1], connection[2])]

        total = []
        for ds in mm[connection[-1]]:
            if ds in connection:
                continue

            if len(connection) == 2 and ds not in mm[connection[-2]]:
                continue

            total.extend(find((*connection, ds)))

        return total

    all_connections: set[tuple[str, str, str]] = set()
    for key in mm.keys():
        all_connections.update(find((key,)))

    return len([x for x in all_connections if x[0].startswith("t") or x[1].startswith("t") or x[2].startswith("t")])


def puzzle_2(data: T) -> str:
    mm: defaultdict[str, set[str]] = defaultdict(set)
    for a, b in data:
        mm[a].add(b)
        mm[b].add(a)

    @cache
    def find(connection: tuple[str, ...]) -> tuple[str, ...]:
        connection = tuple(sorted(connection))
        new_connection = connection
        for ds in mm[connection[-1]]:
            if ds in connection:
                continue

            bad = False
            for cs in connection:
                if ds not in mm[cs]:
                    bad = True
                    continue
            if bad:
                continue

            new_connection = find((*connection, ds)) if len(find((*connection, ds))) > len(
                new_connection
            ) else new_connection

        return tuple(sorted(new_connection))

    all_connections: set[tuple[str, str, str]] = set()
    for i, key in enumerate(mm.keys()):
        all_connections.add(find((key,)))

    return ",".join(sorted(all_connections, key=len, reverse=True)[0])


if __name__ == "__main__":
    run_solution_pretty(
        day=23,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

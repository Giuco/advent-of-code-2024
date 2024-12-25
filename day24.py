from collections import defaultdict, deque
from functools import cache
from pprint import pprint

from utils import run_solution_pretty

EXAMPLE_1 = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""".strip()

EXAMPLE_2 = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
""".strip()

A = dict[str, bool]
B = list[tuple[str, str, str, str]]
T = tuple[A, B]


def parse_input(input_str: str) -> T:
    raw_registers, raw_instructions = input_str.split("\n\n")
    registers: A = {}
    for rr in raw_registers.splitlines():
        key, raw_value = rr.split(": ")
        registers[key] = raw_value == "1"

    instructions: B = []
    for ins in raw_instructions.splitlines():
        a, b, c, _, e = ins.split(" ")
        instructions.append((a, b, c, e))

    return registers, instructions


def get_number(letter: str, registers: A) -> int:
    zkeys = sorted((z for z in registers.keys() if z.startswith(letter)), reverse=True)
    raw_ans = ""
    for key in zkeys:
        raw_ans += "1" if registers[key] else "0"

    return int(raw_ans, 2)


def puzzle_1(data: T) -> int:
    registers, instructions = data
    q = deque(instructions)

    while q:
        a, op, b, c = q.popleft()
        if a not in registers or b not in registers:
            q.append((a, op, b, c))
            continue

        if op == "AND":
            registers[c] = registers[a] and registers[b]
        elif op == "OR":
            registers[c] = registers[a] or registers[b]
        elif op == "XOR":
            registers[c] = registers[a] ^ registers[b]
        else:
            raise ValueError("op not valid")

    return get_number('z', registers)


def puzzle_2(data: T) -> str:
    pass


if __name__ == "__main__":
    run_solution_pretty(
        day=24,
        example_1=EXAMPLE_1,
        example_2=EXAMPLE_1,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

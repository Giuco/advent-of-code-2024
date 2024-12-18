from collections import deque
from collections.abc import Callable
from functools import cache
from itertools import batched
from multiprocessing.reduction import register

from black.trans import defaultdict

from utils import run_solution_pretty

EXAMPLE = """
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()

Registers = tuple[int, int, int]
Outputs = list[int]
T = tuple[Registers, list[int]]


def parse_input(input_str: str) -> T:
    raw_registers, raw_instructions = input_str.split("\n\n")
    registers: dict[str, int] = {}
    for rr in raw_registers.splitlines():
        key = rr.strip().split(" ")[1].replace(":", "").strip()
        value = int(rr.strip().split(" ")[-1])
        registers[key] = value

    instructions: list[int] = []
    for ri in raw_instructions.split(" ")[1].strip().split(","):
        instructions.append(int(ri))

    return (registers["A"], registers["B"], registers["C"]), instructions


@cache
def get_value(operand: int, registers: Registers) -> int:
    if operand in {0, 1, 2, 3}:
        return operand
    elif operand == 4:
        return registers[0]
    elif operand == 5:
        return registers[1]
    elif operand == 6:
        return registers[2]
    else:
        raise ValueError(f"value not valid: {operand=}, {registers=}")


def adv(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    numerator = registers[0]
    denominator = 2 ** get_value(operand, registers)
    result = int(numerator / denominator)

    registers = (result, registers[1], registers[2])
    return registers, [], ip + 2


def bxl(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    registers = (registers[0], registers[1] ^ operand, registers[2])
    return registers, [], ip + 2


def bst(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    v = get_value(operand, registers) % 8
    registers = (registers[0], v, registers[2])
    return registers, [], ip + 2


def jnz(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    if registers[0] == 0:
        return registers, [], ip + 2

    return registers, [], operand


def bxc(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    registers = (registers[0], registers[1] ^ registers[2], registers[2])
    return registers, [], ip + 2


def out(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    combo = get_value(operand, registers) % 8
    return registers, [combo], ip + 2


def bdv(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    numerator = registers[0]
    denominator = 2 ** get_value(operand, registers)
    result = int(numerator / denominator)

    registers = (registers[0], result, registers[2])
    return registers, [], ip + 2


def cdv(operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    numerator = registers[0]
    denominator = 2 ** get_value(operand, registers)
    result = int(numerator / denominator)

    registers = (registers[0], registers[1], result)
    return registers, [], ip + 2


def rr(instruction: int, operand: int, registers: Registers, ip: int) -> tuple[Registers, Outputs, int]:
    return INSTRUCTIONS[instruction](operand, registers, ip)


InstructionFn = Callable[[int, Registers, int], tuple[Registers, Outputs, int]]

INSTRUCTIONS: dict[int, InstructionFn] = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def puzzle_1(data: T) -> str:
    registers, instructions = data
    outputs: list[int] = []
    ip = 0

    print("Start")
    print(f"Registers: {registers}")
    print(f"Outputs: {outputs}")

    while ip < len(instructions):
        instruction, operand = instructions[ip], instructions[ip + 1]
        print(f"\nInstruction: {ip=}. {instruction=}, {operand=}")

        registers, new_outputs, ip = rr(
            instruction=instruction, operand=operand, registers=registers, ip=ip
        )
        outputs.extend(new_outputs)
        print(f"Registers: {registers}")
        print(f"Outputs: {outputs}")

    return ",".join(map(str, outputs))


def puzzle_2(data: T) -> int:
    original_registers, instructions = data
    expected_output = ",".join(map(str, instructions))
    a = 0
    while True:
        print("This doesn't work for real input")
        actual_output = puzzle_1(((a, original_registers[1], original_registers[2]), instructions.copy()))
        if actual_output == expected_output:
            break
        a += 1

    return a


if __name__ == "__main__":
    run_solution_pretty(
        day=17,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

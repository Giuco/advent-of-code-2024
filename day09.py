from itertools import repeat

from utils import run_solution_pretty

EXAMPLE = """
2333133121414131402
""".strip()

T = list[int]


def parse_input(input_str: str) -> T:
    return [int(x) for x in input_str.strip()]


def print_blocks(data: T) -> None:
    print("".join(map(lambda x: "." if x == -1 else str(x), data)))


def explode_blocks(data: T) -> T:
    new_blocks = []
    for i, b in enumerate(data):
        if i % 2 == 0:
            new_blocks.extend([i // 2] * b)
        else:
            new_blocks.extend([-1] * b)
    return new_blocks


def puzzle_1(data: T) -> int:
    blocks = explode_blocks(data)

    l = 0
    r = len(blocks) - 1
    while r > l:
        if blocks[l] != -1:
            l += 1
        elif blocks[r] == -1:
            r -= 1
        else:
            blocks[l], blocks[r] = blocks[r], blocks[l]

    return sum(i * b for i, b in enumerate(blocks) if b != -1)


def puzzle_2(data: T) -> int:
    blocks: list[tuple[int, int]] = []
    for i, s in enumerate(data):
        file_id = i // 2 if i % 2 == 0 else -1
        blocks.append((file_id, s))

    r = len(blocks) - 1
    l = 0
    while r >= 0:
        (r_id, r_size), (l_id, l_size) = blocks[r], blocks[l]

        if r_id == -1 or l >= r:
            r -= 1
            l = 0
            # If the size of the file is 1, and it couldn't find any empty space, it means there's no more empty space to
            # to move things. So it can finish early.
            if r_size == 1 and r_id != -1:
                break
        elif l_id == -1 and r_size == l_size:
            blocks[r], blocks[l] = blocks[l], blocks[r]
            r -= 1
            l = 0
        elif l_id == -1 and l_size > r_size:
            blocks[r] = (-1, r_size)
            blocks[l] = (r_id, r_size)
            blocks.insert(l + 1, (-1, l_size - r_size))
            l = 0
        else:
            l += 1

    return sum(i * b for i, b in enumerate(gen(blocks)) if b != -1)


def gen(blocks: list[tuple[int, int]]) -> T:
    for block_id, block_size in blocks:
        yield from repeat(block_id, block_size)


if __name__ == "__main__":
    run_solution_pretty(
        day=9,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )

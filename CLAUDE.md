# CLAUDE.md - AI Assistant Guide for Advent of Code 2024

This document provides comprehensive guidance for AI assistants working with this Advent of Code 2024 solutions repository.

## Repository Overview

This repository contains Python solutions for Advent of Code 2024. All 25 days have been completed with both Part 1 and Part 2 solutions.

**Key Facts:**
- Language: Python 3.12+ (pyproject.toml requirement, but 3.11+ works)
- Solutions: 25 completed days (day01.py through day25.py)
- Input Data: Stored in `data/` directory as `{01-25}.txt`
- No external dependencies (standard library only)

## Project Structure

```
advent-of-code-2024/
├── day01.py              # Day 1 solution
├── day02.py              # Day 2 solution
├── ...                   # Days 3-24
├── day25.py              # Day 25 solution
├── utils.py              # Shared helper functions
├── data/
│   ├── 01.txt           # Day 1 input
│   ├── 02.txt           # Day 2 input
│   └── ...              # Days 3-25 inputs
├── pyproject.toml        # Project metadata
├── .gitignore           # Standard Python gitignore
└── README.md            # (Empty currently)
```

## Code Structure & Conventions

### Standard Solution File Pattern

Every `dayXX.py` file follows this consistent structure:

```python
from collections import ...  # Standard library imports as needed
from utils import run_solution_pretty

EXAMPLE = """
<example input text>
""".strip()

# Type aliases for clarity
T = <main_data_type>      # e.g., list[list[int]]
A = <helper_type>         # Optional additional types
B = <helper_type>         # Optional additional types

def parse_input(input_str: str) -> T:
    """Parse the input string into the data structure needed for solving."""
    # Convert input string to appropriate data structure
    return data

def puzzle_1(data: T) -> int | str:
    """Solve part 1 of the puzzle."""
    # Solution logic
    return result

def puzzle_2(data: T) -> int | str:
    """Solve part 2 of the puzzle."""
    # Solution logic
    return result

# Optional helper functions
def helper_function(...):
    """Helper functions as needed."""
    pass

if __name__ == "__main__":
    run_solution_pretty(
        day=XX,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )
```

### Key Conventions

1. **Type Aliases**: Use single-letter type aliases (T, A, B, etc.) at module level for complex types
   ```python
   T = list[list[int]]           # Main data type
   A = list[list[str]]           # Grid type
   B = list[tuple[int, int]]     # Coordinates list
   ```

2. **EXAMPLE Constant**: Always use `.strip()` on multiline example strings
   ```python
   EXAMPLE = """
   line 1
   line 2
   """.strip()
   ```

3. **Parsing Functions**:
   - Always named `parse_input` with signature `(input_str: str) -> T`
   - Returns the data structure expected by puzzle functions
   - Handles newline splitting, type conversion, and structure building

4. **Puzzle Functions**:
   - Named `puzzle_1` and `puzzle_2`
   - Accept parsed data as input: `(data: T) -> int | str`
   - Return the final answer (usually int, sometimes str)

5. **Helper Functions**: Common patterns include:
   - `print_grid(grid: A) -> None` - Visual debugging
   - `find_X(data: T) -> list[...]` - Search functions
   - `is_inside(grid: A, pos: tuple) -> bool` - Boundary checks
   - Grid navigation helpers

### Common Imports

```python
# Most frequently used
from collections import Counter, defaultdict, deque
from functools import cache, lru_cache
from itertools import combinations, permutations, product
import copy
from operator import itemgetter
from pprint import pprint

# Always required
from utils import run_solution_pretty
```

## The `utils.py` Module

### `run_solution_pretty()` Function

The main entry point for running solutions with automatic testing and formatting.

**Signature:**
```python
def run_solution_pretty(
    day: int,
    parse_input_1: Callable,
    puzzle_1: Callable,
    puzzle_2: Callable,
    example_1: str,
    parse_input_2: Callable = None,  # Defaults to parse_input_1
    example_2: str = None,            # Defaults to example_1
) -> None
```

**Behavior:**
- Runs puzzle_1 and puzzle_2 on both example and real input
- Prints results with ANSI color formatting (bold for labels)
- Respects `ONLY_EXAMPLE=true` environment variable (skips real input)
- Automatically loads real input from `data/{day:02}.txt`
- Supports different parsers/examples for part 2 if needed

**Output Format:**
```
Day XX

Puzzle 1
Example: <result>
Result: <result>

Puzzle 2
Example: <result>
Result: <result>
```

### `get_input()` Function

Reads input data from the data directory.

```python
def get_input(day: int) -> str:
    """Returns stripped contents of data/{day:02}.txt"""
```

## Running Solutions

### Standard Execution
```bash
python day01.py
```

### Example-Only Mode
```bash
ONLY_EXAMPLE=true python day01.py
```

This mode is useful for:
- Testing during development
- Verifying logic without waiting for full input processing
- Debugging with smaller, known datasets

## Common Patterns & Idioms

### Grid Parsing
```python
def parse_input(input_str: str) -> list[list[str]]:
    return [list(line) for line in input_str.split("\n")]
```

### Integer Grid Parsing
```python
def parse_input(input_str: str) -> list[list[int]]:
    return [
        [int(c) if c != "." else -1 for c in line]
        for line in input_str.split("\n")
    ]
```

### Multi-Section Input
```python
def parse_input(input_str: str) -> tuple[A, B]:
    section1, section2 = input_str.split("\n\n")
    # Parse each section independently
    return parsed_section1, parsed_section2
```

### Grid Navigation (4-direction)
```python
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

def search_neighbours(grid: list[list], i: int, j: int) -> list[tuple[int, int]]:
    neighbors = []
    for di, dj in DIRECTIONS:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            neighbors.append((ni, nj))
    return neighbors
```

### BFS/DFS with Deque
```python
from collections import deque

def solve_bfs(start: tuple[int, int], grid: list[list]) -> int:
    q = deque([start])
    visited = {start}

    while q:
        pos = q.popleft()
        # Process position
        for neighbor in get_neighbors(pos):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return result
```

### Memoization
```python
from functools import cache

@cache
def recursive_solution(state: tuple) -> int:
    # Use immutable types (tuples, frozensets) for cache
    return result
```

### Deep Copying for Simulation
```python
import copy

def puzzle_1(data: T) -> int:
    data = copy.deepcopy(data)  # Prevent mutations
    # Simulate changes to data
    return result
```

## Development Workflow

### When Adding New Solutions

1. **Create the file**: Follow the naming pattern `dayXX.py` (zero-padded)
2. **Add input data**: Place puzzle input in `data/XX.txt`
3. **Start with template**: Copy structure from any existing day
4. **Test with example**: Implement with `EXAMPLE` first
5. **Verify**: Run with `ONLY_EXAMPLE=true` until example passes
6. **Run full solution**: Execute normally to solve with real input

### When Debugging Solutions

1. **Add print helpers**: Create `print_grid()` or similar visualization functions
2. **Use pprint**: `from pprint import pprint` for complex structures
3. **Test incrementally**: Use example input first, then real input
4. **Add assertions**: Validate intermediate steps with known values
5. **Simplify input**: Test with minimal cases from examples

### When Refactoring

1. **Preserve public API**: Don't change `parse_input`, `puzzle_1`, `puzzle_2` signatures
2. **Extract helpers**: Move repeated logic to helper functions
3. **Update type hints**: Keep type aliases accurate
4. **Test after changes**: Verify output hasn't changed

## Type Hints

Type hints are used consistently throughout the codebase:

```python
# Simple types
def puzzle_1(data: list[int]) -> int:
    pass

# Complex types with aliases
T = tuple[list[list[str]], list[tuple[int, int]]]

def parse_input(input_str: str) -> T:
    pass

# Union types for return values
def puzzle_2(data: T) -> int | str:
    pass
```

## Git Workflow

### Current Branch Structure
- **Development branches**: Follow pattern `claude/claude-md-{session-id}`
- **Main branch**: (not specified in current context)

### Committing Changes

When making commits:
1. Follow conventional commit format
2. Be descriptive about which day/feature is affected
3. Example: `"day 25"`, `"day 24 part 2"`, `"day 17 part 2"`

### Common Git Operations

```bash
# Check status
git status

# Add and commit
git add dayXX.py data/XX.txt
git commit -m "day XX"

# Push to branch
git push -u origin <branch-name>
```

## Special Considerations

### Day 24 Note
Day 24 Part 2 contains a solution adapted from Reddit (see comment in day24.py:131). This is explicitly noted in the code.

### Day 25 Note
Day 25 Part 2 returns a string instead of int (puzzle_2 just passes).

### No External Dependencies
This repository intentionally uses only Python standard library. Avoid suggesting external packages like numpy, pandas, networkx, etc.

### Performance Considerations
- Some solutions process large inputs (see day 15, 16)
- Use `@cache` decorator for recursive solutions (day 11, 19)
- Deep copying is acceptable for simulation problems (day 15, 24)
- Deque is preferred over list for BFS operations

## Testing

There is no formal test framework. Testing is done via:
1. **Example verification**: Each solution runs example input automatically
2. **Manual verification**: Compare output against Advent of Code website
3. **Example-only mode**: `ONLY_EXAMPLE=true` for rapid iteration

## Code Style

### Follows these conventions:
- **Line length**: Generally reasonable (no strict limit observed)
- **Indentation**: 4 spaces
- **Imports**: Standard library grouped, then utils
- **Naming**:
  - snake_case for functions and variables
  - UPPER_CASE for constants (EXAMPLE, DIRECTIONS)
  - Single capital letters for type aliases (T, A, B)
- **Docstrings**: Minimal (function signatures are self-documenting)
- **Comments**: Used sparingly, mainly for complex algorithms

### Do NOT:
- Add unnecessary comments or docstrings
- Reformat existing working code
- Add type hints to existing code without type hints
- Add external dependencies
- Create helper modules or packages
- Add configuration files (pytest, mypy, etc.)

## AI Assistant Guidelines

### When Asked to Add a New Day:

1. **Read existing day files** to match style
2. **Follow the exact template** shown in "Standard Solution File Pattern"
3. **Use appropriate type aliases** (T, A, B, etc.)
4. **Include EXAMPLE constant** with test data
5. **Implement parse_input, puzzle_1, puzzle_2** functions
6. **Add helper functions** only if needed for clarity
7. **Test with ONLY_EXAMPLE** mode first

### When Asked to Debug:

1. **Read the entire file** before suggesting changes
2. **Run the solution** to see actual output
3. **Check example output** first - if that's wrong, the logic is wrong
4. **Add temporary print statements** for debugging
5. **Verify against problem description** (ask user if unclear)

### When Asked to Optimize:

1. **Profile first** - don't optimize prematurely
2. **Consider algorithmic improvements** before micro-optimizations
3. **Use @cache** for expensive recursive calls
4. **Use appropriate data structures** (set for membership, deque for BFS)
5. **Keep code readable** - don't sacrifice clarity for minor gains

### When Asked to Explain:

1. **Reference specific line numbers** (e.g., "day15.py:87")
2. **Explain algorithm** not just code
3. **Point out key data structures** and why they were chosen
4. **Mention time/space complexity** if relevant

## Quick Reference

### File Template
```python
from utils import run_solution_pretty

EXAMPLE = """...""".strip()

T = <type>

def parse_input(input_str: str) -> T:
    return data

def puzzle_1(data: T) -> int:
    return result

def puzzle_2(data: T) -> int:
    return result

if __name__ == "__main__":
    run_solution_pretty(
        day=X,
        example_1=EXAMPLE,
        parse_input_1=parse_input,
        puzzle_1=puzzle_1,
        puzzle_2=puzzle_2,
    )
```

### Essential Commands
```bash
# Run solution
python dayXX.py

# Run with example only
ONLY_EXAMPLE=true python dayXX.py

# Check git status
git status

# Commit changes
git add . && git commit -m "descriptive message"
```

### Common Mistakes to Avoid
- Forgetting `.strip()` on EXAMPLE strings
- Using 0-indexing when problem uses 1-indexing
- Mutating shared data structures between part 1 and part 2
- Not handling edge cases present in examples
- Inefficient algorithms that work on examples but timeout on real input

## Summary

This repository is a clean, well-structured implementation of Advent of Code 2024 solutions. The consistent patterns make it easy to:
- Add new solutions
- Debug existing code
- Understand algorithms at a glance
- Test with examples before running full input

When working with this codebase, prioritize consistency with existing patterns over introducing new conventions or optimizations.

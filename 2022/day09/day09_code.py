import argparse
import sys
from pathlib import Path
from typing import Any, Callable, List, Literal, Sequence, Set, Tuple, TypeVar
from unicodedata import digit

###########################################################################
############################### Setup #####################################
###########################################################################
sys.path.append(Path(__file__).parent.parent.as_posix())
import lib

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "--input", "-i", help="Input file path.", type=Path, required=False
)
arg_parser.add_argument(
    "--part",
    "-p",
    type=int,
    default=(1, 2),
    choices=(1, 2),
    nargs=1,
    help="Run part 1 or 2",
    required=False,
)
arg_parser.add_argument(
    "--puzzle",
    "-a",
    help="Use real puzzle data.",
    default=False,
    action="store_true",
    required=False,
)
arg_parser.add_argument(
    "--debug",
    help="Debug mode.",
    default=False,
    action="store_true",
    required=False,
)
args, _ = arg_parser.parse_known_args(sys.argv)

args, _ = arg_parser.parse_known_args(sys.argv)

ParsedInput = TypeVar("ParsedInput")


def get_input(
    parse: Callable[[str], ParsedInput], puzzle: bool = False
) -> List[ParsedInput]:
    data: List[ParsedInput] = []
    if args.input:
        filename = Path(args.input)
    else:
        filename = Path(__file__).parent / f'input{"" if puzzle else "_test"}.txt'
        if not filename.exists():
            print(f"[Warning] {filename.absolute()} does not exists.")
            print(
                f"[Info] Defaulting to {filename.parent / 'input_test.txt'} for input."
            )
            print("-" * 42)
            filename = Path(__file__).parent / "input_test.txt"

    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def debug_print(*s: Any):
    if args.debug:
        print(*s)


###########################################################################

################################################################################
############################### Start of Part 1 ################################
################################################################################
def parse1(line: str):
    direction, steps = line.split()
    return direction, int(steps)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def is_touching(h, t):
    for x in range(h[0] - 1, h[0] + 2):
        for y in range(h[1] - 1, h[1] + 2):
            if t == [x, y]:
                return True
    return False


def print_grid(h, t, width=30):
    if not args.debug:
        return
    print("=" * 23)
    for y in reversed(range(-1 * width, width)):
        for x in range(-1 * width, width):
            if h == [x, y]:
                print("H", end="")
            elif t == [x, y]:
                print("T", end="")
            elif [x, y] == [0, 0]:
                print("s", end="")
            else:
                print(".", end="")
        print("", str(y).zfill(2))


################################################################################
def day09p1():
    data = get_input(parse1, args.puzzle)
    t_pos = [0, 0]
    h_pos = [0, 0]
    dimension = 0
    direction = 0
    visited = set()
    print_grid(h_pos, t_pos, 5)
    for d, s in data:
        debug_print(d, s)
        if d == "U" or d == "D":
            dimension = 1  # Y
        else:
            dimension = 0  # X

        if d == "U" or d == "R":
            direction = 1
        else:
            direction = -1

        for _ in range(s):
            h_pos[dimension] += direction

            if not is_touching(h_pos, t_pos):
                if h_pos[0] == t_pos[0] or h_pos[1] == t_pos[1]:
                    t_pos[dimension] += direction
                else:
                    t_pos[dimension] += direction
                    other_dim = int(not dimension)
                    t_pos[other_dim] += h_pos[other_dim] - t_pos[other_dim]

            visited.add(tuple(t_pos))

            print_grid(h_pos, t_pos, 5)
            debug_print(h_pos, t_pos)

    return len(visited)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def print_snake(knots: List[List[int]]):
    if not args.debug:
        return
    print("=" * 23)

    min_x = min(knots, key=lambda x: x[0])[0]
    max_x = max(knots, key=lambda x: x[0])[0]
    min_y = min(knots, key=lambda x: x[1])[1]
    max_y = max(knots, key=lambda x: x[1])[1]

    for y in reversed(range(min_y - 1, max_y + 2)):
        for x in range(min_x - 1, max_x + 2):
            p = False
            for i, k in enumerate(knots):
                if k == [x, y]:
                    if i == 0:
                        p = True
                        print("H", end="")
                        break
                    else:
                        p = True
                        print(i, end="")
                        break
            if not p:
                if [x, y] == [0, 0]:
                    print("s", end="")
                else:
                    print(".", end="")
        print()


def print_visited(visited: Set[Tuple[int, int]]):
    if not args.debug:
        return
    print("Debug Visited:")
    min_x = min(visited, key=lambda x: x[0])[0]
    max_x = max(visited, key=lambda x: x[0])[0]
    min_y = min(visited, key=lambda x: x[1])[1]
    max_y = max(visited, key=lambda x: x[1])[1]

    for y in reversed(range(min_y - 1, max_y + 2)):
        for x in range(min_x - 1, max_x + 2):
            if (x, y) == (0, 0):
                print("s", end="")
            elif (x, y) in visited:
                print("#", end="")
            else:
                print(".", end="")
        print()


def move_towards(h, t):
    if h[0] == t[0]:
        t[1] += 1 if h[1] - t[1] > 0 else -1
    elif h[1] == t[1]:
        t[0] += 1 if h[0] - t[0] > 0 else -1
    else:
        t[0] += 1 if h[0] - t[0] > 0 else -1
        t[1] += 1 if h[1] - t[1] > 0 else -1
    return t


################################################################################
def day09p2():
    data = get_input(parse2, args.puzzle)
    heads = [[0, 0] for _ in range(10)]
    dimension = 0
    direction = 0

    visited = set()
    visited.add((0, 0))
    for d, s in data:
        debug_print("Move:", d, s)
        if d == "U" or d == "D":
            dimension = 1  # Y
        else:
            dimension = 0  # X

        if d == "U" or d == "R":
            direction = 1
        else:
            direction = -1

        for _ in range(s):
            heads[0][dimension] += direction
            for i in range(1, len(heads)):
                h_pos = heads[i - 1]
                t_pos = heads[i]
                if not is_touching(h_pos, t_pos):
                    move_towards(h_pos, t_pos)
            visited.add(tuple(heads[-1]))

        print_snake(heads)

    print_visited(visited)
    return len(visited)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 09 - Part 1", "-" * n)
        print("Result =>", day09p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 09 - Part 2", "-" * n)
        print("Result =>", day09p2())
    print()


main()

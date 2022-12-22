import argparse
import sys
from collections import deque
from pathlib import Path
from typing import Any, Callable, List, Set, Tuple, TypeVar

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
    return lib.convert_to_int(line.split(","))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_nb(x, y, z):
    nb = []
    for nx in [x - 1, x + 1]:
        nb.append((nx, y, z))
    for ny in [y - 1, y + 1]:
        nb.append((x, ny, z))
    for nz in [z - 1, z + 1]:
        nb.append((x, y, nz))
    return nb


################################################################################
def day18p1():
    cubes = get_input(parse1, args.puzzle)
    cubes = set(cubes)

    open_sides = {}
    for cube in cubes:
        open_sides[cube] = 6
        for nx, ny, nz in get_nb(*cube):
            if (nx, ny, nz) == cube:
                continue
            if (nx, ny, nz) in cubes:
                open_sides[cube] -= 1
    debug_print(open_sides)
    return sum(open_sides.values())


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


IN = set()
OUT = set()


def reaches_out(pos: Tuple[int, int, int], cubes):
    if pos in OUT:
        return True
    if pos in IN:
        return False

    to_visit = [(pos, int(0))]
    visited: Set[Tuple[int, int, int]] = set()

    while len(to_visit) > 0:
        c, path = to_visit.pop()

        if c in OUT:
            OUT.update(visited)
            return True

        if c in cubes:
            continue

        if c in visited:
            continue

        visited.add(c)

        if path > 700:
            OUT.update(visited)
            return True

        for nb in get_nb(*c):
            to_visit.append((nb, path + 1))

    IN.update(visited)
    return False


################################################################################
def day18p2():
    cubes = get_input(parse2, args.puzzle)
    cubes = set(cubes)
    ans = 0
    for cube in cubes:
        for nx, ny, nz in get_nb(*cube):
            if reaches_out((nx, ny, nz), cubes):
                ans += 1
    return ans


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 18 - Part 1", "-" * n)
        print("Result =>", day18p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 18 - Part 2", "-" * n)
        print("Result =>", day18p2())
    print()


main()

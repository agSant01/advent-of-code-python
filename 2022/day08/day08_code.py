import argparse
import sys
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Any, Callable, List, TypeVar

###########################################################################
############################### Setup #####################################
###########################################################################
sys.path.append(Path(__file__).parent.parent.as_posix())

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
def parse1(line: str) -> List[int]:
    return list(map(int, line))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_nbs(x, y, directions=["R", "L", "U", "D"]):
    nbs = []
    if "L" in directions:
        nbs.append(((x - 1, y), "L"))
    if "R" in directions:
        nbs.append(((x + 1, y), "R"))
    if "D" in directions:
        nbs.append(((x, y - 1), "D"))
    if "U" in directions:
        nbs.append(((x, y + 1), "U"))
    return nbs


################################################################################
def day08p1():
    data = get_input(parse1, args.puzzle)
    h = len(data)
    w = len(data[0])
    is_visible = set()

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            value = data[y][x]
            to_visit = get_nbs(x, y)
            visited = set()
            while len(to_visit) > 0:
                nb, direction = to_visit.pop()

                if nb in visited:
                    continue

                visited.add(nb)

                if data[nb[1]][nb[0]] >= value:
                    continue

                if (
                    nb[0] == 0
                    or nb[1] == 0
                    or nb[0] == len(data[0]) - 1
                    or nb[1] == len(data) - 1
                ):
                    if data[nb[1]][nb[0]] < value:
                        is_visible.add((x, y))
                    break

                for nb in get_nbs(nb[0], nb[1], [direction]):
                    if nb not in visited:
                        to_visit.append(nb)

    edges_count = len(data) * 2 + len(data[0]) * 2 - 4
    debug_print(is_visible)
    return len(is_visible) + edges_count


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def get_scenic_score(data: List[List[int]], x: int, y: int):
    value = data[y][x]
    to_visit = get_nbs(x, y)
    scores = []

    while len(to_visit) > 0:
        nb, direction = to_visit.pop()

        if nb[0] == 0 or nb[0] >= len(data[0]) - 1:
            scores.append(abs(x - nb[0]))
            continue
        if nb[1] == 0 or nb[1] >= len(data) - 1:
            scores.append(abs(y - nb[1]))
            continue

        if data[nb[1]][nb[0]] >= value:
            if direction == "R" or direction == "L":
                scores.append(abs(x - nb[0]))
            else:
                scores.append(abs(y - nb[1]))
            continue

        for nb in get_nbs(nb[0], nb[1], [direction]):
            to_visit.append(nb)

    if len(scores) < 4:
        return 0

    return reduce(mul, scores, 1)


################################################################################
def day08p2():
    data = get_input(parse2, args.puzzle)
    h = len(data)
    w = len(data[0])
    scores = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            ss = get_scenic_score(data, x, y)
            debug_print((x, y), ss)
            scores.append(ss)
    return max(scores)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 08 - Part 1", "-" * n)
        print("Result =>", day08p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 08 - Part 2", "-" * n)
        print("Result =>", day08p2())
    print()


main()

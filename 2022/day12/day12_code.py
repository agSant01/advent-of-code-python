import argparse
import sys
from pathlib import Path
from typing import Any, Callable, List, NamedTuple, Set, Tuple, TypeVar, Union
from unittest import result

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
arg_parser.add_argument(
    "--map",
    help="Print trail of elves of topology",
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
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_neighbors(data: List[str]):
    def _get_neighbor(coordinate):
        nbs = []
        for x, y in (
            (coordinate[0], coordinate[1] + 1),
            (coordinate[0], coordinate[1] - 1),
            (coordinate[0] + 1, coordinate[1]),
            (coordinate[0] - 1, coordinate[1]),
        ):
            if x < 0 or y < 0 or x >= len(data[0]) or y >= len(data):
                continue
            next_value = data[y][x]
            if next_value == "S":
                next_value = "a"
            elif next_value == "E":
                next_value = "z"
            if (
                ord(data[coordinate[1]][coordinate[0]].lower())
                >= ord(next_value.lower()) - 1
            ):
                nbs.append((x, y))
        return nbs

    return _get_neighbor


def print_map(result: lib.ToVisit, end_coord):
    trail = set(result.trail)
    max_x = max(trail, key=lambda p: p[0])[0]
    max_y = max(trail, key=lambda p: p[1])[1]
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in trail:
                print("#", end="")
            elif (x, y) == end_coord:
                print("E", end="")
            else:
                print(".", end="")
        print()


################################################################################
def day12p1():
    data = get_input(parse1, args.puzzle)
    debug_print("\n".join(data), "\n")

    start = (0, 0)
    end = (-1, -1)
    for y, r in enumerate(data):
        for x, c in enumerate(r):
            if c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)
    debug_print("Start", start, "End", end)

    result = lib.find_paths(
        get_neighbors=get_neighbors(data),
        is_end=lambda coord: coord == end,
        starting_point=start,
    )

    shortest_path = min(result, key=lambda p: p.steps)

    if args.map:
        print_map(shortest_path, end)

    paths = len(result)
    debug_print("Paths", paths)

    return shortest_path.steps


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day12p2():
    data = get_input(parse2, args.puzzle)
    end = (-1, -1)
    for y, r in enumerate(data):
        for x, c in enumerate(r):
            if c == "E":
                end = (x, y)
                break

    paths: List[lib.ToVisit] = []

    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == "a":
                paths_from_this = lib.find_paths(
                    get_neighbors=get_neighbors(data),
                    is_end=lambda coord: coord == end,
                    starting_point=(x, y),
                )
                paths.extend(paths_from_this)

    debug_print("Path qty:", len(paths))
    shortest_path = min(paths, key=lambda p: p.steps)
    if args.map:
        print_map(shortest_path, end)

    return shortest_path.steps


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 12 - Part 1", "-" * n)
        print("Result =>", day12p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 12 - Part 2", "-" * n)
        print("Result =>", day12p2())
    print()


main()

import argparse
import sys
from pathlib import Path
from typing import Any, Callable, List, TypeVar

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


import re
from collections import namedtuple

Game = namedtuple("Game", ["id", "blue", "red", "green", "raw"])
cpat_colors_b = re.compile(r"(\d+) blue")
cpat_colors_r = re.compile(r"(\d+) red")
cpat_colors_g = re.compile(r"(\d+) green")
cpat_id = re.compile(r"^Game (\d+):")


################################################################################
############################### Start of Part 1 ################################
################################################################################
def parse1(line: str):
    return Game(
        id=int(cpat_id.match(line).groups()[0]),
        blue=max(map(int, cpat_colors_b.findall(line))),
        red=max(map(int, cpat_colors_r.findall(line))),
        green=max(map(int, cpat_colors_g.findall(line))),
        # raw=line,
        raw=None,
    )


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day02p1():
    games = get_input(parse1, args.puzzle)
    # 12 red cubes, 13 green cubes, and 14 blue cubes
    max_r = 12
    max_g = 13
    max_b = 14
    id_sum = 0
    for g in games:
        if g.blue <= max_b and g.red <= max_r and g.green <= max_g:
            id_sum += g.id
            print("yes", end=" ")
        print(g)
    return id_sum


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day02p2():
    games = get_input(parse2, args.puzzle)
    result = 0
    for g in games:
        result += g.red * g.green * g.blue
    return result


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2

    if 1 in args.part:
        print()
        print("-" * (n), "Day 02 - Part 1", "-" * n)
        print("Result =>", day02p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 02 - Part 2", "-" * n)
        print("Result =>", day02p2())
    print()


main()

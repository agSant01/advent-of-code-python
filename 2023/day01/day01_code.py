import argparse
import sys
from curses.ascii import isalpha
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


################################################################################
############################### Start of Part 1 ################################
################################################################################
def parse1(line: str):
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################

import re


################################################################################
def day01p1():
    data = get_input(parse1, args.puzzle)
    print(args.puzzle)
    numbers = []
    pat = re.compile(r"\d")
    for d in data:
        print(d)
        digits = pat.findall(d)
        a, b = digits[0], digits[-1]
        numbers.append(int(a + b))
    return sum(numbers)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


map_ = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


################################################################################
def day01p2():
    data = get_input(parse2, args.puzzle)

    pat = r"(?=(zero|one|two|three|four|five|six|seven|eight|nine|[0-9]))"
    cpat = re.compile(pat)
    numbers = []
    for d in data:
        all_nums = cpat.findall(d)

        for idx, num in enumerate(all_nums):
            if num.isalpha():
                all_nums[idx] = map_[num]

        a, b = all_nums[0], all_nums[-1]
        if args.debug:
            print(d, a, b, int(a + b))
        numbers.append(int(a + b))

    return sum(numbers)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2

    if 1 in args.part:
        print()
        print("-" * (n), "Day 01 - Part 1", "-" * n)
        print("Result =>", day01p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 01 - Part 2", "-" * n)
        print("Result =>", day01p2())
    print()


main()

import argparse
import math
import sys
from math import radians
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
arg_parser.add_argument(
    "--test",
    "-t",
    help="Execute tests",
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


def snafu_to_base10(number: str):
    ptr = len(number) - 1
    base10 = 0
    radix = 1

    while ptr >= 0:
        c = number[ptr]
        if c == "=":
            to_add = -2 * radix
        elif c == "-":
            to_add = -1 * radix
        else:
            to_add = int(c) * radix
        base10 += to_add
        radix *= 5
        ptr -= 1
    return base10


def base10_to_snafu(number: int):
    snafu = []
    while number > 0:
        if number == 1:
            snafu.append("1")
            break
        digit = number % 5
        number = round(number / 5)

        if digit == 3:
            snafu.append("=")
        elif digit == 4:
            snafu.append("-")
        else:
            snafu.append(str(digit))

    return "".join(reversed(snafu))


################################################################################
def day25p1():
    data = get_input(parse1, args.puzzle)

    return base10_to_snafu(sum(snafu_to_base10(snafu) for snafu in data))


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day25p2():
    return True


def test():
    tests = [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ]
    for expected, to_test in tests:
        assert snafu_to_base10(to_test) == expected

    tests = [
        ("1=-0-2", 1747),
        ("12111", 906),
        ("2=0=", 198),
        ("21", 11),
        ("2=01", 201),
        ("111", 31),
        ("20012", 1257),
        ("112", 32),
        ("1=-1=", 353),
        ("1-12", 107),
        ("12", 7),
        ("1=", 3),
        ("122", 37),
    ]
    for expected, base10 in tests:
        assert base10_to_snafu(base10) == expected


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2

    if args.test:
        test()
        return

    if 1 in args.part:
        print()
        print("-" * (n), "Day 25 - Part 1", "-" * n)
        print("Result =>", day25p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 25 - Part 2", "-" * n)
        print("Result =>", day25p2())
    print()


main()

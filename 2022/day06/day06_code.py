import argparse
import sys
from pathlib import Path
from typing import Callable, List

###########################################################################
############################### Setup #####################################
###########################################################################

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
args, _ = arg_parser.parse_known_args(sys.argv)


def get_input(parse: Callable[[str], str], puzzle: bool = False) -> List[str]:
    data: List[str] = []
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


###########################################################################

################################################################################
############################### Start of Part 1 ################################
################################################################################
def parse1(line: str):
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def find_marker(data_stream: str, width: int) -> int:
    window: List[str] = list(data_stream[:width])
    for i in range(width, len(data_stream)):
        if len(set(window)) != width:
            window.pop(0)
            window.append(data_stream[i])
        else:
            return i
    return -1


################################################################################
def day06p1():
    data = get_input(parse1, args.puzzle)[0]
    return find_marker(data, 4)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day06p2():
    data: str = get_input(parse2, args.puzzle)[0]
    return find_marker(data, 14)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 06 - Part 1", "-" * n)
        print("Result =>", day06p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 06 - Part 2", "-" * n)
        print("Result =>", day06p2())
    print()


main()

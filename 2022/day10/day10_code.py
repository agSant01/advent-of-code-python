import argparse
import sys
from pathlib import Path
from typing import Any, Callable, List, TypeVar

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
    return line.split()


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day10p1():
    data = get_input(parse1, args.puzzle)
    X = 1
    cycle = 0
    signal_strengths = 0
    for inst in data:
        if len(inst) == 1:
            cycle += 1
            if ((cycle // 20) & 1) == 1 and cycle % 20 == 0:
                signal_strengths += cycle * X
        else:
            for _ in range(2):
                cycle += 1
                if ((cycle // 20) & 1) == 1 and cycle % 20 == 0:
                    signal_strengths += cycle * X
            X += int(inst[1])

    return signal_strengths


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day10p2():
    data = get_input(parse2, args.puzzle)
    px = 40
    py = 6
    display = [0 for _ in range(px * py)]
    X = 1
    cycle = 0
    for inst in data:
        row = (cycle + 1) // px
        delta = row * px
        if len(inst) == 1:
            cycle += 1
            if (cycle - 1) - delta in (X - 1, X, X + 1):
                display[cycle - 1] = 1
        else:
            for _ in range(2):
                cycle += 1
                if (cycle - 1) - delta in (X - 1, X, X + 1):
                    display[cycle - 1] = 1
            X += int(inst[1])

    for i in range(py):
        print("".join(map(lambda x: "#" if x else ".", display[i * px : i * px + px])))


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 10 - Part 1", "-" * n)
        print("Result =>", day10p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 10 - Part 2", "-" * n)
        print("Result =>", day10p2())
    print()


main()

import argparse
import sys
from pathlib import Path

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
args, _ = arg_parser.parse_known_args(sys.argv)


def get_input(parse: Callable[[str], str], test: bool = False) -> List[str]:
    data: List[str] = []
    if args.input:
        filename = Path(args.input)
    else:
        filename = Path(__file__).parent / f'input{"_test" if test else ""}.txt'

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


################################################################################
def day04p1():
    data = get_input(parse1, test=True)
    for d in data:
        print(d)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day04p2():
    data = get_input(parse2, test=True)
    for d in data:
        pass


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 04 - Part 1", "-" * n)
        print("Result =>", day04p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 04 - Part 2", "-" * n)
        print("Result =>", day04p2())
    print()


main()

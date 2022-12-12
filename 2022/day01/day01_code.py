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


def get_input(parse, test=False):
    data = []
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
    return int(line) if line else None


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day01p1():
    data = get_input(parse1, test=False)
    agg = 0
    max_ = 0
    max_idx = 0
    idx = 1
    for d in data:
        if d is None:
            if agg > max_:
                max_idx = idx
                max_ = agg
            agg = 0
            idx += 1
        else:
            agg += d
    return max_idx, max_


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day01p2():
    data = get_input(parse2, test=False)
    agg_list = []
    agg = 0
    for d in data:
        if d is None:
            agg_list.append(agg)
            agg = 0
        else:
            agg += d
    return sum(sorted(agg_list)[-3:])


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 01 - Part 1", "-" * n)
        print("Result =>", day01p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 01 - Part 2", "-" * n)
        print("Result =>", day01p1())
    print()


main()

import sys
import argparse
from pathlib import Path

###########################################################################
############################### Setup #####################################
###########################################################################
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    '--input', '-i',
    help='Input file path.',
    type=Path,
    required=False
)
arg_parser.add_argument('--part', '-p',
                        type=int,
                        default=(1, 2),
                        choices=(1, 2),
                        nargs=1,
                        help='Run part 1 or 2',
                        required=False
                        )
args, _ = arg_parser.parse_known_args(sys.argv)


def get_input(parse, test=False):
    data = []
    if args.input:
        filename = Path(args.input)
    else:
        filename = Path(__file__).parent / \
            f'input{"_test" if test else ""}.txt'

    with open(filename, 'r') as file:
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


def get_p(c):
    c = ord(c)
    if c > 96:
        return c - 96
    return c - 64 + 26

################################################################################


def day03p1():
    data = get_input(parse1, test=False)

    p_sum = 0
    for d in data:
        p = len(d)//2
        c1 = set(d[:p])
        c2 = set(d[p:])
        common_ = c1.intersection(c2).pop()
        p_sum += get_p(common_)
    return p_sum


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day03p2():
    data = get_input(parse2, test=False)
    p_sum = 0

    g_set = set()
    for i, rs in enumerate(data):
        c1 = set(rs)
        if len(g_set) == 0:
            g_set.update(c1)
        else:
            g_set.intersection_update(c1)
        if (i+1) % 3 == 0 and i > 0:
            p_sum += get_p(g_set.pop())
            g_set.clear()

    return p_sum


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    if 1 in args.part:
        print()
        print('-'*(n), "Day 03 - Part 1", '-'*n)
        print('Result =>', day03p1())
        print()
    if 2 in args.part:
        print('-'*(n), "Day 03 - Part 2", '-'*n)
        print('Result =>', day03p2())
    print()


main()

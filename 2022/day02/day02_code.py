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
    return line.split()


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


MOVE_1 = {"A": 1, "B": 2, "C": 3}  # rock  # paper  # scissors

MOVE_2 = {"X": 1, "Y": 2, "Z": 3}  # rock  # paper  # scissors

MOVE_TO_WIN = {2: 1, 3: 2, 1: 3}


def round_score(opponent, my_play):
    if opponent == my_play:
        return 3
    if MOVE_TO_WIN[my_play] == opponent:
        return 6
    return 0


################################################################################


def day02p1():
    data = get_input(parse1, test=False)
    score = 0
    for op, mp in data:
        score += round_score(MOVE_1[op], MOVE_2[mp]) + MOVE_2[mp]

    return score


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def select_move(opponent_move, round_result):
    if round_result == "X":
        return 0, MOVE_TO_WIN[opponent_move]
    if round_result == "Y":
        return 3, opponent_move
    if round_result == "Z":
        my_move = opponent_move + 1
        return 6, 1 if my_move == 4 else my_move


################################################################################


def day02p2():
    data = get_input(parse2, test=False)
    score = 0
    for op, rr in data:
        score += sum(select_move(MOVE_1[op], rr))
    return score


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

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

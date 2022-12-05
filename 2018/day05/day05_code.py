import argparse
import sys
from pathlib import Path
from typing import Callable, List, Set, Union

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


def cause_reaction(unitA: str, unitB: str):
    return abs(ord(unitA) - ord(unitB)) == 32


def observe_reaction(polymer: str, ignore_type_lower: Union[str, None] = None):
    if len(polymer) == 0:
        return ""

    units: List[str] = []

    if ignore_type_lower:
        uc_i = chr(ord(ignore_type_lower) - 32)
        lc_i = ignore_type_lower
    else:
        uc_i = lc_i = 0

    for unit in polymer:
        if unit == uc_i or unit == lc_i:
            continue

        if len(units) == 0:
            units.append(unit)
        else:
            if cause_reaction(units[-1], unit):
                units.pop()
            else:
                units.append(unit)

    return "".join(units)


################################################################################
def day05p1():
    polymer: str = get_input(parse1, args.puzzle)[0]

    experiment_result = observe_reaction(polymer)

    return len(experiment_result)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day05p2():
    polymer: str = get_input(parse2, args.puzzle)[0]

    existing_unit_types: Set[str] = set(polymer)

    lc_units = filter(lambda x: 97 <= ord(x) <= 122, existing_unit_types)

    min_len = sys.maxsize

    for unit_type in lc_units:
        reaction = observe_reaction(polymer, ignore_type_lower=unit_type)
        reaction_len = len(reaction)
        if reaction_len < min_len:
            min_len = reaction_len

    return min_len


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 05 - Part 1", "-" * n)
        print("Result =>", day05p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 05 - Part 2", "-" * n)
        print("Result =>", day05p2())
    print()


main()

import argparse
import enum
import sys
from pathlib import Path
from re import A
from tkinter.tix import Tree
from typing import Any, Callable, List, TypeVar, Union

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
def parse1(line: str) -> Union[None, List[Any]]:
    if len(line) == 0:
        return None
    return eval(line)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


class Order(enum.IntEnum):
    RIGHT = -1
    EQ = 0
    WRONG = 1


def is_right_order(
    left: Union[int, List[int], List[List[int]]],
    right: Union[int, List[int], List[List[int]]],
) -> Order:
    if isinstance(left, int) and isinstance(right, int):
        debug_print("int and int", left, right)
        if left - right > 0:
            return Order.WRONG
        elif left - right < 0:
            return Order.RIGHT
        return Order.EQ
    elif isinstance(left, list) and isinstance(right, list):
        l_l = len(left)
        l_r = len(right)
        debug_print("list and list", left, l_l, right, l_r)

        for l, r in zip(left, right):
            res = is_right_order(l, r)
            if res != Order.EQ:
                return res

        # can't conclude after comparing all elements, need check length
        if l_l > l_r:
            return Order.WRONG
        elif l_l < l_r:
            return Order.RIGHT

        return Order.EQ
    else:
        debug_print("list and int", left, right)
        if isinstance(left, int):
            left = [left]
        elif isinstance(right, int):
            right = [right]
        return is_right_order(left, right)


################################################################################
def day13p1():
    data = get_input(parse1, args.puzzle)

    pairs = []
    i = 0
    while i < len(data):
        if isinstance(data[i], list):
            pairs.append((data[i], data[i + 1]))
            i += 3

    result = []
    for idx, pair in enumerate(pairs, start=1):
        left, right = pair
        debug_print(f"Pair {idx}")

        res = is_right_order(left, right)

        debug_print(f"Pair {idx} | Is right order: {(str(res))}")

        if res != Order.WRONG:
            result.append(idx)

    debug_print("Indexes:", result)

    return sum(result), len(result)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day13p2():
    data = get_input(parse2, args.puzzle)

    dividers = (
        [[2]],
        [[6]],
    )

    ordered_list = [*dividers]

    for line in data:
        if isinstance(line, list):
            lib.sorted_insert(
                ordered_list,
                line,
                comparator=is_right_order,
            )

    debug_print("\nPacket list\n=>", "\n=> ".join(map(str, ordered_list)), "\n")

    idx_s = []

    for i, p in enumerate(ordered_list, start=1):
        if p in dividers:
            idx_s.append(i)
        if len(idx_s) == 2:
            return idx_s[0] * idx_s[1]


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 13 - Part 1", "-" * n)
        print("Result =>", day13p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 13 - Part 2", "-" * n)
        print("Result =>", day13p2())
    print()


main()

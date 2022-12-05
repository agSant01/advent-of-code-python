import argparse
import collections
import sys
from pathlib import Path
from typing import Any, Callable, DefaultDict, Dict, List, Tuple

###########################################################################
############################### Setup #####################################
###########################################################################
sys.path.append(Path(__file__).parent.parent.as_posix())

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
            data.append(parse(line.rstrip()))
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


def extract_data(lines: List[str]):
    stacks_collection: Dict[int, List[str]] = collections.defaultdict(list)
    instructions: List[Tuple[int, int, int]] = []
    diagram = True

    for line in lines:
        if len(line) == 0:
            diagram = False
            continue
        if diagram:
            nxt = line.find("[")
            while nxt != -1:
                stacks_collection[nxt // 4 + 1].insert(0, line[nxt + 1])
                nxt = line.find("[", nxt + 1)
        else:
            items = line.split()
            instructions.append((int(items[1]), int(items[3]), int(items[5])))

    return stacks_collection, instructions


def get_top_crates(stacks: DefaultDict[int, List[str]]):
    sorted_stacks = sorted(stacks.items(), key=lambda x: x[0])
    top_crates = list(map(lambda x: x[1].pop(), sorted_stacks))
    return top_crates


################################################################################
def day05p1():
    global diagram
    diagram = True
    data: List[Any] = get_input(parse1, args.puzzle)

    stacks, instructions = extract_data(data)

    # print(stacks, instructions)

    for qty, from_, to_ in instructions:
        for _ in range(qty):
            stacks[to_].append(stacks[from_].pop())

    top_crates = get_top_crates(stacks)

    return "".join(top_crates)


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
    data = get_input(parse2, args.puzzle)

    stacks, instructions = extract_data(data)

    for qty, from_, to_ in instructions:
        movers: List[str] = []
        for _ in range(qty):
            movers.append(stacks[from_].pop())
        stacks[to_].extend(reversed(movers))

    top_crates = get_top_crates(stacks)
    return "".join(top_crates)


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

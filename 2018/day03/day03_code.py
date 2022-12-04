import argparse
import collections
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence, Tuple

###########################################################################
############################### Setup #####################################
###########################################################################
# sys.path.append(Path(__file__).parent.parent.as_posix())
# import lib


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


def get_input(parse: Callable[[Any], Any], puzzle: bool = False) -> List[Any]:
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
class Fabric:
    def __init__(self, data: str) -> None:
        splitted = data.split()

        self.id = splitted[0]

        margins = splitted[2].replace(":", "").split(",")
        self.left = int(margins[0])
        self.top = int(margins[1])

        dimensions = splitted[-1].split("x")

        self.width = int(dimensions[0])
        self.height = int(dimensions[1])

    def get_x_range(self):
        return (self.left, self.left + self.width - 1)

    def get_y_range(self):
        return (self.top, self.top + self.height - 1)

    def get_cells(self) -> List[Tuple[int, int]]:
        rgs: List[Tuple[int, int]] = []
        x_r = self.get_x_range()
        y_r = self.get_y_range()
        for x in range(x_r[0], x_r[1] + 1):
            for y in range(y_r[0], y_r[1] + 1):
                rgs.append((x, y))
        return rgs

    def __str__(self) -> str:
        return (
            f"<Fabric id={self.id}"
            f" x_range={self.get_x_range()} y_range={self.get_y_range()}>"
        )


def parse1(line: str) -> Fabric:
    return Fabric(line)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################
def is_partial_overlap(range1: Sequence[int], range2: Sequence[int]) -> bool:
    if range1[0] < range2[0]:
        return range1[1] >= range2[0]
    return range2[1] >= range1[0]


# def get_overlap(range1, range2) -> Tuple:
#     if is_partial_overlap(range1, range2):
#     return (0,0)

################################################################################
def day03p1():
    data: List[Fabric] = get_input(parse1, args.puzzle)
    coords: Dict[Tuple[int, int], int] = collections.defaultdict(int)
    for fabric in data:
        # print(fabric)
        for coord in fabric.get_cells():
            coords[coord] += 1
    return len(list(filter(lambda x: x >= 2, coords.values())))


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day03p2():
    data: List[Fabric] = get_input(parse2, args.puzzle)
    coords: Dict[Tuple[int, int], int] = collections.defaultdict(int)
    for fabric in data:
        for coord in fabric.get_cells():
            coords[coord] += 1

    for fabric in data:
        overlap = False
        for coord in fabric.get_cells():
            if coords[coord] >= 2:
                overlap = True
                break
        if not overlap:
            return fabric


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 03 - Part 1", "-" * n)
        print("Result =>", day03p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 03 - Part 2", "-" * n)
        print("Result =>", day03p2())
    print()


main()

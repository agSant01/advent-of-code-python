import argparse
import sys

from operator import mul
from collections import defaultdict

from pathlib import Path
from pprint import PrettyPrinter
from typing import Any, Callable, List, Tuple, TypeVar

###########################################################################
############################### Setup #####################################
###########################################################################
sys.path.append(Path(__file__).parent.parent.as_posix())
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
arg_parser.add_argument(
    "--debug",
    help="Debug mode.",
    default=False,
    action="store_true",
    required=False,
)
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

    print(f"Using input file {filename}")
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
    return list(line)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


class Number:
    def __init__(self) -> None:
        self.number: int | None = None
        self.coord = []
        self.is_part = False
        self.neighbor_gear = set()

    def __str__(self) -> str:
        return f"Number(number={self.number} coord={self.coord} is_part={self.is_part} gears={self.neighbor_gear} {self.__hash__()})"

    def __repr__(self) -> str:
        return self.__str__()

    # def __eq__(self, __value: object) -> bool:
    #     return self.coord == __value.coord


def get_nb(coord: Tuple[int, int], width: int, height: int):
    nbs = []
    for y in range(coord[1] - 1, coord[1] + 2):
        for x in range(coord[0] - 1, coord[0] + 2):
            if y >= 0 and y < height and x >= 0 and x < width:
                nbs.append((x, y))
    return nbs


################################################################################
def day03p1():
    data = get_input(parse1, args.puzzle)

    height = len(data)
    width = len(data[0])

    visited = set()
    to_visit = [(0, 0)]

    numbers = {}

    while len(to_visit) > 0:
        coord = to_visit.pop()

        if coord in visited:
            continue

        visited.add(coord)

        value = data[coord[1]][coord[0]]

        new_number = None
        if value.isnumeric() and coord not in numbers:
            new_number = Number()

            digits = []
            lp = coord[0]
            rp = coord[0] + 1
            while lp >= 0 and data[coord[1]][lp].isnumeric():
                digits.insert(0, data[coord[1]][lp])
                visited.add((lp, coord[1]))
                numbers[(lp, coord[1])] = new_number
                new_number.coord.append((lp, coord[1]))
                lp -= 1

            while rp < width and data[coord[1]][rp].isnumeric():
                digits.append(data[coord[1]][rp])
                visited.add((rp, coord[1]))
                numbers[(rp, coord[1])] = new_number
                new_number.coord.append((rp, coord[1]))
                rp += 1
            new_number.number = int("".join(digits))

        nbs = []

        if new_number:
            coords_to_a = new_number.coord
        else:
            coords_to_a = [coord]

        for cx, cy in coords_to_a:
            for y in range(cy - 1, cy + 2):
                if 0 > y or y >= height:
                    continue
                for x in range(cx - 1, cx + 2):
                    if x == cx and y == cy:
                        continue
                    if 0 <= x < width:
                        val = data[y][x]
                        if val != "." and not val.isnumeric():
                            if new_number:
                                new_number.is_part = True
                        nbs.append((x, y))

        to_visit.extend(nbs)

    parts = list(filter(lambda x: x.is_part, numbers.values()))
    parts = set(parts)

    if args.debug:
        print(list(map(lambda p: p.number, parts)))

    return sum(map(lambda p: p.number, parts))


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
    data = get_input(parse1, args.puzzle)

    height = len(data)
    width = len(data[0])

    visited = set()
    to_visit: List[Tuple[int, int]] = [(0, 0)]

    numbers = {}

    pairs = defaultdict(set)

    result = 0

    while len(to_visit) > 0:
        coord = to_visit.pop()

        if coord in visited:
            continue

        visited.add(coord)

        value = data[coord[1]][coord[0]]

        new_number = None
        if value.isnumeric() and coord not in numbers:
            new_number = Number()

            digits = []
            lp = coord[0]
            rp = coord[0] + 1
            while lp >= 0 and data[coord[1]][lp].isnumeric():
                digits.insert(0, data[coord[1]][lp])
                visited.add((lp, coord[1]))
                numbers[(lp, coord[1])] = new_number
                new_number.coord.append((lp, coord[1]))
                lp -= 1

            while rp < width and data[coord[1]][rp].isnumeric():
                digits.append(data[coord[1]][rp])
                visited.add((rp, coord[1]))
                numbers[(rp, coord[1])] = new_number
                new_number.coord.append((rp, coord[1]))
                rp += 1
            new_number.number = int("".join(digits))

        if new_number:
            coords_to_a = new_number.coord
        else:
            coords_to_a = [coord]

        for cx, cy in coords_to_a:
            for y in range(cy - 1, cy + 2):
                if 0 > y or y >= height:
                    continue
                for x in range(cx - 1, cx + 2):
                    if x == cx and y == cy:
                        continue
                    if x < 0 or x >= width:
                        continue
                    val = data[y][x]
                    if val != "." and not val.isnumeric():
                        if new_number:
                            new_number.is_part = True
                            if val == "*":
                                pairs[(x, y)].add(new_number)

                    to_visit.append((x, y))

    result = map(
        lambda p: mul(p[0].number, p[1].number),
        map(list, filter(lambda x: len(x) == 2, pairs.values())),
    )

    if args.debug:
        p = PrettyPrinter()
        p.pprint(pairs)

    return sum(result)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2

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

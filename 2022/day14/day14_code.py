import argparse
import sys
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, NamedTuple, Set, Tuple, TypeVar, Union

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
@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, tuple):
            return __o[0] == self.x and __o[1] == self.y
        if not isinstance(__o, Point):
            return False
        return (self.x == __o.x) and (self.y == __o.y)


def parse1(line: str) -> List[Point]:
    points = line.split(" -> ")
    coords = list(map(lambda x: x.split(","), points))
    return [Point(x=int(x), y=int(y)) for x, y in coords]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################
@dataclass
class Layout:
    wall_points: Set[Point]
    free_sand_points: List[Point]
    resting_sand: Set[Point]
    min_x: int
    max_x: int
    max_y: int

    def has_obstacle_in(self, x, y) -> bool:
        return (
            (x, y) in self.wall_points
            or (x, y) in self.resting_sand
            or (x, y) in self.free_sand_points
        )


def get_coords_from_points(points: List[Point]):
    coordinates = set()
    for current, next_point in zip(points, points[1:]):
        if current.x == next_point.x:
            ly = min(current.y, next_point.y)
            gy = max(current.y, next_point.y)
            for y in range(ly, gy + 1):
                coordinates.add(Point(current.x, y))
        elif current.y == next_point.y:
            lx = min(current.x, next_point.x)
            gx = max(current.x, next_point.x)
            for x in range(lx, gx + 1):
                coordinates.add(Point(x, current.y))
        current = next_point
    return coordinates


def print_simulation(layout: Layout, print_=False):
    if not args.debug and not print_:
        return
    print("=" * (layout.max_x - layout.min_x))
    for y in range(layout.max_y + 5):
        for x in range(layout.min_x - 25, layout.max_x + 25):
            if (x, y) in layout.wall_points:
                print("#", end="")
            elif (x, y) in layout.free_sand_points or (
                x,
                y,
            ) in layout.resting_sand:
                print("o", end="")
            elif (None, y) in layout.wall_points:
                print("#", end="")
            elif (x, y) == (500, 0):
                print("+", end="")
            else:
                print(".", end="")
        print()
    print("=" * (layout.max_x - layout.min_x))


def simulate(layout: Layout):
    while True:
        all_resting = True
        for i, sand in enumerate(layout.free_sand_points):
            if (None, sand.y + 1) in layout.wall_points:
                # do nothing
                # line of infinite X
                pass
            elif not layout.has_obstacle_in(sand.x, sand.y + 1):
                # check down
                all_resting = False
                sand.y += 1
            elif not layout.has_obstacle_in(sand.x - 1, sand.y + 1):
                # check down-left
                all_resting = False
                sand.x -= 1
                sand.y += 1
            elif not layout.has_obstacle_in(sand.x + 1, sand.y + 1):
                # check down-right
                all_resting = False
                sand.x += 1
                sand.y += 1

            if sand.y >= layout.max_y:
                layout.free_sand_points.pop(i)

        if all_resting:
            layout.resting_sand.update(layout.free_sand_points)
            layout.free_sand_points.clear()
            break


################################################################################
def day14p1():
    lines: List[List[Point]] = get_input(parse1, args.puzzle)

    wall_points = set()
    for line in lines:
        wall_points.update(get_coords_from_points(line))
    debug_print(wall_points)

    layout: Layout = Layout(
        wall_points=wall_points,
        free_sand_points=[],
        resting_sand=set(),
        max_x=max(wall_points, key=lambda p: p.x).x,
        min_x=min(wall_points, key=lambda p: p.x).x,
        max_y=max(wall_points, key=lambda p: p.y).y,
    )

    while True:
        current_sand = len(layout.resting_sand)
        layout.free_sand_points.append(Point(500, 0))

        simulate(layout)

        if current_sand == len(layout.resting_sand):
            break
        print_simulation(layout)

    return len(layout.resting_sand)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day14p2():
    lines = get_input(parse2, args.puzzle)

    wall_points = set()
    for line in lines:
        wall_points.update(get_coords_from_points(line))
    debug_print(wall_points)

    layout: Layout = Layout(
        wall_points=wall_points,
        free_sand_points=[],
        resting_sand=set(),
        max_x=max(wall_points, key=lambda p: p.x).x,
        min_x=min(wall_points, key=lambda p: p.x).x,
        max_y=max(wall_points, key=lambda p: p.y).y + 2,
    )


    layout.wall_points.add(Point(x=None, y=layout.max_y))  # type:ignore

    print_simulation(layout)

    while True:
        layout.free_sand_points.append(Point(500, 0))
        simulate(layout)
        if (500, 0) in layout.resting_sand:
            break

    print_simulation(layout)

    return len(layout.resting_sand)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 14 - Part 1", "-" * n)
        print("Result =>", day14p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 14 - Part 2", "-" * n)
        print("Result =>", day14p2())
    print()


main()

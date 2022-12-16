import argparse
import re
import sys
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Tuple,
    TypeVar,
    Union,
)

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
    default=(1, 3),
    choices=(1, 2, 3),
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

Sensor = NamedTuple("Sensor", x=int, y=int, bx=int, by=int)


def parse1(line: str) -> Sensor:
    numbers = re.findall(r"-*\d+", line)
    pn = lib.convert_to_int(numbers)
    return Sensor(*pn)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################

Coord = NamedTuple("Coord", x=int, y=int)


def print_map(covered, sensors, beacons):
    if not args.debug:
        return

    min_x = min(covered, key=lambda c: c[0])[0]
    max_x = max(covered, key=lambda c: c[0])[0]
    min_y = min(covered, key=lambda c: c[1])[1]
    max_y = max(covered, key=lambda c: c[1])[1]

    for y in range(min_y - 2, max_y + 2):
        print(str(y).zfill(2), end="")
        for x in range(min_x - 2, max_x + 2):
            if (x, y) in beacons:
                print("B", end="")
            elif (x, y) in sensors:
                print("S", end="")
            elif (x, y) in covered:
                print("#", end="")
            else:
                print(".", end="")
        print()


def find_occupied_at_depth(
    sensors: List[Sensor],
    analyzing_depth: int,
    min_c: int = None,  # type: ignore
    max_c: int = None,  # type: ignore
):
    ranges = []

    for sensor in sensors:
        md_sensor_beacon = lib.manhattan_distance(
            (sensor.x, sensor.y), (sensor.bx, sensor.by)
        )
        md_sensor_depth = lib.manhattan_distance(
            (sensor.x, sensor.y), (sensor.x, analyzing_depth)
        )

        if md_sensor_depth > md_sensor_beacon:
            continue

        x_component = md_sensor_beacon - md_sensor_depth

        low_b = int(sensor.x - x_component)
        high_b = sensor.x + x_component

        low_b = max(low_b, min_c)
        high_b = min(high_b, max_c)

        ranges.append((low_b, high_b))

    ranges.sort(key=lambda r: r[0])

    compressed_ranges = []
    i = 1
    c_range = list(ranges[0])
    while i < len(ranges):
        while i < len(ranges) and lib.Day04.is_partial_overlap(c_range, ranges[i]):
            debug_print("C_range:", c_range, "Next:", ranges[i], "partial overlap")
            c_range[1] = max(c_range[1], ranges[i][1])
            i += 1
        compressed_ranges.append(c_range)
        if i >= len(ranges):
            break
        c_range = list(ranges[i])
        i += 1

    return compressed_ranges


################################################################################
def day15p1():
    sensors: List[Sensor] = get_input(parse1, args.puzzle)

    analyzing_depth = 10 if not args.puzzle else 2_000_000

    ranges = []

    for sensor in sensors:
        md_sensor_beacon = lib.manhattan_distance(
            (sensor.x, sensor.y), (sensor.bx, sensor.by)
        )
        md_sensor_depth = lib.manhattan_distance(
            (sensor.x, sensor.y), (sensor.x, analyzing_depth)
        )

        if md_sensor_depth > md_sensor_beacon:
            continue

        x_component = md_sensor_beacon - md_sensor_depth

        ranges.append((sensor.x - x_component, sensor.x + x_component))

    ranges.sort(key=lambda r: r[0])

    compressed_ranges = []
    i = 1
    c_range = list(ranges[0])
    while i < len(ranges):
        while i < len(ranges) and lib.Day04.is_partial_overlap(c_range, ranges[i]):
            debug_print("C_range:", c_range, "Next:", ranges[i], "partial overlap")
            c_range[1] = max(c_range[1], ranges[i][1])
            i += 1
        compressed_ranges.append(c_range)
        if i >= len(ranges):
            break
        c_range = list(ranges[i])
        i += 1

    debug_print("CompRanges", compressed_ranges)

    return sum(max_ - min_ for min_, max_ in compressed_ranges)  # compressed ranges sum


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day15p2():
    sensors: List[Sensor] = get_input(parse2, args.puzzle)

    max_coord = 20 if not args.puzzle else 4_000_000
    print(max_coord)

    for y in range(2_000_000, max_coord, 1):
        ranges = find_occupied_at_depth(
            sensors,
            y,
            min_c=0,
            max_c=max_coord,
        )
        # print(y, ranges)
        if len(ranges) > 1:
            print(ranges)
            if ranges[0][1] + 1 != ranges[1][0]:
                return (ranges[0][1] + 1, y), (ranges[0][1] + 1) * 4000000 + y

    return None


E = TypeVar("E")


def for_each(func: Callable[[E], Any], iterable: Iterable[E]) -> List[Any]:
    return list(map(func, iterable))


################################################################################
########################## Helper Functions of Part 3 ##########################
################################################################################

Point = NamedTuple("Point", x=int, y=int)


def line_intersection(line1, line2) -> Union[None, Point]:
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) // div
    y = det(d, ydiff) // div
    return Point(x, y)


def day15p2Optimized():
    sensors: List[Sensor] = get_input(parse2, args.puzzle)
    max_coord = 20 if not args.puzzle else 4_000_000

    distances_sensor_beacons: Dict[Sensor, int] = dict(
        for_each(
            lambda s: (s, lib.manhattan_distance((s.x, s.y), (s.bx, s.by))),
            sensors,
        )
    )

    lines: List[Tuple[Point, Point]] = []

    for sensor, d in distances_sensor_beacons.items():
        left_p = Point(sensor.x - d - 1, sensor.y)
        right_p = Point(sensor.x + d + 1, sensor.y)
        up_p = Point(sensor.x, sensor.y - d - 1)
        down_p = Point(sensor.x, sensor.y + d + 1)
        lines.extend(
            [
                (up_p, left_p),
                (up_p, right_p),
                (down_p, left_p),
                (down_p, right_p),
            ]
        )

    intersection_points = set()
    for line in lines:
        for line2 in lines:
            if line == line2:
                continue
            inter = line_intersection(line, line2)
            if inter and 0 <= inter.x <= max_coord and 0 <= inter.y <= max_coord:
                intersection_points.add(inter)

    beacon_position: Point = list(
        filter(
            lambda point: all(
                lib.manhattan_distance((sensor.x, sensor.y), point) > dist
                for sensor, dist in distances_sensor_beacons.items()
            ),
            intersection_points,
        )
    ).pop()

    print(beacon_position)

    return beacon_position.x * 4_000_000 + beacon_position.y


import time


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 15 - Part 1", "-" * n)
        tc = time.perf_counter()
        print("Result =>", day15p1(), f"| Result #1 in {time.perf_counter() - tc:.3f} s")
        print()

    if 2 in args.part:
        print("-" * (n), "Day 15 - Part 2", "-" * n)
        tc = time.perf_counter()
        print("Result =>", day15p2())
        print(f"Result #2 in {time.perf_counter() - tc:.3f} s")
        print()

    if 3 in args.part:
        print("-" * (n), "Day 15 - Part 3 (Part 2 - optimized)", "-" * n)
        tc = time.perf_counter()
        print(
            "Result =>",
            day15p2Optimized(),
            f"| Result #3 in {time.perf_counter() - tc:.3f} s",
        )
    print()


main()

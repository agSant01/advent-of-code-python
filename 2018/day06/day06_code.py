import argparse
import collections
import sys
from pathlib import Path
from typing import Callable, Dict, List, Set, Tuple, TypeVar

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

    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


###########################################################################

################################################################################
############################### Start of Part 1 ################################
################################################################################
def parse1(line: str) -> Tuple[int, int]:
    x, y = line.split(", ")
    return int(x), int(y)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def manhattan_distance(c1: Tuple[int, int], c2: Tuple[int, int]) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def neighbors(coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    nbs_cs: List[Tuple[int, int]] = []
    for x in range(coord[0] - 1, coord[0] + 2):
        for y in range(coord[1] - 1, coord[1] + 2):
            nbs_cs.append((x, y))
    return nbs_cs


def find_corners(centroids: List[Tuple[int, int]]):
    corners: Set[Tuple[int, int]] = set()

    left_x = min(centroids, key=lambda x: x[0])
    right_x = max(centroids, key=lambda x: x[0])
    top_y = min(centroids, key=lambda x: x[1])
    bottom_y = max(centroids, key=lambda x: x[1])
    for c in centroids:
        if c[0] == left_x[0]:
            corners.add(c)
        if c[0] == right_x[0]:
            corners.add(c)
        if c[1] == top_y[1]:
            corners.add(c)
        if c[1] == bottom_y[1]:
            corners.add(c)

    def is_out_of_bounds(xy: Tuple[int, int]) -> bool:
        if xy[0] > right_x[0] or xy[0] < left_x[0]:
            return True

        if xy[1] > bottom_y[1] or xy[1] < top_y[1]:
            return True

        return False

    return corners, is_out_of_bounds


def print_regions(
    named_centroids: Dict[Tuple[int, int], str],
    coordinates: Dict[Tuple[int, int], Set[Tuple[int, int]]],
    debug: bool = args.debug,
) -> None:
    if not debug:
        return

    all_cs: List[Tuple[int, int]] = []
    for c_set in coordinates.values():
        all_cs.extend(c_set)

    left_x = min(all_cs, key=lambda x: x[0])[0]
    right_x = max(all_cs, key=lambda x: x[0])[0]
    top_y = min(all_cs, key=lambda x: x[1])[1]
    bottom_y = max(all_cs, key=lambda x: x[1])[1]
    cartesian_plane = [
        ["." for _ in range(right_x + 1 - left_x)] for _ in range(bottom_y + 1 - top_y)
    ]

    for centroid_xy, region_coordinates in coordinates.items():
        centroid_name = named_centroids[centroid_xy]
        cartesian_plane[centroid_xy[1] - top_y][centroid_xy[0] - left_x] = centroid_name

        lc = centroid_name.lower()
        for x, y in region_coordinates:
            # print(x, y, "|", len(cartesian_plane), len(cartesian_plane[0]))
            cartesian_plane[y - top_y][x - left_x] = lc

    for r in cartesian_plane:
        print("".join(r))


################################################################################
def day06p1():
    """
    Find the largest area surrounding a Centroid (input coordinates) that is not infinite.
    The input coordinates represent a point in an Infinite grid.

    Returns:
        int: the size of the largest area that isn't infinite
    """
    centroids: List[Tuple[int, int]] = get_input(parse1, args.puzzle)

    # For debugging purposes: Name the centroids
    named_centroids: Dict[Tuple[int, int], str] = {}
    for i, d in enumerate(centroids):
        named_centroids[d] = chr(i + 65)

    if args.debug:
        print("Named Centroids:", named_centroids)
    ############################################

    corners, is_out_of_bounds = find_corners(centroids)

    # result map
    c_area_cords: Dict[Tuple[int, int], Set[Tuple[int, int]]] = collections.defaultdict(
        set
    )

    for centroid in centroids:
        if centroid in corners:
            # if centroid is in the edges we do not need to check it since
            # it will have an infinite region
            continue

        # DFS search
        to_visit = [centroid]
        visited: Set[Tuple[int, int]] = set()

        while len(to_visit) > 0:
            current_xy = to_visit.pop()

            # if visited or out of bounds do not visit
            # avoid infinite search
            if current_xy in visited or is_out_of_bounds(current_xy):
                continue

            visited.add(current_xy)

            # calculate M. distance from this coordinate to the (x,y) of the centroid
            # if distance to this centroid is less than to any of the other Centroids
            # assign to current centroid area
            md_curr_centroid = manhattan_distance(current_xy, centroid)
            assign_to_curr_centroid = True

            # compare Manhattan distance to rest of centroids
            for nc in centroids:
                if nc == centroid:
                    continue
                md_other_centroid = manhattan_distance(current_xy, nc)
                if not (md_curr_centroid < md_other_centroid):
                    assign_to_curr_centroid = False
                    break

            if assign_to_curr_centroid:
                # current_xy belongs to this centroid
                # add to centroid region dict
                c_area_cords[centroid].add(current_xy)
            else:
                # not part of the region
                # no need to visit the neighbors
                continue

            for nb in neighbors(current_xy):
                if nb not in visited:
                    to_visit.append(nb)

    # print map in debug mode
    print_regions(named_centroids, c_area_cords)

    largest_region = max(c_area_cords.values(), key=lambda x: len(x))

    return len(largest_region)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day06p2():
    """Find a region that contains all the Centroids and that every coordinate
    has an aggregate of the Manhattan distances to every centroid of less than THRESHOLD

    Returns:
        int: the size of the region containing all locations which have a total distance
            to all given coordinates of less than THRESHOLD
    """
    centroids = get_input(parse2, args.puzzle)

    THRESHOLD = 10_000

    _, is_out_of_bounds = find_corners(centroids)

    to_visit = [centroids[0]]  # start at the point of any centroid
    visited: Set[Tuple[int, int]] = set()

    region_area: int = 0

    # Depth First Search
    while len(to_visit) > 0:
        c = to_visit.pop()

        if c in visited or is_out_of_bounds(c):
            continue

        visited.add(c)

        # sum of manhattan distance from this coordinate to every centroid
        total_d = sum(manhattan_distance(centroid, c) for centroid in centroids)

        if total_d < THRESHOLD:
            region_area += 1
        else:
            # if not satisfies the THRESHOLD, then no need to visit its neighbors
            continue

        for nb in neighbors(c):
            if nb not in visited:
                to_visit.append(nb)

    return region_area


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 06 - Part 1", "-" * n)
        print("Result =>", day06p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 06 - Part 2", "-" * n)
        print("Result =>", day06p2())
    print()


main()

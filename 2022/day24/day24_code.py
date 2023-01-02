import argparse
import heapq
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Set, Tuple, TypeVar

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
def parse1(line: str):
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


@dataclass
class Blizzard:
    x: int
    y: int
    icon: str

    def move(self, x_bound: int, y_bound: int):
        is_x = self.icon in (">", "<")
        delta = 1 if self.icon in (">", "v") else -1
        if is_x:
            new_x = self.x + delta
            if new_x > x_bound:
                new_x = 1
            elif new_x < 1:
                new_x = x_bound
            return Blizzard(new_x, self.y, self.icon)
        else:
            new_y = self.y + delta
            if new_y > y_bound:
                new_y = 1
            elif new_y < 1:
                new_y = y_bound
            return Blizzard(self.x, new_y, self.icon)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, tuple):
            return self.x == __o[0] and self.y == __o[1]
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def parse_blizzards(lines: List[str]):
    blizzards = set()
    for idx_y, line in enumerate(lines):
        for idx_x, c in enumerate(line):
            if c in (">", "<", "^", "v"):
                blizzards.add(Blizzard(idx_x, idx_y, c))
    return blizzards


def get_blizzard_by_minute(
    blizzard_states: Dict[int, Set[Blizzard]],
    minute: int,
    width: int,
    height: int,
) -> Set[Blizzard]:
    if minute in blizzard_states:
        return blizzard_states[minute]

    last_state_min = max(blizzard_states.keys())
    last_state = blizzard_states[last_state_min]

    for _cm in range(last_state_min + 1, minute + 1):
        new_state = set()
        for b in last_state:
            new_state.add(b.move(width - 2, height - 2))
        blizzard_states[_cm] = new_state
        last_state = new_state

    return last_state


def print_grid(blizzards: List[Blizzard], pos, width, height):
    if not args.debug:
        return
    for y in range(height):
        for x in range(width):
            if pos == (x, y):
                print("E", end="")
            elif x == 0 or y == 0:
                print("#", end="")
            elif y == height - 1 and x == width - 2:
                print(".", end="")
            elif x == width - 1 or y == height - 1:
                print("#", end="")
            elif (x, y) in blizzards:
                b = blizzards.index((x, y))  # type:ignore
                cnt = blizzards.count((x, y))  # type:ignore
                if cnt > 1:
                    print(cnt, end="")
                else:
                    print(blizzards[b].icon, end="")
            else:
                print(".", end="")
        print()


def shortest_route(
    blizzard_states,
    start_time: int,
    start_point: Tuple,
    target: Tuple,
    width: int,
    height: int,
):
    def is_wall(pos):
        return (
            pos[0] <= 0
            or pos[0] >= width - 1
            or (pos[1] <= 0 and pos[0] != 1)
            or (pos[1] >= height - 1 and pos[0] != width - 2)
        )

    completion_time = sys.maxsize
    to_visit: List[Any] = [(start_time, start_point)]
    visited = set()

    while to_visit:
        item_ = heapq.heappop(to_visit)
        (x, y), steps = item_[1], item_[0]

        if steps >= completion_time:
            continue

        if (x, y) == target:
            completion_time = min(completion_time, steps)
            continue

        if (x, y, steps) in visited:
            continue

        visited.add((x, y, steps))

        next_blizzard = get_blizzard_by_minute(blizzard_states, steps + 1, width, height)
        for dx, dy in [(0, 0), (0, -1), (-1, 0), (0, 1), (1, 0)]:
            new_pos = (x + dx, y + dy)
            if new_pos not in next_blizzard and not is_wall(new_pos):
                heapq.heappush(
                    to_visit,
                    (
                        steps + 1,
                        new_pos,
                    ),
                )

    return completion_time


################################################################################
def day24p1():
    data = get_input(parse1, args.puzzle)
    blizzards = parse_blizzards(data)
    width = len(data[0])
    height = len(data)

    start_pos = (1, 0)
    end_pos = (width - 2, height - 1)

    blizzard_states = {}
    blizzard_states[0] = blizzards

    return shortest_route(blizzard_states, 0, start_pos, end_pos, width, height)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day24p2():
    data = get_input(parse2, args.puzzle)
    blizzards = parse_blizzards(data)
    width = len(data[0])
    height = len(data)

    start_pos = (1, 0)
    end_pos = (width - 2, height - 1)

    blizzard_states = {}
    blizzard_states[0] = blizzards

    start_end = shortest_route(blizzard_states, 0, start_pos, end_pos, width, height)
    end_start = shortest_route(
        blizzard_states, start_end, end_pos, start_pos, width, height
    )

    return shortest_route(blizzard_states, end_start, start_pos, end_pos, width, height)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2

    if 1 in args.part:
        print()
        print("-" * (n), "Day 24 - Part 1", "-" * n)
        print("Result =>", day24p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 24 - Part 2", "-" * n)
        print("Result =>", day24p2())
    print()


main()

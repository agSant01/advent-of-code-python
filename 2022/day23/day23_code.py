import argparse
import enum
import sys
from collections import defaultdict
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


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, __o: object):
        if isinstance(__o, tuple):
            return Position(self.x + __o[0], self.y + __o[1])
        if isinstance(__o, Position):
            return Position(self.x + __o.x, self.y + __o.y)
        raise ValueError(f"Object {__o} is not of Type Position or tuple[int, int]")

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, tuple):
            return self.x == __o[0] and self.y == __o[1]
        if isinstance(__o, Position):
            return self.x == __o.x and self.y == __o.y
        return super().__eq__(__o)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def print_grid(elves: List[Position]):
    if not args.debug:
        return
    print("=" * 10)
    min_X = min(elves, key=lambda ep: ep.x).x
    max_X = max(elves, key=lambda ep: ep.x).x
    min_Y = min(elves, key=lambda ep: ep.y).y
    max_Y = max(elves, key=lambda ep: ep.y).y

    lib.print_range_horizontal(min_X - 3, max_X + 3, 2)
    for y in range(min_Y - 3, max_Y + 3):
        print(str(y).zfill(2), end="")
        for x in range(min_X - 3, max_X + 3):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


class Orientation(enum.IntEnum):
    N = 0
    S = 1
    W = 2
    E = 3


################################################################################
def day23p1():
    data = get_input(parse1, args.puzzle)
    # elf_positions: Dict[Position, List[Literal["N", "S", "W", "E"]]] = {}
    elf_positions: Dict[Position, Tuple[Orientation, Position]] = {}
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                elf_positions[Position(x, y)] = (Orientation.N, Position(x, y))

    ROUNDS = 10

    to_move_dict = {}

    deltas = [
        [(0, -1), (1, -1), (-1, -1)],
        [(0, 1), (1, 1), (-1, 1)],
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0), (1, 1), (1, -1)],
    ]

    compass = {
        Orientation.N: (0, -1),
        Orientation.S: (0, 1),
        Orientation.W: (-1, 0),
        Orientation.E: (1, 0),
    }

    for _ in range(ROUNDS):
        # determine where to move the elves
        # first half of rounds
        for elf, (consideration_start, old_) in elf_positions.items():
            assert type(elf) == Position
            neighbor_elves = 0
            for x in range(elf.x - 1, elf.x + 2):
                for y in range(elf.y - 1, elf.y + 2):
                    if (x, y) == elf:
                        continue
                    if (x, y) in elf_positions:
                        neighbor_elves += 1

            if neighbor_elves == 0:
                to_move_dict[elf] = (consideration_start + 1, elf)
                continue

            to_move = elf
            for k in range(4):
                if all(
                    (elf + delta) not in elf_positions
                    for delta in deltas[(consideration_start + k) % 4]
                ):
                    to_move = elf + compass[(consideration_start + k) % 4]  # type:ignore
                    break

            consideration_start = (consideration_start + 1) % 4

            if to_move not in to_move_dict:
                to_move_dict[to_move] = (consideration_start, elf)
            else:
                other_consideration_start, other_elf = to_move_dict.pop(to_move)
                to_move_dict[other_elf] = (other_consideration_start, other_elf)
                to_move_dict[elf] = (consideration_start, elf)

        elf_positions = to_move_dict
        to_move_dict = {}

    min_X = min(elf_positions, key=lambda ep: ep.x).x
    max_X = max(elf_positions, key=lambda ep: ep.x).x
    min_Y = min(elf_positions, key=lambda ep: ep.y).y
    max_Y = max(elf_positions, key=lambda ep: ep.y).y

    total_area = (max_X - min_X + 1) * (max_Y - min_Y + 1)

    return total_area - len(elf_positions)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day23p2():
    data = get_input(parse2, args.puzzle)
    # elf_positions: Dict[Position, List[Literal["N", "S", "W", "E"]]] = {}
    # elf_positions: Dict[Position, Tuple[int, Position]] = {}
    elf_positions: Dict[Position, list] = defaultdict(list)
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                p = Position(x, y)
                elf_positions[p].append(p)

    deltas = {
        0: ((0, -1), (1, -1), (-1, -1)),
        1: ((0, 1), (1, 1), (-1, 1)),
        2: ((-1, 0), (-1, 1), (-1, -1)),
        3: ((1, 0), (1, 1), (1, -1)),
    }

    compass = {
        0: (0, -1),
        1: (0, 1),
        2: (-1, 0),
        3: (1, 0),
    }

    rounds = 0
    moved = True
    to_move_dict = defaultdict(list)
    while moved:
        moved = False
        # determine where to move the elves
        # first half of rounds
        for elf in elf_positions:
            # assert type(elf) == Position
            need_to_move = False
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if (x, y) == (0, 0):
                        continue
                    if (elf.x + x, elf.y + y) in elf_positions:
                        need_to_move = True
                        break

            if need_to_move is False:
                to_move_dict[elf].append(elf)
                continue

            moved = True
            to_move = elf
            for k in range(4):
                nk = (rounds + k) % 4
                need_move = True
                for delta in deltas[nk]:
                    if (elf + delta) in elf_positions:
                        need_move = False
                        continue
                if need_move:
                    to_move = elf + compass[nk]
                    break

            if to_move not in to_move_dict:
                to_move_dict[to_move].append(elf)
            else:
                to_move_dict[elf] = [elf]
                old_ = to_move_dict.pop(to_move).pop()
                to_move_dict[old_] = [old_]

        elf_positions = to_move_dict.copy()
        to_move_dict.clear()

        rounds += 1
        # print_grid(elf_positions.keys())
    # type: ignore
    return rounds


def day23p2_2():
    data = get_input(parse2, args.puzzle)
    elf_positions: Set[Position] = set()
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                elf_positions.add(Position(x, y))

    deltas = [
        ((0, -1), (1, -1), (-1, -1)),
        ((0, 1), (1, 1), (-1, 1)),
        ((-1, 0), (-1, 1), (-1, -1)),
        ((1, 0), (1, 1), (1, -1)),
    ]

    compass = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
    ]

    m = (-1, 0, 1)

    rounds = 0
    moved = True

    while moved:
        to_move_dict = defaultdict(list)
        moved = False
        # determine where to move the elves
        # first half of rounds
        for elf in elf_positions:
            need_to_move = False
            for x in m:
                for y in m:
                    if (x, y) == (0, 0):
                        continue
                    if (elf.x + x, elf.y + y) in elf_positions:
                        need_to_move = True
                        break

            if need_to_move is False:
                continue

            moved = True
            to_move: Position = None  # type:ignore
            for k in range(4):
                nk = (rounds + k) % 4
                if all((elf + delta) not in elf_positions for delta in deltas[nk]):
                    to_move = elf + compass[nk]
                    break
            if to_move is None:
                continue
            to_move_dict[to_move].append(elf)

        for new_p, old_p in to_move_dict.items():
            if len(old_p) == 1:
                elf_positions.remove(old_p[0])
                elf_positions.add(new_p)
        rounds += 1
    return rounds


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2

    if 1 in args.part:
        print()
        print("-" * (n), "Day 23 - Part 1", "-" * n)
        print("Result =>", day23p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 23 - Part 2", "-" * n)
        print("Result =>", day23p2())
    print()


if __name__ == "__main__":
    main()

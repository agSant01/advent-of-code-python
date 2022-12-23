import argparse
import sys
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Any, Callable, Iterable, List, TypeVar

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
def parse1(line: str) -> int:
    return int(line)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


@dataclass
class Node:
    prev: Any
    next: Any
    value: int

    def __repr__(self) -> str:
        return f"Node(value={self.value} prev={self.prev.value} next={self.next.value})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Node):
            return False
        return id(self) == id(__o)


class Decryptor:
    def __init__(self, sequence: Iterable[int], decrypt_key: int = 1) -> None:
        self.head: Node = None
        self.tail: Node = None
        self.__len: int = 0
        self.decrypt_key = decrypt_key
        self.original_order = []

        for value in sequence:
            self.append(value * decrypt_key)

    def append(self, value: int):
        node = Node(None, None, value)
        if self.head is None:
            self.head = node
            self.tail = node
            self.head.next = node
            self.head.prev = node
        else:
            self.head.prev = node
            node.next = self.head
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

        self.original_order.append(node)

        self.__len += 1

    def remove_node(self, node: Node):
        prev = node.prev
        next_ = node.next

        prev.next = next_
        next_.prev = prev

        if node == self.head:
            self.head = next_
        if node == self.tail:
            self.tail = prev

        self.__len -= 1

        return node

    def insert_after(self, before: Node, to_insert: Node):
        to_insert.prev = before
        to_insert.next = before.next

        before_next = before.next

        before.next = to_insert
        before_next.prev = to_insert

        self.__len += 1

    def mix_in_node(self, node: Node):
        number = node.value

        if number == 0:
            return

        node = self.remove_node(node)
        insertion_point = node.prev
        if number > 0:
            for _ in range(number % self.__len):
                insertion_point = insertion_point.next
        else:
            for _ in range(abs(number) % (self.__len)):
                insertion_point = insertion_point.prev

        self.insert_after(insertion_point, node)

    def apply_mixing(self, rounds: int = 1) -> List[int]:
        for _ in range(rounds):
            for og_node in self.original_order:
                self.mix_in_node(og_node)
        return list(map(lambda node: node.value, self.__iter__()))

    def __repr__(self) -> str:
        return ", ".join(map(lambda node: str(node.value), self.__iter__()))

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self):
        return self.__len

    def __iter__(self):
        curr = self.head
        for _ in range(self.__len):
            yield curr
            curr = curr.next


################################################################################
def day20p1():
    data: List[int] = get_input(parse1, args.puzzle)

    decryptor = Decryptor(data)
    debug_print(decryptor)
    mixed_sequence = decryptor.apply_mixing()
    debug_print(mixed_sequence)

    vals = []
    zero_index = mixed_sequence.index(0)
    for k in [1000, 2000, 3000]:
        idx_ = (zero_index + k) % len(mixed_sequence)
        vals.append(mixed_sequence[idx_])

    return vals, sum(vals)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day20p2():
    data = get_input(parse2, args.puzzle)

    decryptor = Decryptor(data, 811589153)

    debug_print(decryptor)

    mixed_sequence = decryptor.apply_mixing(10)

    debug_print(mixed_sequence)

    vals = []
    zero_index = mixed_sequence.index(0)
    for k in [1000, 2000, 3000]:
        idx_ = (zero_index + k) % len(mixed_sequence)
        vals.append(mixed_sequence[idx_])

    return vals, sum(vals)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 20 - Part 1", "-" * n)
        print("Result =>", day20p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 20 - Part 2", "-" * n)
        print("Result =>", day20p2())
    print()


main()

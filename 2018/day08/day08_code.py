import argparse
import sys
from pathlib import Path
from typing import Any, Callable, Iterator, List, Tuple, TypeVar, Union

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

args, _ = arg_parser.parse_known_args(sys.argv)

ParsedInput = TypeVar("ParsedInput")


def get_input(
    parse: Callable[[str], ParsedInput], puzzle: bool = False
) -> List[ParsedInput]:
    data: List[ParsedInput] = []
    if args.input:
        filename = Path(args.input)
    else:
        filename = Path(__file__).parents[0] / f'input{"" if puzzle else "_test"}.txt'
        if not filename.exists():
            print(f"[Warning] {filename.absolute()} does not exists.")
            print(
                f"[Info] Defaulting to {filename.parents[0] / 'input_test.txt'} for"
                " input."
            )
            print("-" * 42)
            filename = Path(__file__).parents[0] / "input_test.txt"

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
def parse1(line: str) -> Tuple[int, ...]:
    return tuple(map(int, line.split()))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def name_generator():
    turn = 0
    while True:
        yield chr(65 + turn)


class Node:
    def __init__(
        self,
        nid: int,
        children_count: int,
        meta_count: int,
        name_generator: Iterator[str],
    ) -> None:
        self.nid = nid
        self.name = next(name_generator)
        self.parent: Union[Node, None] = None

        self.children_count = self.remaining_children = children_count
        self.children: List[Node] = []

        self.meta_data = []
        self.meta_count = meta_count

        self.end_idx = None

    def meta_data_sum(self):
        return sum(self.meta_data) + sum(c.meta_data_sum() for c in self.children)

    def node_value(self):
        if self.children_count == 0:
            return sum(self.meta_data)

        value = 0
        for idx in self.meta_data:
            if idx - 1 >= self.children_count:
                continue
            value += self.children[idx - 1].node_value()
        return value

    def __repr__(self) -> str:
        return (
            f"Node(name={self.name} metaCount={self.meta_count} rc={self.remaining_children} metaData={self.meta_data})"
        )


def build_tree(data: Tuple[int, ...]):
    pending = [Node(0, data[0], data[1], name_generator())]
    root: Node = pending[0]

    i = 2
    while len(pending) > 0:
        curr_node = pending[-1]
        debug_print(curr_node)

        if curr_node.remaining_children > 0:
            new_node = Node(i, data[i], data[i + 1], name_generator())
            i += 2
            curr_node.children.append(new_node)
            new_node.parent = curr_node
            pending.append(new_node)
            debug_print("[Creating] new node:", new_node)
        elif curr_node.children_count == 0:
            debug_print("Adding meta data to node:", curr_node)
            for _ in range(curr_node.meta_count):
                curr_node.meta_data.append(data[i])
                i += 1
            if curr_node.parent:
                curr_node.parent.remaining_children -= 1
            pending.pop()
            debug_print("[Updated] node:", curr_node)
        elif curr_node.remaining_children == 0:
            debug_print(
                "[Adding] meta data to node after processing children:", curr_node
            )
            for _ in range(curr_node.meta_count):
                curr_node.meta_data.append(data[i])
                i += 1
            if curr_node.parent:
                curr_node.parent.remaining_children -= 1
            pending.pop()
            debug_print("[Updated] node:", curr_node)
    return root


################################################################################
def day08p1():
    data = get_input(parse1, args.puzzle)[0]
    debug_print(data)

    root = build_tree(data)

    return root, root.meta_data_sum()


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day08p2():
    data = get_input(parse2, args.puzzle)[0]
    debug_print(data)

    root = build_tree(data)

    return root, root.node_value()


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 08 - Part 1", "-" * n)
        print("Result =>", day08p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 08 - Part 2", "-" * n)
        print("Result =>", day08p2())
    print()


main()

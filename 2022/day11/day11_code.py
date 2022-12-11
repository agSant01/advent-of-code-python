import argparse
import re
import sys
from operator import add, mul
from pathlib import Path
from typing import Any, Callable, List, TypeVar

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


class Monkey:
    def __init__(self, lines: List[str]) -> None:
        self.id = re.findall(r"\d+", lines[0])[0]
        self.items = list(map(int, lines[1].split(": ")[1].split(", ")))
        # print(lines[2])
        self.operation = re.findall(r"(\+|\*) (old|\d+)", lines[2])[0]
        self.test_div = int(re.findall(r"\d+", lines[3])[0])
        self.if_true = int(re.findall(r"\d+", lines[4])[0])
        self.if_false = int(re.findall(r"\d+", lines[5])[0])
        self.inspections = 0

    def inspect_item(self):
        self.inspections += 1
        return self.items.pop(0)

    def apply_op(self, worry_score: int) -> int:
        op = mul if self.operation[0] == "*" else add
        if self.operation[1] == "old":
            return op(worry_score, worry_score)
        return op(int(self.operation[1]), worry_score)

    def throw_to(self, worry_score: int) -> int:
        if (worry_score % self.test_div) == 0:
            debug_print(f"Monkey: {self.id} throw to Monkey: {self.if_true}")
            return self.if_true
        debug_print(f"Monkey: {self.id} throw to Monkey: {self.if_false}")
        return self.if_false

    def __repr__(self) -> str:
        return (
            "<Monkey"
            f" id={self.id} inspections={self.inspections} items={self.items} op={self.operation} div={self.test_div} if_true={self.if_true} if_False={self.if_false}>"
        )

    def __str__(self) -> str:
        return self.__repr__()


def parse_monkeys(lines: List[str]) -> List[Monkey]:
    monkeys: List[Monkey] = []
    for i in range(len(lines)):
        if len(lines[i]) == 0:
            monkeys.append(Monkey(lines[i - 6 : i]))
    return monkeys


################################################################################
def day11p1():
    monkeys = parse_monkeys(get_input(parse1, args.puzzle))

    for r in range(20):
        for monk in monkeys:
            while len(monk.items) > 0:
                item_worry = monk.inspect_item()
                new_worry = monk.apply_op(item_worry) // 3
                throw_to = monk.throw_to(new_worry)
                monkeys[throw_to].items.append(new_worry)

        debug_print(f"Round {r} =" * 10)
        debug_print("\n".join(map(str, monkeys)))

    most_active_monkeys: List[Monkey] = sorted(
        monkeys, key=lambda m: m.inspections, reverse=True
    )[:2]

    debug_print("Most active =>", most_active_monkeys)

    return most_active_monkeys[0].inspections * most_active_monkeys[1].inspections


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day11p2():
    monkeys = parse_monkeys(get_input(parse2, args.puzzle))

    lcm = 1
    for m in monkeys:
        lcm *= lcm * m.test_div

    for _ in range(10000):
        for monk in monkeys:
            while len(monk.items) > 0:
                item_worry = monk.inspect_item()
                new_worry = monk.apply_op(item_worry)
                throw_to = monk.throw_to(new_worry)
                monkeys[throw_to].items.append(new_worry % lcm)

    most_active_monkeys: List[Monkey] = sorted(
        monkeys, key=lambda m: m.inspections, reverse=True
    )[:2]

    debug_print("Most active =>", most_active_monkeys)

    return most_active_monkeys[0].inspections * most_active_monkeys[1].inspections


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 11 - Part 1", "-" * n)
        print("Result =>", day11p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 11 - Part 2", "-" * n)
        print("Result =>", day11p2())
    print()


main()

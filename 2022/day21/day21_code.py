import argparse
import sys
from dataclasses import dataclass
from operator import add, imul, itruediv, sub
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple, TypeVar, Union

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


@dataclass
class ValueMonkey:
    name: str
    number: int


@dataclass
class OperationMonkey:
    name: str
    term1: str
    op: str
    term2: str


def parse1(line: str) -> Union[ValueMonkey, OperationMonkey]:
    name, values = line.split(": ")
    values = values.split()
    if len(values) == 1:
        return ValueMonkey(name, int(values[0]))
    return OperationMonkey(name, values[0], values[1], values[2])


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def calculate_monkeys(
    monkeys: List[Union[ValueMonkey, OperationMonkey]],
    start_monkey_name: str,
):
    monkey_results = {}
    monkey_by_name = {}

    for monkey in monkeys:
        monkey_by_name[monkey.name] = monkey
    debug_print(monkey_by_name)

    pending_monkeys: List[str] = [start_monkey_name]

    while pending_monkeys:
        curr_monkey_name = pending_monkeys.pop(0)
        current_mky = monkey_by_name[curr_monkey_name]

        if isinstance(current_mky, ValueMonkey):
            monkey_results[current_mky.name] = int(current_mky.number)
            continue

        if isinstance(current_mky, OperationMonkey):
            if (
                current_mky.term1 in monkey_results
                and current_mky.term2 in monkey_results
            ):
                operation: Callable[[int, int], Any] = add
                if current_mky.op == "*":
                    operation = imul
                elif current_mky.op == "-":
                    operation = sub
                elif current_mky.op == "/":
                    operation = itruediv

                monkey_results[current_mky.name] = operation(
                    monkey_results[current_mky.term1],
                    monkey_results[current_mky.term2],
                )
                continue
            else:
                pending_monkeys.append(current_mky.name)

            if (
                current_mky.term1 not in monkey_results
                and current_mky.term1 not in pending_monkeys
            ):
                pending_monkeys.append(current_mky.term1)

            if (
                current_mky.term2 not in monkey_results
                and current_mky.term2 not in pending_monkeys
            ):
                pending_monkeys.append(current_mky.term2)

    # print(monkey_results)

    return monkey_results


################################################################################
def day21p1():
    monkeys = get_input(parse1, args.puzzle)

    monkey_results = calculate_monkeys(monkeys, "root")

    return monkey_results["root"]


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def get_inverse_op(operation: str):
    if operation == "+":
        return sub
    if operation == "-":
        return add
    if operation == "*":
        return itruediv
    if operation == "/":
        return imul
    return add


def find_my_number(
    monkey_by_name: Dict[str, Union[ValueMonkey, OperationMonkey]],
    results: Dict[str, int],
    my_name: str,
):
    root_monkey: OperationMonkey = monkey_by_name["root"]  # type: ignore

    def get_term_sequence(terms_pending: List[Tuple[str, List[str]]]) -> List[str]:
        while terms_pending:
            term_name, path = terms_pending.pop(0)
            monkey = monkey_by_name[term_name]

            if term_name == my_name:
                return path

            if isinstance(monkey, ValueMonkey):
                continue

            terms_pending.append((monkey.term1, path + [monkey.term1]))
            terms_pending.append((monkey.term2, path + [monkey.term2]))
        return []

    term_names = get_term_sequence([(root_monkey.term1, [root_monkey.term1])])
    constant = results[root_monkey.term2]
    if len(term_names) == 0:
        term_names = get_term_sequence([(root_monkey.term2, [root_monkey.term2])])
        constant = results[root_monkey.term1]

    value = constant
    for name in term_names:
        cm: Union[OperationMonkey, ValueMonkey] = monkey_by_name[name]
        if isinstance(cm, ValueMonkey):
            break
        inv_op = get_inverse_op(cm.op)
        if cm.term1 in term_names:
            value = inv_op(value, results[cm.term2])
        else:
            if cm.op == "-":
                value = inv_op(value, results[cm.term1] * -1)
                value *= -1
            else:
                value = inv_op(value, results[cm.term1])

    return value


################################################################################
def day21p2():
    monkeys = get_input(parse2, args.puzzle)
    monkey_by_name = {}
    for monkey in monkeys:
        monkey_by_name[monkey.name] = monkey

    results = calculate_monkeys(monkeys, "root")
    value = find_my_number(monkey_by_name, results, "humn")

    return int(value)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 21 - Part 1", "-" * n)
        print("Result =>", day21p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 21 - Part 2", "-" * n)
        print("Result =>", day21p2())
    print()


main()

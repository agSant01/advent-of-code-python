import collections
import functools
from typing import Tuple


def get_filename(test=False):
    return f'day06_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line):
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def op_line(columns: list, char: Tuple[int, str]):
    dict_ = columns[char[0]]
    dict_[char[1]] += 1
    return columns


def count_letters(columns: list, line: str):
    return functools.reduce(op_line, enumerate(line), columns)


def join(iterable, sep: str = ""):
    return sep.join(iterable)


def join_reversed(iterable):
    return join(map(str, reversed(iterable)))


def freq_rep(column):
    return sorted(map(join_reversed, column), reverse=True)[0][-1]


def error_correct_msg(lines: list):
    return map(
        freq_rep,
        map(
            lambda col: list(col.items()),
            functools.reduce(
                count_letters,
                lines,
                list(map(lambda _: collections.defaultdict(int), range(len(lines[0])))),
            ),
        ),
    )


def error_correct_imp(lines: list):
    columns = [collections.defaultdict(int) for _ in lines[0]]

    for line in lines:
        for idx, char in enumerate(line):
            columns[idx][char] += 1

    msg = []
    for column in columns:
        items = []
        for item in column.items():
            items.append((item[1], item[0]))
        msg.append(max(items)[1])

    return "".join(msg)


################################################################################


def day06p1():
    lines = get_input(parse1, test=False)
    imp = error_correct_imp(lines)
    corrected_msg = error_correct_msg(lines)
    return "Functional:", join(corrected_msg), "Imperative:", imp


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def error_correct_imp_part2(lines: list):
    columns = [collections.defaultdict(int) for _ in lines[0]]

    for line in lines:
        for idx, char in enumerate(line):
            columns[idx][char] += 1

    msg = []
    for column in columns:
        items = []
        for item in column.items():
            items.append((item[1], item[0]))
        msg.append(min(items)[1])

    return "".join(msg)


################################################################################
def day06p2():
    lines = get_input(parse2, test=False)
    return error_correct_imp_part2(lines)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 06 - Part 1", "-" * n)
    print("Result =>", day06p1())
    print()
    print("-" * (n), "Day 06 - Part 2", "-" * n)
    print("Result =>", day06p2())
    print()


main()

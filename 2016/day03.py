import itertools
import functools


def get_filename(test=False):
    return f'day03_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data

################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    return list(map(int, line.split()))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day03p1():
    data = get_input(parse1, test=False)
    valid_ts = 0
    for d in data:
        d = sorted(d)
        if sum(d[0:2]) > d[2]:
            valid_ts += 1
    return valid_ts

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day03p2():
    lines = get_input(parse2, test=False)

    sides = list(  # consume to list
        functools.reduce(
            itertools.chain,  # reduced
            (  # iterable
                map(lambda column:  # all items in column <column>
                    map(lambda row: row[column], lines),
                    range(len(lines[0]))  # get columns indexes
                    )
            ),  # end of iterable
            []  # initial value
        )
    )

    # make every 3 NUMBERS into groups;
    # Each groups is the 3 sides of a triangle
    grouped_sides = map(
        lambda index: sorted(sides[index:index+3]),
        range(0, len(sides), 3)
    )

    # filter valid triangles
    valid_triangles = functools.reduce(
        lambda count, sides: count + (sides[0] + sides[1] > sides[2]),
        grouped_sides,
        0
    )

    return valid_triangles


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 03 - Part 1", '-'*n)
    print('Result =>', day03p1())
    print()
    print('-'*(n), "Day 03 - Part 2", '-'*n)
    print('Result =>', day03p2())
    print()


main()

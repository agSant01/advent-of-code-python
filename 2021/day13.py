import copy
import re
from typing import List, Tuple


def get_filename(test=False):
    return f'day13_input{"_test" if test else ""}.txt'


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
    if len(line) == 0:
        return None

    if ',' in line:
        return tuple(map(int, line.split(',')))

    axis, value = re.findall(r'(x|y)=(\d+)', line)[0]

    return axis, int(value)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def pp(values: list):
    max_x = max(values, key=lambda x: x[0])
    max_y = max(values, key=lambda x: x[1])

    mtrx = [[' ' for _ in range(max_x[0]+1)] for _ in range(max_y[1]+1)]

    for x, y in values:
        mtrx[y][x] = '#'

    for r in mtrx:
        print(''.join(r))


def fold_paper(marks: List[Tuple[int, int]], instructions: List[Tuple[str, int]], times: int):
    result = copy.deepcopy(marks)

    for i in range(times):
        instruction = instructions[i]

        tmp = set()

        if instruction[0] == 'x':
            x = instruction[1]
            for cdnt in result:
                if cdnt[0] < x:
                    tmp.add(cdnt)
                elif 0 < cdnt[0]-x <= x:
                    nx = x - (cdnt[0]-x)
                    tmp.add((nx, cdnt[1]))
        else:
            y = instruction[1]
            for cdnt in result:
                if cdnt[1] < y:
                    tmp.add(cdnt)
                elif 0 < cdnt[1]-y <= y:
                    ny = y - (cdnt[1]-y)
                    tmp.add((cdnt[0], ny))

        result = tmp

    return result

################################################################################


def day13p1():
    data = get_input(parse1, test=False)

    split_ = data.index(None)

    coordinates = data[:split_]
    folding = data[split_+1:]

    result = fold_paper(coordinates, folding, 1)

    return len(result)

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day13p2():
    data = get_input(parse2, test=False)

    split_ = data.index(None)

    coordinates = data[:split_]
    folding = data[split_+1:]

    result = fold_paper(coordinates, folding, len(folding))

    pp(result)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 13 - Part 1", '-'*n)
    print('Result =>', day13p1())
    print()
    print('-'*(n), "Day 13 - Part 2", '-'*n)
    print('Result =>', day13p2())
    print()


main()

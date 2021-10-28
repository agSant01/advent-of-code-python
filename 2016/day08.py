import numpy as np
import re
import functools
from itertools import count
from os import pipe


def get_filename(test=False):
    return f'day08_input{"_test" if test else ""}.txt'


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


def parse1(line_: str):
    line = line_.split(' ')
    a, b = list(re.findall(r'\d+', line_))
    if line[0] == 'rect':
        return (line[0], int(a), int(b))
    if line[0] != 'rotate':
        print("error parsing", line)
        exit(1)
    return (line[0], line[1], int(a), int(b))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


"""
rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall off the right end appear at the left end of the row.
rotate column x=A by B
"""


def execute(instruction, matrix):
    if instruction[0] == 'rect':
        for x in range(instruction[1]):
            for y in range(instruction[2]):
                matrix[y][x] = '#'
        return

    if instruction[0] == 'rotate':
        if instruction[1] == 'column':
            row_len = len(matrix)
            column, shift = instruction[2], instruction[3]
            data_col = [row[column] for row in matrix]
            for _ in range(shift):
                data_col.insert(0, data_col.pop())
            for row_idx in range(row_len):
                matrix[row_idx][column] = data_col[row_idx]
            return
        if instruction[1] == 'row':
            row, shift = instruction[2], instruction[3]
            data_row: list = matrix[row]
            for _ in range(shift):
                data_row.insert(0, data_row.pop())
            matrix[row] = data_row
            return

    print("ERROR")
    exit(1)


def turn_on_bit_display(instructions, x, y):
    matrix = [['.' for _ in range(x)] for _ in range(y)]

    for inst in instructions:
        execute(inst, matrix)

    return matrix


################################################################################


def day08p1():
    is_test = False
    instructions = get_input(parse1, test=is_test)

    x, y = 50, 6
    if is_test:
        x, y, = 7, 3

    matrix = turn_on_bit_display(instructions, x, y)

    def count_(acc, array): return acc + \
        len(list(filter(lambda x: x == '#', array)))

    return 'Turned on', functools.reduce(count_, matrix, 0)

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day08p2():
    is_test = False
    instructions = get_input(parse1, test=is_test)

    x, y = 50, 6
    if is_test:
        x, y, = 7, 3

    matrix = turn_on_bit_display(instructions, x, y)

    # pretty_print
    for r in matrix:
        print(''.join(map(lambda x: x.replace('.', ' '), r)))

    return True


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 08 - Part 1", '-'*n)
    print('Result =>', day08p1())
    print()
    print('-'*(n), "Day 08 - Part 2", '-'*n)
    print('Result =>', day08p2())
    print()


main()

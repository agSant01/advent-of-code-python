from itertools import product
import copy
from typing import List


def get_filename(test=False):
    return f'day20_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def bit_arr_to_dec(bitArr: List[bool]) -> int:
    """Convert bit array to decimal representation

    Args:
        bitArr (List[bool]): bit array

    Returns:
        int: int representation of bit array
    """
    value: int = 0
    for bit in bitArr:
        value <<= 1
        value += bit
    return value


def decoded_pixel(x, y, lx, ly, matrix, default):
    binary = []

    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if 0 <= j < ly and 0 <= i < lx:
                binary.append(matrix[j][i])
            else:
                binary.append(default)
    assert len(binary) == 9
    return bit_arr_to_dec(binary)


################################################################################


def day20p1():
    data = get_input(parse1, test=False)

    encoding = data[0]

    image = [[int(c == '#') for c in line] for line in data[2:]]

    len_x = len(image[0])
    len_y = len(image)

    print('Lens', len_x, len_y)

    turns = 2
    for t in range(turns):
        tmp = []
        len_x = len(image[0])
        len_y = len(image)
        for j in range(-3, len(image)+3):
            nr = []
            for i in range(-3, len(image[0])+3):
                encoded_pix = decoded_pixel(i, j, len_x, len_y, image, t & 1)
                nr.append(int(encoding[encoded_pix] == '#'))
            tmp.append(nr)
        image = tmp

    print('--------------')
    s = 0
    for r in image:
        print(''.join('#' if b == 1 else '.' for b in r))
        s += sum(r)
    print('--------------')

    return s


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day20p2():
    data = get_input(parse2, test=False)

    encoding = data[0]

    image = [[int(c == '#') for c in line] for line in data[2:]]

    len_x = len(image[0])
    len_y = len(image)

    print('Lens', len_x, len_y)

    turns = 50
    for t in range(turns):
        tmp = []
        len_x = len(image[0])
        len_y = len(image)
        for j in range(-3, len(image)+3):
            nr = []
            for i in range(-3, len(image[0])+3):
                encoded_pix = decoded_pixel(i, j, len_x, len_y, image, t & 1)
                nr.append(int(encoding[encoded_pix] == '#'))
            tmp.append(nr)
        image = tmp

    return sum((sum(r) for r in image))


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 20 - Part 1", '-'*n)
    print('Result =>', day20p1())
    print()
    print('-'*(n), "Day 20 - Part 2", '-'*n)
    print('Result =>', day20p2())
    print()


main()

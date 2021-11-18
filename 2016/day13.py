import random
import math


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


def parse1(line):
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


"""
If the number of bits that are 1 is even, it's an open space.
If the number of bits that are 1 is odd, it's a wall.
"""


def is_open_space(number: int):
    return len(list(filter(lambda x: x == '1', bin(number)))) % 2 == 0


def is_wall(number: int):
    return len(list(filter(lambda x: x == '1', bin(number)))) % 2 == 1


def formula(x, y, favorite_number): return (
    x*x + 3*x + 2*x*y + y + y*y) + favorite_number

################################################################################


def draw():
    # steps for part 1
    steps1 = [(1, 1), (35, 34), (11, 11), (33, 27), (22, 19), (35, 29), (36, 34), (16, 14), (24, 22), (36, 30), (38, 37), (37, 35), (10, 8), (34, 29), (22, 20), (6, 7), (5, 5), (10, 7), (35, 33), (29, 22), (30, 24), (11, 13), (36, 39), (33, 25), (38, 38), (22, 17), (31, 24), (2, 3), (8, 7), (33, 28), (25, 21), (6, 5), (5, 3), (21, 15), (32, 25), (19, 16), (38, 35), (22, 18), (16, 13), (36, 29), (38, 36), (15, 13), (16, 16), (13, 13), (27, 21),
              (6, 6), (23, 22), (7, 7), (14, 13), (19, 15), (29, 23), (21, 16), (17, 16), (32, 40), (1, 2), (11, 10), (3, 3), (12, 13), (33, 26), (37, 39), (22, 16), (35, 40), (18, 16), (33, 40), (23, 21), (16, 15), (2, 2), (33, 29), (36, 31), (37, 34), (25, 22), (10, 9), (9, 7), (22, 21), (5, 4), (26, 21), (31, 39), (35, 32), (34, 40), (11, 9), (32, 24), (29, 21), (32, 39), (35, 39), (11, 12), (36, 32), (38, 39), (28, 21), (4, 3), (29, 24), (20, 15)]
    # steps for part 2
    steps2 = [(1, 1), (16, 6), (11, 11), (17, 7), (22, 19), (20, 7), (1, 6), (2, 5), (23, 7), (10, 8), (9, 0), (6, 7), (5, 5), (10, 7), (16, 3), (7, 6), (0, 4), (1, 1), (22, 3), (3, 2), (23, 10), (4, 5), (11, 0), (16, 0), (25, 21), (17, 13), (21, 18), (13, 10), (25, 10), (23, 19), (21, 15), (23, 9), (16, 13), (14, 8), (13, 0), (19, 8), (17, 8), (15, 13), (16, 16), (13, 13), (27, 21), (23, 22), (23, 3), (11, 10), (17, 6), (12, 13), (19, 7), (18, 5), (15, 0), (22, 16), (18, 16), (1, 5), (23, 21), (22, 7), (2, 2), (23, 6), (10, 9), (9, 7), (5, 4), (11, 9), (17, 1), (14, 6), (13, 6), (18, 6), (0, 5), (3, 5), (23, 5), (4, 6),
              (5, 7), (11, 3), (16, 1), (17, 12), (20, 15), (0, 2), (23, 18), (8, 0), (23, 8), (16, 14), (24, 22), (14, 9), (18, 1), (16, 17), (22, 20), (13, 12), (10, 0), (11, 13), (17, 5), (14, 10), (19, 6), (18, 2), (22, 17), (22, 4), (2, 3), (8, 7), (6, 5), (5, 3), (11, 7), (12, 0), (19, 16), (17, 0), (14, 7), (13, 5), (0, 6), (15, 6), (22, 18), (21, 7), (4, 7), (10, 11), (6, 6), (11, 2), (10, 6), (7, 7), (14, 13), (16, 2), (19, 15), (17, 3), (14, 0), (21, 16), (18, 8), (17, 16), (1, 2), (3, 3), (11, 1), (16, 15), (25, 22), (24, 10), (22, 21), (21, 19), (13, 11), (26, 21), (11, 12), (17, 4), (16, 12), (22, 5), (4, 3), (11, 6)]

    steps = steps2
    print('len', len(set(steps)))
    m_n = 56
    fv = 1352

    mx = [['.' for _ in range(m_n)] for _ in range(m_n)]

    for x in range(m_n):
        for y in range(m_n):
            if is_wall(formula(x, y, fv)):
                mx[y][x] = '#'

    for s in steps:
        mx[s[1]][s[0]] = 'O'

    print('  0123456789')
    i = 0
    for m in mx:
        print(str(i), ''.join(m))
        i += 1

    print('Exiting...')
    exit(0)


# draw()

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
BEST = []
LEN = math.inf


def findpath(x_start, y_start, steps, favorite_number, ex, ey):
    global LEN, BEST
    if x_start == ex and y_start == ey:
        if len(steps) < LEN:
            BEST = steps.copy()
            LEN = len(steps)
        return [], True

    if len(steps) >= LEN:
        return [], False

    for x, y in DIRECTIONS:
        tmp_x, tmp_y = x_start + x, y_start + y
        if tmp_x < 0 or tmp_y < 0:
            continue

        if (tmp_x, tmp_y) in steps:
            continue

        if is_wall(formula(tmp_x, tmp_y, favorite_number)):
            continue

        findpath(tmp_x, tmp_y, steps.union(
            [(tmp_x, tmp_y)]), favorite_number, ex, ey)

    return [], False


def day13p1():
    is_test = False

    # start
    x, y = 1, 1

    # Modify variables
    favorite_number = 1352
    end_x, end_y = 31, 39
    if is_test:
        favorite_number = 10
        end_x, end_y = 7, 4

    steps = set()
    findpath(x, y, steps, favorite_number, end_x, end_y)

    return LEN, BEST
################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


LOCATIONS = set()


def locations(x_start, y_start, steps, favorite_number):
    if len(steps) <= 50:
        LOCATIONS.update(steps)

    if len(steps) > 50:
        return

    for x, y in DIRECTIONS:
        tmp_x, tmp_y = x_start + x, y_start + y
        if tmp_x < 0 or tmp_y < 0:
            continue

        if (tmp_x, tmp_y) in steps:
            continue

        if is_wall(formula(tmp_x, tmp_y, favorite_number)):
            continue

        locations(tmp_x, tmp_y, steps.union([(tmp_x, tmp_y)]), favorite_number)


################################################################################


def day13p2():
    is_test = False

    # Modify variables
    favorite_number = 1352
    if is_test:
        favorite_number = 10

    locations(1, 1, set(), favorite_number)

    print(LOCATIONS)

    return len(LOCATIONS)


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

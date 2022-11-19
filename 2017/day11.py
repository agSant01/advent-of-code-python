import collections
import sys


def get_filename(test=False):
    return f'day11_input{"_test" if test else ""}.txt'


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
    return line.split(',')

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


DIAGONALS = {
    'se': 'nw',
    'nw': 'se',
    'sw': 'ne',
    'ne': 'sw',
    'n': 's',
    's': 'n'
}


def get_diagonal(direction):
    return DIAGONALS[direction]


SAME = {
    'nw': 'ne',
    'ne': 'nw',
    'sw': 'se',
    'se': 'sw',
}

MATCH = {
    'nw': 'n',
    'ne': 'n',
    'sw': 's',
    'se': 's',
}


def get_same(direction):
    if direction in ['s', 'n']:
        return None
    return SAME[direction]


OPOSITES = {
    's': 'n',
    'n': 's'
}
################################################################################


def day11p1():
    lines = get_input(parse1, test=True)

    steps_res = []
    for directions in lines:
        x, y, z = 0, 0, 0
        # s, q, r
        for direction in directions:
            if direction == 'n':
                x += 1
                z -= 1
            elif direction == 's':
                x -= 1
                z += 1
            elif direction == 'se':
                y += 1
                x -= 1
            elif direction == 'ne':
                y += 1
                z -= 1
            elif direction == 'sw':
                y -= 1
                z += 1
            elif direction == 'nw':
                y -= 1
                x += 1
        steps_res.append((abs(z)+abs(x)+abs(y))//2)

    return steps_res


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day11p2():
    lines = get_input(parse2, test=True)

    results = []
    for directions in lines:
        x, y, z = 0, 0, 0
        # s, q, r
        distances = []
        for direction in directions:
            if direction == 'n':
                x += 1
                z -= 1
            elif direction == 's':
                x -= 1
                z += 1
            elif direction == 'se':
                y += 1
                x -= 1
            elif direction == 'ne':
                y += 1
                z -= 1
            elif direction == 'sw':
                y -= 1
                z += 1
            elif direction == 'nw':
                y -= 1
                x += 1
            distances.append((abs(z)+abs(x)+abs(y))//2)

        results.append(max(distances))

    return results


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print('-'*(n), "Day 11 - Part 1", '-'*n)
        print('Result =>', day11p1())
        print()
    if run_two:
        print('-'*(n), "Day 11 - Part 2", '-'*n)
        print('Result =>', day11p2())
    print()


main()

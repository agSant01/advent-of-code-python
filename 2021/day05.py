import collections
from typing import Dict, List, Tuple


def get_filename(test=False):
    return f'day05_input{"_test" if test else ""}.txt'


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
    return tuple(map(lambda x: (int(x.split(',')[0]), int(x.split(',')[1])), line.split(' -> ')))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def show_coords(coords: dict):
    mx = max(map(lambda xy: xy[0], coords.keys()))
    my = max(map(lambda xy: xy[1], coords.keys()))
    print(mx, my)
    matrix = [['.' for _ in range(mx+1)] for _ in range(my+1)]
    for k, v in coords.items():
        matrix[k[0]][k[1]] = str(v)
    for k in matrix:
        print(''.join(k))


################################################################################


def day05p1():
    data: List[
        Tuple[
            Tuple[int, int],
            Tuple[int, int]
        ]
    ] = get_input(parse1, test=False)

    coordinates: Dict[Tuple[int, int], int] = collections.defaultdict(int)

    for a, b in data:
        if a[0] == b[0]:
            for i in range(min(a[1], b[1]), max(b[1], a[1])+1):
                coordinates[(i, a[0])] += 1
        if a[1] == b[1]:
            for i in range(min(a[0], b[0]), max(a[0], b[0])+1):
                coordinates[(a[1], i)] += 1

    # show_coords(m)

    return len(list(filter(lambda x: x[1] >= 2, coordinates.items())))

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day05p2():
    data = get_input(parse2, test=False)
    m = collections.defaultdict(int)
    for a, b in data:
        if a[0] != b[0] and a[1] != b[1]:
            deltax = 1 if b[0] > a[0] else -1
            deltay = 1 if b[1] > a[1] else -1
            sx = a[0]
            sy = a[1]
            while sx != b[0]+deltax:
                m[(sy, sx)] += 1
                sx += deltax
                sy += deltay
        elif a[0] == b[0]:
            for i in range(min(a[1], b[1]), max(b[1], a[1])+1):
                m[(i, a[0])] += 1
        elif a[1] == b[1]:
            for i in range(min(a[0], b[0]), max(a[0], b[0])+1):
                m[(a[1], i)] += 1

    # show_coords(m)

    return len(list(filter(lambda x: x[1] >= 2, m.items())))


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 05 - Part 1", '-'*n)
    print('Result =>', day05p1())
    print()
    print('-'*(n), "Day 05 - Part 2", '-'*n)
    print('Result =>', day05p2())
    print()


main()

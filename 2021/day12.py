import copy
import collections
from os import path
from typing import Dict, List


def get_filename(test=False):
    return f'day12_input{"_test" if test else ""}.txt'


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
    return line.split('-')


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################

paths = []


def occurrences(items: list):
    freq_map = collections.defaultdict(int)
    for i in items:
        freq_map[i] += 1

    occs = collections.defaultdict(int)

    for v in freq_map.values():
        occs[v] += 1

    return occs


def find_all_paths(start, end, path: List[str], vertices: Dict[str, List[str]], part: int) -> None:
    global paths

    if start == end:
        paths.append(tuple(path))
        return

    if part == 2:
        if path.count('start') > 1:
            return

        if path.count('end') > 1:
            return

    for vert in vertices[start]:
        if part == 1:
            if vert.islower() and vert in path:
                continue
        elif part == 2:
            if vert.islower() and path.count(vert) + 1 >= 2:
                tmp = list(filter(lambda x: x.islower() and x !=
                                  'start' and x != 'end', path+[vert]))
                occ = occurrences(tmp)

                if len(tmp) > 0 and occ[2] > 1:
                    continue

                if len(tmp) > 0 and occ[3] > 0:
                    continue

        find_all_paths(vert, end, path + [vert], vertices, part)


################################################################################

def day12p1():
    global paths
    data = get_input(parse1, test=False)

    vertices = collections.defaultdict(list)

    for edge in data:
        vertices[edge[0]].append(edge[1])
        vertices[edge[1]].append(edge[0])

    # print(vertices)

    paths = []
    find_all_paths('start', 'end', ['start'], vertices, 1)

    return len(paths)

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day12p2():
    global paths

    test = False
    data = get_input(parse2, test)

    vertices = collections.defaultdict(list)

    for edge in data:
        vertices[edge[0]].append(edge[1])
        vertices[edge[1]].append(edge[0])

    print(vertices)

    paths = []
    find_all_paths('start', 'end', ['start'], vertices, 2)

    if test:
        print(paths)

        for p in sorted(paths):
            print(p)

    return len(paths)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 12 - Part 1", '-'*n)
    print('Result =>', day12p1())
    print()
    print('-'*(n), "Day 12 - Part 2", '-'*n)
    print('Result =>', day12p2())
    print()


main()

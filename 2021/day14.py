import collections
import copy
import functools


def get_filename(test=False):
    return f'day14_input{"_test" if test else ""}.txt'


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
    line = line.split(' -> ')
    if len(line) == 0:
        return None
    if len(line) == 1:
        return line[0]

    return line[0], line[1]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_polymer(start: str, mapping, steps):
    pairs = collections.defaultdict(int)
    letters = collections.defaultdict(int)

    for char in start:
        letters[char] += 1

    for pair in zip(start, start[1:]):
        pairs[''.join(pair)] += 1

    for _ in range(steps):
        tmp = collections.defaultdict(int)
        for pair in pairs.copy():
            pair = ''.join(pair)
            letters[mapping[pair]] += pairs[pair]
            tmp[pair[0] + mapping[pair]] += pairs[pair]
            tmp[mapping[pair] + pair[1]] += pairs[pair]
        pairs = tmp

    items = letters.items()

    _, mx = max(items, key=lambda x: x[1])
    _, min_ = min(items, key=lambda x: x[1])

    return mx - min_

################################################################################


def day14p1():
    data = get_input(parse1, test=False)

    start = data[0]
    mapping = {}

    for p, i in data[2:]:
        mapping[p] = i

    return get_polymer(start, mapping, 10)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day14p2():
    data = get_input(parse2, test=False)

    start = data[0]
    mapping = {}

    for p, i in data[2:]:
        mapping[p] = i

    return get_polymer(start, mapping, 40)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 14 - Part 1", '-'*n)
    print('Result =>', day14p1())
    print()
    print('-'*(n), "Day 14 - Part 2", '-'*n)
    print('Result =>', day14p2())
    print()


main()

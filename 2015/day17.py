import itertools
import collections
from collections import defaultdict

from numpy.core.defchararray import count


def get_filename(test=False):
    return f'day17_input{"_test" if test else ""}.txt'


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
    return int(line)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################

TARGET_LITTERS = 150

MCOUNT = 0
MCCOUNT = 0


def sum_rec(items: list, cumulative_liters: int, curr_permutation: set, next_container_pos: int):
    global MCOUNT, MCCOUNT
    item_len = len(items)

    permutation_collection = []
    MCCOUNT += 1

    while next_container_pos < item_len and \
            cumulative_liters+items[next_container_pos] <= TARGET_LITTERS and \
            next_container_pos not in curr_permutation:
        MCOUNT += 1
        sub_permutations_ = sum_rec(items, cumulative_liters,
                                    curr_permutation.copy(), next_container_pos+1)
        permutation_collection.extend(sub_permutations_)

        cumulative_liters += items[next_container_pos]
        curr_permutation.add(next_container_pos)

        next_container_pos += 1

    if cumulative_liters == TARGET_LITTERS:
        permutation_collection.append(curr_permutation)

    return permutation_collection


def sol1(data: list):
    data_ = sorted(data)
    total_combinations = set()

    i = 0
    data_len = len(data_)
    while i < data_len:
        t = sum_rec(data_, data_[i], set([i]), i+1)
        if t:
            total_combinations.update([frozenset(item) for item in t])
        i += 1

    return total_combinations

################################################################################


def day17p1():
    global MCOUNT, MCCOUNT
    data = get_input(parse1, test=False)

    combinations = sol1(data)

    print('MCCOUNT', MCCOUNT, 'MCOUNT', MCOUNT)
    return ('Total', len(combinations))

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day17p2():
    data = get_input(parse2, test=False)

    combinations = sol1(data)

    d = collections.defaultdict(int)
    for i in combinations:
        d[len(i)] += 1

    return ('Min combs', d.get(min(d.keys() or [0])))


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 17 - Part 1", '-'*n)
    print('Result =>', day17p1())
    print()
    print('-'*(n), "Day 17 - Part 2", '-'*n)
    print('Result =>', day17p2())
    print()


main()

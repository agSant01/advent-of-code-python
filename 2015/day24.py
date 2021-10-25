import functools
import operator
import math
import itertools


def get_filename(test=False):
    return f'day24_input{"_test" if test else ""}.txt'


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


################################################################################


def qe(it: list):
    return functools.reduce(operator.mul, it)


def find_gs(total, items):
    items_ = sorted(items)

    r = total
    t = []
    while len(items_) > 0:
        i = items_.pop()
        if i <= r:
            r -= i
            t.append(i)
        # print(t, r)

    # print('t', t, 'r', r)

    return t, r == 0


find_gs(20, [10, 8, 2,  7, 5, 4, 3, 1])


def day24p1():
    data = get_input(parse1, test=False)
    data = set(data)
    print(data)

    min_qe = math.inf
    min_front_item = math.inf

    for k in range(1, len(data)):
        if k > min_front_item:
            continue
        for comb in itertools.combinations(data, k):
            total_sum = sum(comb)

            if total_sum != sum(data)/3:
                continue

            if qe(comb) < min_qe:
                min_qe = qe(comb)
                min_front_item = k

    return 'QE', min_qe, 'ITEMS', min_front_item
################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day24p2():
    data = get_input(parse2, test=False)
    data = set(data)
    print(data)

    min_qe = math.inf
    min_front_item = math.inf

    for k in range(1, len(data)):
        if k > min_front_item:
            continue
        for comb in itertools.combinations(data, k):
            total_sum = sum(comb)

            if total_sum != sum(data)/4:
                continue

            if qe(comb) < min_qe:
                min_qe = qe(comb)
                min_front_item = k

    return 'QE', min_qe, 'ITEMS', min_front_item


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 24 - Part 1", '-'*n)
    print('Result =>', day24p1())
    print()
    print('-'*(n), "Day 24 - Part 2", '-'*n)
    print('Result =>', day24p2())
    print()


main()

"""
Problem Statement: https://adventofcode.com/2015/day/13
"""


import itertools
import sys


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
    line = line \
        .replace('happiness units by sitting next to', '') \
        .replace('would', '') \
        .replace('.', '') \
        .split()
    guest, sign, amount, side = line
    amount = int(amount)
    if sign == 'lose':
        amount *= -1

    return (guest, amount, side)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def create_happiness_matrix(guests: int, data, gm):
    happiness = [[0 for _ in range(guests)] for _ in range(guests)]

    for i in range(guests):
        happiness[i][i] = 0

    for edge in data:
        fromV = gm[edge[0]]
        toV = gm[edge[2]]
        cost = edge[1]
        happiness[fromV][toV] = cost

    return happiness


def calculate_best_happiness(guests, happiness):
    # calculate the paths of every permutation
    result = 0
    success_perm = None
    costs = []
    for permutation in itertools.permutations(range(guests)):
        cost = 0
        permutation = list(permutation)
        previous = permutation[-1]
        cost_ = []
        for node in permutation:
            cost += happiness[previous][node]
            cost_.append(happiness[previous][node])
            previous = node
        previous = permutation[0]
        for node in reversed(permutation):
            cost_.append(happiness[previous][node])
            cost += happiness[previous][node]
            previous = node
        if cost > result:
            result = cost
            costs = cost_.copy()
            success_perm = permutation

    return result, success_perm, costs
################################################################################


def day13p1():
    data = get_input(parse1, test=False)
    guests_set = set()
    gm = dict()

    for d in data:
        guests_set.add(d[0])

    for idx, g in enumerate(sorted(guests_set)):
        gm.update({g: idx})

    guests = len(guests_set)

    happiness = create_happiness_matrix(guests, data, gm)

    result, success_perm, costs = calculate_best_happiness(guests, happiness)

    print('perm', success_perm, 'costs', costs, 'map', gm)

    return result


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
    data = get_input(parse1, test=False)
    guests_set = set()
    gm = dict()

    for d in data:
        guests_set.add(d[0])

    guests_set.add('Me')

    for idx, g in enumerate(sorted(guests_set)):
        gm.update({g: idx})

    guests = len(guests_set)

    happiness = create_happiness_matrix(guests, data, gm)

    result, success_perm, costs = calculate_best_happiness(guests, happiness)

    print('perm', success_perm, 'costs', costs, 'map', gm)

    return result


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

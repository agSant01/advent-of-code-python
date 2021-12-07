import math


def get_filename(test=False):
    return f'day07_input{"_test" if test else ""}.txt'


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
    return list(map(int, line.split(',')))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day07p1():
    input = get_input(parse1, test=False)[0]

    total = len(input)

    median = sorted(input)[total//2]

    cost = 0
    for crab in input:
        cost += abs(crab-median)

    return cost

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day07p2():
    input = get_input(parse2, test=False)[0]

    total = len(input)

    avg = sum(input)//total

    total_fuel = 0
    for crab in input:
        delta = abs(crab-avg)
        total_fuel += delta*(delta+1) // 2

    return total_fuel


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 07 - Part 1", '-'*n)
    print('Result =>', day07p1())
    print()
    print('-'*(n), "Day 07 - Part 2", '-'*n)
    print('Result =>', day07p2())
    print()


main()

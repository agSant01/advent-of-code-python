import math
from os import access, curdir


def get_filename(test=False):
    return f'day19_input{"_test" if test else ""}.txt'


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


def pp(s):
    s_ = ''.join(['#' if c == 1 else '.' for c in s])
    print(s_)

################################################################################


def day19p1():
    elves = get_input(parse1, test=False)[0]

    cnt = 0
    for elves in range(3, elves+1):
        cnt += 2
        if math.log2(elves) == int(math.log2(elves)):
            cnt = 0

    return cnt+1


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day19p2():
    elves = get_input(parse2, test=False)[0]

    i = 1
    while i * 3 < elves:
        i *= 3

    return elves-i


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 19 - Part 1", '-'*n)
    print('Result =>', day19p1())
    print()
    print('-'*(n), "Day 19 - Part 2", '-'*n)
    print('Result =>', day19p2())
    print()


main()

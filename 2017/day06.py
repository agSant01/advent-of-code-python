from itertools import cycle
import sys


def get_filename(test=False):
    return f'day06_input{"_test" if test else ""}.txt'


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
    return [int(n) for n in line.split()]

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day06p1():
    data = get_input(parse1, test=False)[0]

    states = set()
    cycles = 0
    curr_state = data
    bounds = len(curr_state)

    while tuple(curr_state) not in states:
        states.add(tuple(curr_state))
        i_m = 0
        max_ = curr_state[0]
        for idx, mem in enumerate(curr_state):
            if mem > max_:
                i_m = idx
                max_ = mem

        to_spread = curr_state[i_m]
        curr_state[i_m] = 0
        i_m += 1

        while to_spread > 0:
            curr_state[i_m % bounds] += 1
            to_spread -= 1
            i_m += 1
        cycles += 1

    return cycles


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day06p2():
    data = get_input(parse2, test=False)[0]

    states = {}
    cycles = 0
    curr_state = data
    bounds = len(curr_state)

    while tuple(curr_state) not in states:
        states.update({tuple(curr_state): cycles})
        i_m = 0
        max_ = curr_state[0]
        for idx, mem in enumerate(curr_state):
            if mem > max_:
                i_m = idx
                max_ = mem

        to_spread = curr_state[i_m]
        curr_state[i_m] = 0
        i_m += 1

        while to_spread > 0:
            curr_state[i_m % bounds] += 1
            to_spread -= 1
            i_m += 1
        cycles += 1

    return cycles - states[tuple(curr_state)]


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
        print('-'*(n), "Day 06 - Part 1", '-'*n)
        print('Result =>', day06p1())
        print()
    if run_two:
        print('-'*(n), "Day 06 - Part 2", '-'*n)
        print('Result =>', day06p2())
    print()


main()

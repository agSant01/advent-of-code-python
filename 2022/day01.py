import sys


def get_filename(test=False):
    return f'day01_input{"_test" if test else ""}.txt'


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
    return int(line) if line else None

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day01p1():
    data = get_input(parse1, test=False)
    agg = 0
    max_ = 0
    max_idx = 0
    idx = 1
    for d in data:
        if d is None:
            if agg > max_:
                max_idx = idx
                max_ = agg
            agg = 0
            idx += 1
        else:
            agg += d
    return max_idx, max_

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day01p2():
    data = get_input(parse2, test=False)
    agg_list = []
    agg = 0
    for d in data:
        if d is None:
            agg_list.append(agg)
            agg = 0
        else:
            agg += d
    return sum(sorted(agg_list)[-3:])


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
        print('-'*(n), "Day 01 - Part 1", '-'*n)
        print('Result =>', day01p1())
        print()
    if run_two:
        print('-'*(n), "Day 01 - Part 2", '-'*n)
        print('Result =>', day01p2())
    print()


main()

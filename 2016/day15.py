import re


def get_filename(test=False):
    return f'day15_input{"_test" if test else ""}.txt'


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
PARSE1 = re.compile('Disc #(\d+) has (\d+) positions.*position (\d*)')


def parse1(line: str):
    return list(map(lambda a: int(a), PARSE1.findall(line)[0]))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def reaches_end(start_time, discs):
    for disk in discs:
        start_time += 1
        curr_pos = (disk[2] + start_time) % disk[1]

        if curr_pos != 0:
            return False

    return True

################################################################################


def day15p1():
    data = get_input(parse1, test=False)

    start_time = 0

    while True:
        if reaches_end(start_time, data):
            break
        start_time += 1

    return "Win at: {}".format(start_time)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day15p2():
    data = get_input(parse2, test=False)

    start_time = 0

    data.append([0, 11, 0])

    while True:
        if reaches_end(start_time, data):
            break
        start_time += 1

    return "Win at: {}".format(start_time)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 15 - Part 1", '-'*n)
    print('Result =>', day15p1())
    print()
    print('-'*(n), "Day 15 - Part 2", '-'*n)
    print('Result =>', day15p2())
    print()


main()

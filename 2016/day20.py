from os import curdir


def get_filename(test=False):
    return f'day20_input{"_test" if test else ""}.txt'


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
    return list(map(int, line.split('-')))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day20p1():
    data = get_input(parse1, test=False)
    data = sorted(data, key=lambda x: x[0])

    for i in range(1, len(data)):
        prev = data[i-1]
        curr = data[i]

        if curr[0] < prev[1]:
            curr[0] = prev[1]

        if curr[0] > curr[1]:
            curr[1] = curr[0]

        if prev[1] + 1 < curr[0]:
            return prev[1] + 1

    return None

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################
################################################################################


def day20p2():
    data = get_input(parse2, test=False)
    data = sorted(data, key=lambda x: x[0])

    last_ip = 2**32 - 1
    allowed = 0

    for i in range(1, len(data)):
        prev = data[i-1]
        curr = data[i]

        if curr[0] < prev[1]:
            curr[0] = prev[1]

        if curr[0] > curr[1]:
            curr[1] = curr[0]

        if prev[1] + 1 < curr[0]:
            allowed += curr[0] - prev[1] - 1

    return allowed + (last_ip - data[-1][0])


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 20 - Part 1", '-'*n)
    print('Result =>', day20p1())
    print()
    print('-'*(n), "Day 20 - Part 2", '-'*n)
    print('Result =>', day20p2())
    print()


main()

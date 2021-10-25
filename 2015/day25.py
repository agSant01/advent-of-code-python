def get_filename(test=False):
    return f'day25_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_next(code):
    return code * 252533 % 33554393


def get_code(start, row, column):
    d = column + row - 1

    iterations = sum(i for i in range(1, d+1)) - row + 1

    for _ in range(1, iterations):
        start = get_next(start)

    return start

################################################################################


def day25p1():
    data = get_input(parse1, test=True)

    is_test = False

    start = 20151125

    column = 3083
    row = 2978
    if is_test:
        column = 6
        row = 6

    x = get_code(start, row, column)

    return x

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day25p2():
    data = get_input(parse2, test=True)
    for d in data:
        pass


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 25 - Part 1", '-'*n)
    print('Result =>', day25p1())
    print()
    print('-'*(n), "Day 25 - Part 2", '-'*n)
    print('Result =>', day25p2())
    print()


main()

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


def parse1(line):
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def calculate_captcha(string: str):
    cnt = 0
    for first, next_ in zip(string, string[1:]):
        if first == next_:
            cnt += int(first)

    if string[0] == string[-1]:
        cnt += int(string[0])
    return cnt


################################################################################
def day01p1():
    data = get_input(parse1, test=False)
    for d in data:
        print(d, calculate_captcha(d))

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def captcha_circular(string: str):
    steps = len(string) // 2
    len_ = len(string)

    # print('steps', steps)

    cnt: int = 0
    for i in range(len_):
        current = string[i]
        to_compare = string[(i+steps) % len_]
        if current == to_compare:
            cnt += int(current)

    return cnt


################################################################################


def day01p2():
    data = get_input(parse2, test=False)
    res = []
    for d in data:
        cap = captcha_circular(d)
        print(d, cap)
        res.append(cap)

    return res


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    run_one = any(arg == '1' for arg in sys.argv)
    run_two = any(arg == '2' for arg in sys.argv)

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

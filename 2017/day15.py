import sys
from ctypes import c_int16


def get_filename(test=False):
    return f'day15_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line):
    return int(line.split()[-1])


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def next_a(prev):
    # print((prev*16807) % ((2**32)-1))
    # print((prev*16807) % 2147483647)
    # print((prev*16807) >> 31)

    n = prev * 16807
    a = n & 2147483647
    b = n >> 31
    # return (prev*16807) % 2147483647
    return a + b


def next_b(prev):
    n = prev * 48271
    a = n & 2147483647
    b = n >> 31
    # return (prev*48271) % 2147483647
    return a + b


################################################################################


def day15p1():
    A, B = get_input(parse1, test=True)
    consider = 40_000_000
    # consider = 6
    matching_pairs = 0
    for _ in range(consider):
        A = next_a(A)
        B = next_b(B)
        # print(A, B)
        # print('-'*10)
        if c_int16(A ^ B).value == 0:
            matching_pairs += 1

    return matching_pairs


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


# Returns true if n is a multiple of 4.
def isMultipleOf4(n):
    if n == 0:
        return True
    return ((n >> 2) << 2) == n


# Returns true if n is a multiple of 4.
def isMultipleOf8(n):
    if n == 0:
        return True
    return ((n >> 3) << 3) == n


def next_a_by4(prev):
    # n = (prev*16807)
    # a = n & 2147483647
    # b = n >> 31
    n = (prev * 16807) % 2147483647
    # while (a+b) % 4 != 0:
    while not isMultipleOf4(n):
        # n *= 16807
        # a = n & 2147483647
        # b = n >> 31
        n = (n * 16807) % 2147483647

    # return a+b
    return n


def next_b_by8(prev):
    # n = (prev*48271)
    # a = n & 2147483647
    # b = n >> 31
    # while (a+b) % 8 != 0:
    n = (prev * 48271) % 2147483647
    while not isMultipleOf8(n):
        # n *= 48271
        # a = n & 2147483647
        # b = n >> 31
        n = (n * 48271) % 2147483647

    return n


################################################################################


def day15p2():
    A, B = get_input(parse2, test=True)
    consider = 5_000_000
    # consider = 1058
    matching_pairs = 0
    for _ in range(consider):
        A = next_a_by4(A)
        B = next_b_by8(B)
        if c_int16(A ^ B).value == 0:
            matching_pairs += 1

    return matching_pairs


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print("-" * (n), "Day 15 - Part 1", "-" * n)
        print("Result =>", day15p1())
        print()
    if run_two:
        print("-" * (n), "Day 15 - Part 2", "-" * n)
        print("Result =>", day15p2())
    print()


main()

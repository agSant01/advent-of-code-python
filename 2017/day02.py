import sys
from typing import List


def get_filename(test=False):
    return f'day02_input{"_test" if test else ""}.txt'


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
    return list(map(int, line.split()))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def min_max_diff(numbers):
    return max(numbers) - min(numbers)


def checksum(table_number):
    check = 0
    for row in table_number:
        check += min_max_diff(row)

    return check

################################################################################


def day02p1():
    data = get_input(parse1, test=False)

    return checksum(data)


################################################################################
############################### Start of Part 2 ################################
################################################################################

def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def find_divisible(numbers_row: List[int]):
    number_row_set = set(numbers_row)  # O(1) search time
    max_ = max(numbers_row)

    for number in number_row_set:  # O(N)
        mult = 2
        new_ = number
        while new_ <= max_:  # O(MAX)
            new_ = number*mult
            if new_ in number_row_set:  # find in set: O(1)
                print(new_, number, new_/number)
                return new_ // number
            mult += 1

    # Total Complexity - Worst: O(N * MAX_NUMBER)


def divisible_checksum(table_numbers):
    check = 0
    for row in table_numbers:
        check += find_divisible(row)
    return check

################################################################################


def day02p2():
    data = get_input(parse2, test=False)
    return divisible_checksum(data)


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
        print('-'*(n), "Day 02 - Part 1", '-'*n)
        print('Result =>', day02p1())
        print()
    if run_two:
        print('-'*(n), "Day 02 - Part 2", '-'*n)
        print('Result =>', day02p2())
    print()


main()

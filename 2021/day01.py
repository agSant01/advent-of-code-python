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
    return int(line)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day01p1():
    scan_data = get_input(parse1, test=False)
    prev = scan_data[0]
    increment = 0
    for point in scan_data:
        increment += (point > prev)
        prev = point
    return increment
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
    scan_data = get_input(parse2, test=False)

    prev = sum(scan_data[0:3])
    increment = 0
    for i in range(0, len(scan_data)-2):
        window_sum = sum(scan_data[i:i+3])
        increment += (window_sum > prev)
        prev = window_sum
    return increment


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 01 - Part 1", '-'*n)
    print('Result =>', day01p1())
    print()
    print('-'*(n), "Day 01 - Part 2", '-'*n)
    print('Result =>', day01p2())
    print()


main()

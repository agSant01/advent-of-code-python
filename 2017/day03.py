import math
import sys
from turtle import width


def get_filename(test=False):
    return f'day03_input{"_test" if test else ""}.txt'


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


def get_outer_rim(memory_address: int):
    number = math.ceil(math.sqrt(memory_address))
    return number//2


def find_steps(memory_address: int):
    if memory_address == 1:
        return 0

    outer_rim_level = get_outer_rim(memory_address)

    square_number = 2*outer_rim_level+1
    last_in_level = square_number*square_number

    bottom = [last_in_level-square_number+1, last_in_level]
    left = [last_in_level-2*(square_number-1), bottom[0]]
    top = [last_in_level-3*(square_number-1), left[0]]
    right = [last_in_level-4*(square_number-1)+1, top[0]]

    # print('addr', memory_address, 'lvl', outer_rim_level)
    # print(right, top, left, bottom,)

    if memory_address >= bottom[0] and memory_address <= bottom[1]:
        # memory is bottom of grid
        steps_x = abs(memory_address - (bottom[0] + bottom[1])//2)
        steps_y = (outer_rim_level)
    elif memory_address >= top[0] and memory_address <= top[1]:
        steps_x = abs(memory_address - (top[0] + top[1]) // 2)
        steps_y = (outer_rim_level)
    elif memory_address >= right[0] and memory_address <= right[1]:
        # memory is right of grid
        steps_x = outer_rim_level
        steps_y = abs(memory_address - (right[0] + right[1])//2)
    elif memory_address >= left[0] and memory_address <= left[1]:
        steps_x = outer_rim_level
        steps_y = abs(memory_address - (left[0] + left[1])//2)

    return int(steps_x+steps_y)

################################################################################


def day03p1():
    data = get_input(parse1, test=False)
    # for d in data:
    #     print(d, find_steps(d))
    return data[0], find_steps(data[0])

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def generate_layer(layer_num: int):
    layer_addresses = max(1, 8*layer_num)
    return [0] * layer_addresses


################################################################################


def day03p2():
    data = get_input(parse2, test=True)

    # value = 368078
    value = 100

    curr_layer = generate_layer(0)
    next_layer = generate_layer(1)

    curr_address = [0, 0]

    address = 1

    while curr < value:
        print(address, curr)
        tmp = curr
        curr += prev
        prev = tmp
        address += 1


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
        print('-'*(n), "Day 03 - Part 1", '-'*n)
        print('Result =>', day03p1())
        print()
    if run_two:
        print('-'*(n), "Day 03 - Part 2", '-'*n)
        print('Result =>', day03p2())
    print()


main()

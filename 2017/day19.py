import sys
from typing import List


def get_filename(test=False):
    return f'day19_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    return [c for c in line[:-1]]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

DIRECTIONS = {
    "LEFT": LEFT,
    "RIGHT": RIGHT,
    "UP": UP,
    "DOWN": DOWN,
}


def add(ta, tb):
    return (ta[0] + tb[0], ta[1] + tb[1])


def get_order(network: List[str]):
    start_spot = network[0].index("|")
    current_coordinate = (0, start_spot)
    direction = "DOWN"
    steps = 0
    lst = []
    while True:
        r, c = current_coordinate
        current_value = network[r][c]
        if current_value == "|" or current_value == "-":
            current_coordinate = add(current_coordinate, DIRECTIONS[direction])
        elif current_value.isalpha():
            lst.append(current_value)
            current_coordinate = add(current_coordinate, DIRECTIONS[direction])
        elif current_value == "+":
            if direction in ("LEFT", "RIGHT"):
                if network[r + 1][c] != " ":
                    current_coordinate = add(current_coordinate, DOWN)
                    direction = "DOWN"
                elif network[r - 1][c] != " ":
                    current_coordinate = add(current_coordinate, UP)
                    direction = "UP"
            elif direction in ("UP", "DOWN"):
                if network[r][c + 1] != " ":
                    direction = "RIGHT"
                    current_coordinate = add(current_coordinate, RIGHT)
                elif network[r][c - 1] != " ":
                    direction = "LEFT"
                    current_coordinate = add(current_coordinate, LEFT)
        else:
            break
        steps += 1

    return lst, steps


################################################################################


def day19p1():
    network: List[str] = get_input(parse1, test=False)
    return "".join(get_order(network)[0])


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day19p2():
    network: List[str] = get_input(parse2, test=False)
    order, steps = get_order(network)
    return "->".join(order), steps


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
        print("-" * (n), "Day 19 - Part 1", "-" * n)
        print("Result =>", day19p1())
        print()
    if run_two:
        print("-" * (n), "Day 19 - Part 2", "-" * n)
        print("Result =>", day19p2())
    print()


main()

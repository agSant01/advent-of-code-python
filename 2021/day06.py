import copy
from typing import List


def get_filename(test=False):
    return f'day06_input{"_test" if test else ""}.txt'


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


def parse1(line: str):
    return list(map(int, line.split(",")))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day06p1():
    data = get_input(parse1, test=False)[0]
    usage = copy.deepcopy(data)

    for _ in range(80):
        tmp = copy.copy(usage)
        for idx, lant in enumerate(tmp.copy()):
            if lant == 0:
                tmp.append(8)
                tmp[idx] = 6
            else:
                tmp[idx] -= 1
        usage = tmp
    return len(usage)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day06p2():
    data: list = get_input(parse2, test=False)[0]

    # Key will be the REPRODUCTION COUNTER. Value will be the quantity of Lanterns
    lanternsCount: List[int] = [0 for _ in range(9)]

    # Lantern Dict Bucket Count
    for lantern in data:
        lanternsCount[lantern] += 1

    MX_DAYS = 256
    for _ in range(MX_DAYS):
        new_spawn = lanternsCount.pop(0)
        lanternsCount[6] += new_spawn
        lanternsCount.append(new_spawn)

    return sum(lanternsCount)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 06 - Part 1", "-" * n)
    print("Result =>", day06p1())
    print()
    print("-" * (n), "Day 06 - Part 2", "-" * n)
    print("Result =>", day06p2())
    print()


main()

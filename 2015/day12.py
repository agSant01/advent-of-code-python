import json
import re


def get_filename(test=False):
    return f'day12_input{"_test" if test else ""}.txt'


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
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


COMP = re.compile("-?[0-9]+")
################################################################################


def day12p1():
    data = get_input(parse1, test=False)
    data = "".join(data)

    m = COMP.findall(data)
    print(len(list(m)))
    res = sum([int(i) for i in m])

    return ("Total Sum", res)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def rec_analize(object):
    if type(object) == type(dict()):
        if "red" in object.values():
            return 0
        return sum(map(rec_analize, object.values()))

    if type(object) == type(0):
        return object

    if type(object) == type(list()):
        return sum(map(rec_analize, object))

    return 0


################################################################################


def day12p2():
    data = get_input(parse2, test=False)

    data = json.loads("".join(data))

    r = rec_analize(data)

    return ("Total Sum", r)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 12 - Part 1", "-" * n)
    print("Result =>", day12p1())
    print()
    print("-" * (n), "Day 12 - Part 2", "-" * n)
    print("Result =>", day12p2())
    print()


main()

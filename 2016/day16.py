import copy
import functools


def get_filename(test=False):
    return f'day16_input{"_test" if test else ""}.txt'


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


def neg(bit: str):
    if bit == "0":
        return "1"
    if bit == "1":
        return "0"


@functools.lru_cache()
def dragon_curve(initial: str, max_len=0):
    len_ = len(initial)
    max_len = max(len_, max_len)
    internal = copy.copy(initial)

    while len_ <= max_len:
        b: str = reversed(copy.copy(internal))
        b = "".join(map(neg, b))
        len_ += 1 + len(b)
        internal += "0" + b

    return internal


@functools.lru_cache()
def checksum(bitstring: str):
    i = 0
    resulting = ""
    while i < len(bitstring):
        c = bitstring[i : i + 2]
        if c[0] == c[1]:
            resulting += "1"
        else:
            resulting += "0"
        i += 2

    return resulting


################################################################################


def day16p1():
    data = "01111010110010011"

    max_len = 272
    data = dragon_curve(data, max_len)

    data = data[:max_len]

    chk = checksum(data)
    while len(chk) % 2 == 0:
        chk = checksum(chk)

    return data, chk


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day16p2():
    data = "01111010110010011"

    max_len = 35651584
    data = dragon_curve(data, max_len)

    data = data[:max_len]

    chk = copy.copy(data)
    while len(chk) % 2 == 0:
        chk = checksum(chk)

    return chk


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 16 - Part 1", "-" * n)
    print("Result =>", day16p1())
    print()
    print("-" * (n), "Day 16 - Part 2", "-" * n)
    print("Result =>", day16p2())
    print()


main()

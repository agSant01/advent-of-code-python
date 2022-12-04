import hashlib

import yearutils as yu


def get_filename(test=False):
    return f'day04_input{"_test" if test else ""}.txt'


def parse(line):
    return line


def day04p1():
    input = yu.get_input(get_filename(test=False), parse)[0]
    i = 0
    while True:
        toH = input + str(i)

        hash = hashlib.md5(toH.encode())
        if hash.hexdigest()[:5] == "00000":
            print(toH, i, hash.hexdigest())
            return i
        i += 1


def day04p2():
    data = yu.get_input(get_filename(test=False), parse)[0]

    i = 0
    while True:
        toH = data + str(i)
        hash = hashlib.md5(toH.encode())
        if hash.hexdigest()[:6] == "000000":
            print(toH, i, hash.hexdigest())
            return i
        i += 1


def main():
    print("Day 04 - Part 1")
    print(day04p1())

    print("Day 04 - Part 2")
    print(day04p2())


main()

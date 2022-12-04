import yearutils as yu


def get_filename(test=False):
    return f'day01_input{"_test" if test else ""}.txt'


def parse(line):
    return line


def day01p1():
    result = yu.get_input(get_filename(test=False), parse)
    floor = 0
    for paren in result[0]:
        if paren == "(":
            floor += 1
        if paren == ")":
            floor -= 1
    return floor


def day01p2():
    result = yu.get_input(get_filename(test=False), parse)
    floor = 0
    for idx, paren in enumerate(result[0]):
        if paren == "(":
            floor += 1
        if paren == ")":
            floor -= 1

        if floor == -1:
            return idx + 1

    return None


def main():
    print("Day 01 - Part 1")
    print(day01p1())

    print("Day 01 - Part 2")
    print(day01p2())


main()

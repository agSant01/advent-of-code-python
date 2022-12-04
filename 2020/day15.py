def get_filename(test=False):
    return f'day15_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def parse1(line: str):
    return list(map(lambda x: int(x), line.strip().split(",")))


def day15p1():
    data = get_input(parse1, test=False)[0]
    print(data)

    history = {}
    ieth = 2020
    lastSpoken = None

    # initialize the hitory with given input
    for idx, item in enumerate(data):
        history[item] = idx + 1
        lastSpoken = item

    lastSpoken = data[-1]  # get last Spoken number

    for turn in range(len(data) + 1, ieth + 1):
        if lastSpoken in history:
            # number has been spoken before
            # get the age
            age = turn - history[lastSpoken] - 1
            history[lastSpoken] = turn - 1
            lastSpoken = age
        else:
            # set turn of last spoken as last
            history[lastSpoken] = turn - 1
            lastSpoken = 0

    return lastSpoken


def parse2(line):
    return parse1(line)


def day15p2():
    data = get_input(parse2, test=False)[0]

    print(data)

    history = {}
    ieth = 30000000
    lastSpoken = None

    # initialize the hitory with given input
    for idx, item in enumerate(data):
        history[item] = idx + 1
        lastSpoken = item

    lastSpoken = data[-1]  # get last Spoken number

    for turn in range(len(data) + 1, ieth + 1):
        if lastSpoken in history:
            # number has been spoken before
            # get the age
            age = turn - history[lastSpoken] - 1
            history[lastSpoken] = turn - 1
            lastSpoken = age
        else:
            # set turn of last spoken as last
            history[lastSpoken] = turn - 1
            lastSpoken = 0

    return lastSpoken


def main():
    print("Day 15 - Part 1")
    print(day15p1())

    print("Day 15 - Part 2")
    print(day15p2())


main()

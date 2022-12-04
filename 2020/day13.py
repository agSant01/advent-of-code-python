

def get_filename(test=False):
    return f'day13_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def parse1(line: str):
    return list(map(lambda x: int(x), filter(lambda x: x.isnumeric(), line.split(","))))


def day13p1():
    data = get_input(parse1, test=False)

    timestamp = curr_ts = int(data[0][0])
    busses = data[1]

    print(timestamp, busses)

    while True:
        for bus in busses:
            if curr_ts % bus == 0:
                return bus * (curr_ts - timestamp)
        curr_ts += 1


def parse2(line):
    return line.split(",")


def day13p2():
    data = get_input(parse2, test=True)

    curr_ts = 0
    busses = data[1]
    valid = {}

    for i, bus in enumerate(busses):
        if bus.isnumeric():
            valid[int(bus)] = i

    sum_ = 1
    for i in valid.keys():
        sum_ *= i

    print(valid, sum_)

    while True:
        cnt = 0
        for bus, offset in valid.items():
            if (curr_ts + offset) % bus != 0:
                break
            cnt += 1
        # 1202161486
        # 5876813119
        # 293840655950000000
        # 5,876,813,119
        # 1,202,161,486
        if curr_ts % 10000000 == 0:
            print(curr_ts)

        if cnt == len(valid):
            return curr_ts

        curr_ts += int(sum_)


def main():
    print("Day 13 - Part 1")
    print(day13p1())

    print("Day 13 - Part 2")
    print(day13p2())


main()

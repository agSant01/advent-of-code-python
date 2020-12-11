import collections
import yearutils as yu


def get_filename(test=False):
    return f'day03_input{"_test" if test else ""}.txt'


def parse(line):
    return line


def day03p1():
    data = yu.get_input(get_filename(test=False), parse)

    houses = collections.defaultdict(int)

    current_coord = (0, 0)

    houses[current_coord] = 1

    # north (^), south (v), east (>), or west (<)
    for d in data[0]:
        x, y = current_coord
        if d == '^':
            current_coord = (x, y+1)
            houses[current_coord] += 1
        if d == '>':
            current_coord = (x+1, y)
            houses[current_coord] += 1
        if d == 'v':
            current_coord = (x, y-1)
            houses[current_coord] += 1
        if d == '<':
            current_coord = (x-1, y)
            houses[current_coord] += 1

    # houses at least 1
    return len(houses.keys())


def deliverToy(direction, curr_pos, houses):
    x, y = curr_pos
    current_coord = None
    if direction == '^':
        current_coord = (x, y+1)
        houses[current_coord] += 1
    if direction == '>':
        current_coord = (x+1, y)
        houses[current_coord] += 1
    if direction == 'v':
        current_coord = (x, y-1)
        houses[current_coord] += 1
    if direction == '<':
        current_coord = (x-1, y)
        houses[current_coord] += 1

    return current_coord


def day03p2():
    data = yu.get_input(get_filename(test=False), parse)

    santa_houses = collections.defaultdict(int)
    robosanta_houses = collections.defaultdict(int)

    santa_pos = (0, 0)
    robosanta_pos = (0, 0)

    santa_turn = True

    for d in data[0]:
        if santa_turn:
            santa_pos = deliverToy(d, santa_pos, santa_houses)
        else:
            robosanta_pos = deliverToy(d, robosanta_pos, robosanta_houses)

        santa_turn = not santa_turn

    return len(set(list(santa_houses.keys()) + list(robosanta_houses.keys())))


def main():
    print("Day 03 - Part 1")
    print(day03p1())

    print("Day 03 - Part 2")
    print(day03p2())


main()

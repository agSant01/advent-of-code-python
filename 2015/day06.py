import utils as ut


def get_filename(test=False):
    return f'day06_input{"_test" if test else ""}.txt'


def parse(line):
    '''
    turn off 199,133 through 461,193
    toggle 537,781 through 687,941
    turn on 226,196 through 599,390
    '''
    spl = line.split()

    res = None

    if spl[0] == 'turn':
        left = spl[2].split(',')
        right = spl[4].split(',')
        res = (spl[1], tuple(left), tuple(right))
    if spl[0] == 'toggle':
        left = spl[1].split(',')
        right = spl[3].split(',')
        res = (spl[0], tuple(left), tuple(right))

    return res


def turn(mtx, left, right, on):
    left_x, left_y = left
    right_x, right_y = right

    for x in range(int(left_x), int(right_x)+1):
        for y in range(int(left_y), int(right_y)+1):
            mtx[y][x] = on


def toggle(mtx, left, right):
    left_x, left_y = left
    right_x, right_y = right

    for x in range(int(left_x), int(right_x)+1):
        for y in range(int(left_y), int(right_y)+1):
            mtx[y][x] = not mtx[y][x]


def day06p1():
    data = ut.get_input(get_filename(test=False), parse)

    mtrx = [[False for i in range(1000)] for j in range(1000)]

    for (i, left, right) in data:
        if i in ['off', 'on']:
            o = i == 'on'
            turn(mtrx, left, right, on=o)
        elif i == 'toggle':
            toggle(mtrx, left, right)
        else:
            print('invalid:', i)
            exit(1)

    return sum([sum(i) for i in mtrx])


def turn2(mtx, left, right, on):
    left_x, left_y = left
    right_x, right_y = right

    for x in range(int(left_x), int(right_x)+1):
        for y in range(int(left_y), int(right_y)+1):
            if on:
                mtx[y][x] += 1
            else:
                mtx[y][x] = max(0, mtx[y][x]-1)


def toggle2(mtx, left, right):
    left_x, left_y = left
    right_x, right_y = right

    for x in range(int(left_x), int(right_x)+1):
        for y in range(int(left_y), int(right_y)+1):
            mtx[y][x] += 2


def day06p2():
    data = ut.get_input(get_filename(test=False), parse)

    mtrx = [[0 for i in range(1000)] for j in range(1000)]

    for (i, left, right) in data:
        if i in ['off', 'on']:
            o = i == 'on'
            turn2(mtrx, left, right, on=o)
        elif i == 'toggle':
            toggle2(mtrx, left, right)
        else:
            print('invalid:', i)
            exit(1)

    return sum([sum(i) for i in mtrx])


def main():
    print("Day 06 - Part 1")
    print(day06p1())

    print("Day 06 - Part 2")
    print(day06p2())


main()

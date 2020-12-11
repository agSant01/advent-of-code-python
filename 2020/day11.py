import utils as ut


def get_filename(test=False):
    return f'day11_input{"_test" if test else ""}.txt'


def parse1(line):
    return [char for char in line]


def findAdjacent(seats, x, y):
    adj = []

    for i in range(max(0, x-1), min(len(seats), x+2)):
        for j in range(max(0, y-1), min(len(seats[0]), y+2)):
            adj.append((i, j))

    adj.remove((x, y))
    return adj


def changeState(seats, x, y):
    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # Otherwise, the seat's state does not change.

    if seats[x][y] == ".":
        return '.', False

    if seats[x][y] == "L":
        occupied = 0
        adj = findAdjacent(seats, x, y)
        for i, j in adj:
            if seats[i][j] == '#':
                occupied += 1

        if occupied == 0:
            return "#", True

    if seats[x][y] == "#":
        occupied = 0
        adj = findAdjacent(seats, x, y)
        # print(seats[x][y], x, y, adj)
        for i, j in adj:
            if seats[i][j] == '#':
                occupied += 1

        if occupied >= 4:
            return "L", True

    return seats[x][y], False


def findSeated(seats):
    seated = 0
    for line in seats:
        for seat in line:
            if seat == '#':
                seated += 1
    return seated


def ripple(seats):
    newSeats = [[0 for j in range(len(seats[0]))] for i in range(len(seats))]
    hasChangedState = False
    for i in range(len(seats)):
        for j in range(len(seats[0])):
            result, isChanged = changeState(seats, i, j)
            newSeats[i][j] = result
            if isChanged:
                hasChangedState = True
    # [print(''.join(i)) for i in newSeats]
    # print('')
    return newSeats, hasChangedState


def day11p1():
    seats = ut.get_input(get_filename(test=False), parse1)
    # print(seats)

    change = True

    newSeats = seats.copy()
    i = 0
    while change:
        newSeats, change = ripple(newSeats)

    # [print(''.join(i)) for i in newSeats]

    seated = findSeated(newSeats)
    return seated


def parse2(line):
    return parse1(line)


def findAdjacentWithDirection(seats, x, y):
    adj = []
    d1 = ['up', None, 'down']
    d2 = ['left', None, 'right']

    for i in range(max(0, x-1), min(len(seats), x+2)):
        for j in range(max(0, y-1), min(len(seats[0]), y+2)):
            if (i, j) == (x, y):
                continue
            adj.append(((i, j), (d1[i-(x-1)], d2[j-(y-1)])))

    return adj


def findInSightRec(seats, x, y, direction):
    new_x = x
    new_y = y
    if seats[x][y] == '.':
        if direction[0] == 'up':
            new_x -= 1
        if direction[0] == 'down':
            new_x += 1
        if direction[1] == 'left':
            new_y -= 1
        if direction[1] == 'right':
            new_y += 1

        if new_x < 0 or new_x > len(seats)-1 or new_y < 0 or new_y > len(seats[0])-1:
            return seats[x][y]

        return findInSightRec(seats, new_x, new_y, direction)

    return seats[x][y]


def findInSight(seats, x, y):
    adj = findAdjacentWithDirection(seats, x, y)
    global r_v
    # print()
    # print(directions)

    import collections
    valTo = collections.defaultdict(int)

    for idx, (adj, direction) in enumerate(adj):
        # print(idx, '.', adj)
        x_, y_ = adj
        valTo[findInSightRec(seats, x_, y_, direction)] += 1

    return valTo


def ripple2(seats):
    newSeats = [[seats[i][j]
                 for j in range(len(seats[0]))] for i in range(len(seats))]
    hasChangedState = False
    for i in range(len(seats)):
        for j in range(len(seats[0])):
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            # Otherwise, the seat's state does not change.

            if seats[i][j] == '.':
                # newSeats[i][j] = '.'
                continue

            sight_dict = findInSight(seats, i, j)
            # print(seats[i][j], i, j, sight_dict)
            # [print(''.join(i)) for i in seats]

            if seats[i][j] == 'L' and sight_dict['#'] == 0:
                # print('L -> #')
                newSeats[i][j] = '#'
                hasChangedState = True

            if seats[i][j] == '#' and sight_dict['#'] >= 5:
                # print('# -> L')
                newSeats[i][j] = 'L'
                hasChangedState = True

    # [print(''.join(i)) for i in seats]
    # print('')
    # [print(''.join(i)) for i in newSeats]
    # print('')
    return newSeats, hasChangedState


def day11p2():
    seats = ut.get_input(get_filename(test=False), parse1)

    change = True
    newSeats = seats.copy()
    i = 1
    while change:
        # print('hjb', i)
        i += 1
        newSeats, change = ripple2(newSeats)
        # print(newSeats, change)
    # [print(''.join(i)) for i in newSeats]

    seated = findSeated(newSeats)

    return seated


def main():
    print("Day 11 - Part 1")
    print(day11p1())

    print("Day 11 - Part 2")
    print(day11p2())


main()

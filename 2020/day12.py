def get_filename(test=False):
    return f'day12_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def parse1(line):
    return [line[0], int(line[1:])]


def manhattan_distance(p, q):
    result = 0
    for i in range(len(p)):
        result += abs(p[i] - q[i])
    return result


def day12p1():
    dirs = get_input(parse1, test=False)

    conversions = {'S': 0, 'W': 1, 'N': 2, 'E': 3, 'R': 4, 'L': 5, 'F': 6}
    circle: list = list(conversions.values())[0:4]

    changed = []
    for d in dirs:
        changed.append((conversions.get(d[0]), d[1]))

    # print(changed)

    # (FacingDirection='E', S, W, N, E)
    curr_position = [0, 0, 0, 0]
    curr_direction = 3

    for dir in changed:
        # print('-'*30)
        # print(dir)
        # print(curr_position)
        d = dir[0]
        qty = dir[1]

        if 0 <= d <= 3:
            curr_position[d] += qty

        if d == 4:
            # rotate
            cycles = qty // 90
            c = curr_direction
            for i in range(cycles):
                curr_direction = circle[(c+1) % 4]
                c += 1

        if d == 5:
            # rotate
            cycles = qty // 90
            c = curr_direction
            for i in range(cycles):
                curr_direction = circle[(c-1) % 4]
                c -= 1

        if d == 6:
            # if d == 5:
            curr_position[curr_direction] += qty

    # print(curr_position)
    # print(curr_position[1:], (0, 0, 0, 0))

    curr_position = (abs(
        curr_position[0] - curr_position[2]
    ), abs(
        curr_position[1] - curr_position[3]))

    # print(curr_position)

    return manhattan_distance(curr_position, (0, 0, 0, 0))


def parse2(line):
    return parse1(line)


def day12p2():
    dirs = get_input(parse2, test=False)

    conversions = {'S': 0, 'W': 1, 'N': 2, 'E': 3, 'R': 4, 'L': 5, 'F': 6}

    changed = []
    for d in dirs:
        changed.append((conversions.get(d[0]), d[1]))

    # print(changed)

    # (S, W, N, E)
    curr_position = [0, 0, 0, 0]

    # (S, W, N, E)
    waypoint = [0, 0, 1, 10]  # 10 units east and 1 unit north

    for dir in changed:
        # print('-'*30)
        # print(dir)
        # print('(S, W, N, E)')
        # print('position', curr_position)
        # print('wp', waypoint)
        d = dir[0]
        qty = dir[1]

        if 0 <= d <= 3:
            waypoint[d] += qty

        if d == 4:
            # rotate clockwise
            cycles = qty // 90
            waypoint = waypoint[-(cycles % len(
                waypoint)):] + waypoint[:-(cycles % len(waypoint))]

        if d == 5:
            # rotate counter-clockwise
            cycles = qty // 90

            waypoint = waypoint[cycles % len(
                waypoint):] + waypoint[:cycles % len(waypoint)]

        if d == 6:
            curr_position = [a + b*qty for a,
                             b in zip(curr_position, waypoint)]

    curr_position = (abs(
        curr_position[0] - curr_position[2]
    ), abs(
        curr_position[1] - curr_position[3]))

    # print(curr_position)

    return manhattan_distance(curr_position, (0, 0, 0, 0))


def main():
    print("Day 12 - Part 1")
    print(day12p1())

    print("Day 12 - Part 2")
    print(day12p2())


main()

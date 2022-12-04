import functools
import operator


def get_filename(test=False):
    return f'day09_input{"_test" if test else ""}.txt'


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


def is_lowest(x, y, matrix):
    target = int(matrix[y][x])

    if target == 9:
        return False

    minx = x
    miny = y

    wy = len(matrix)
    wx = len(matrix[0])

    for cy in range(max(0, y - 1), min(wy, y + 2)):
        if int(matrix[cy][x]) < target:
            miny = cy

    for cx in range(max(0, x - 1), min(wx, x + 2)):
        if int(matrix[y][cx]) < target:
            minx = cx

    return minx == x and miny == y


################################################################################


def day09p1():
    data = get_input(parse1, test=False)

    total_lowest = 0
    for ir, row in enumerate(data):
        for ic, col in enumerate(row):
            total_lowest += is_lowest(ic, ir, data) * (1 + int(col))

    return total_lowest


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def adjacents(x, y, matrix):
    adj = set()

    wy = len(matrix)
    wx = len(matrix[0])

    for cy in range(max(0, y - 1), min(wy, y + 2)):
        adj.add((x, cy))

    for cx in range(max(0, x - 1), min(wx, x + 2)):
        adj.add((cx, y))

    adj.discard((x, y))

    return adj


def find_basin_size(x, y, matrix, visited: set):
    if (x, y) in visited:
        return 0

    visited.add((x, y))

    basinValuesSum = int(matrix[y][x])

    for ax, ay in adjacents(x, y, matrix):
        if matrix[ay][ax] == "9":
            continue

        if (ax, ay) in visited:
            continue

        basinValuesSum += find_basin_size(ax, ay, matrix, visited)

    return basinValuesSum


################################################################################


def day09p2():
    data = get_input(parse2, test=False)

    lowest_points = []
    for ir, row in enumerate(data):
        for ic, _ in enumerate(row):
            if is_lowest(ic, ir, data):
                lowest_points.append((ic, ir))

    sizes = []

    for x, y in lowest_points:
        visited = set()
        find_basin_size(x, y, data, visited)
        sizes.append(len(visited))

    max3 = sorted(sizes)[-3:]

    return functools.reduce(operator.mul, max3, 1)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 09 - Part 1", "-" * n)
    print("Result =>", day09p1())
    print()
    print("-" * (n), "Day 09 - Part 2", "-" * n)
    print("Result =>", day09p2())
    print()


main()

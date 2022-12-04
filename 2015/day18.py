import copy


def get_filename(test=False):
    return f'day18_input{"_test" if test else ""}.txt'


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
    return [i for i in line]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_neighbors(m, x, y):
    m_x = max(0, x - 1)
    m_y = max(0, y - 1)
    mx_x = min(len(m) - 1, x + 1)
    mx_y = min(len(m[0]) - 1, y + 1)

    r = []
    for i in range(m_x, mx_x + 1):
        for j in range(m_y, mx_y + 1):
            if (i, j) != (x, y):
                r.append(m[i][j])
    return r


################################################################################


def day18p1():
    data = get_input(parse1, test=False)

    iters = 100

    for _ in range(iters):
        tmp_m = copy.deepcopy(data)
        for i in range(len(data)):
            for j in range(len(data[0])):
                nb: list = get_neighbors(data, i, j)
                # print((i, j), nb)
                if data[i][j] == "#":
                    if nb.count("#") not in [2, 3]:
                        tmp_m[i][j] = "."  # turn off
                else:
                    if nb.count("#") == 3:
                        tmp_m[i][j] = "#"  # turn on
        data = tmp_m

    on = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#":
                on += 1

    return ("ON", on)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day18p2():
    data = get_input(parse2, test=False)
    iters = 100

    data[0][0] = "#"
    data[0][-1] = "#"
    data[-1][0] = "#"
    data[-1][-1] = "#"

    for _ in range(iters):
        tmp_m = copy.deepcopy(data)
        for i in range(len(data)):
            for j in range(len(data[0])):
                nb: list = get_neighbors(data, i, j)
                # print((i, j), nb)
                if data[i][j] == "#":
                    if nb.count("#") not in [2, 3]:
                        tmp_m[i][j] = "."  # turn off
                else:
                    if nb.count("#") == 3:
                        tmp_m[i][j] = "#"  # turn on
        tmp_m[0][0] = "#"
        tmp_m[0][-1] = "#"
        tmp_m[-1][0] = "#"
        tmp_m[-1][-1] = "#"
        data = tmp_m

    on = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#":
                on += 1

    return ("ON", on)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 18 - Part 1", "-" * n)
    print("Result =>", day18p1())
    print()
    print("-" * (n), "Day 18 - Part 2", "-" * n)
    print("Result =>", day18p2())
    print()


main()

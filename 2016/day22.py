import re


def get_filename(test=False):
    return f'day22_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for idx, line in enumerate(file):
            data.append(parse(idx, line.strip()))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(idx: int, line: str):
    if idx < 2:
        return None
    l = line.split()
    l[1] = int(l[1].replace("T", ""))
    l[2] = int(l[2].replace("T", ""))
    l[3] = int(l[3].replace("T", ""))
    return l


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_viable_pairs(nodes: list):
    used = [[d[0], d[2]] for d in nodes]
    available = [[d[0], d[3]] for d in nodes]

    used.sort(key=lambda x: x[1])
    available.sort(key=lambda x: x[1], reverse=True)

    used = list(filter(lambda x: x[1] > 0, used))

    viable_pairs = set()

    cu = 0

    while cu < len(used):
        for ca in available:
            if used[cu][0] == ca[0]:
                continue
            if used[cu][1] <= ca[1]:
                viable_pairs.add((used[cu][0], ca[0]))
            else:
                break

        cu += 1
    return viable_pairs


################################################################################


def day22p1():
    data = get_input(parse1, test=False)
    data = data[2:]

    viable_pairs = get_viable_pairs(data)

    return len(viable_pairs)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(idx, line):
    return parse1(idx, line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day22p2():
    data = get_input(parse2, test=False)
    data = data[2:]

    mx = 31
    my = 31
    mtx = [["." for _ in range(mx)] for _ in range(my)]

    for node in data:
        x, y = map(int, re.findall(r"x(\d+)-y(\d+)", node[0])[0])
        if 92 < node[2]:
            mtx[y][x] = "#"
        if node[2] == 0:
            mtx[y][x] = "_"

    mtx[0][0] = "T"
    mtx[0][30] = "G"

    i = 0
    # This problem was done visually
    # Move _ to right of F
    # Then Move G to Right of T
    # Add 1
    for r in mtx:
        print(i, "\t", "".join(r))
        i += 1

    # 9 + 26 + 25 + 1
    # 5 * 29
    # 1

    move_empty_to_target = 9 + 26 + 25 + 1
    move_target_to_x0_y0 = 5 * 29 + 1

    return move_empty_to_target + move_target_to_x0_y0


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 22 - Part 1", "-" * n)
    print("Result =>", day22p1())
    print()
    print("-" * (n), "Day 22 - Part 2", "-" * n)
    print("Result =>", day22p2())
    print()


main()

from typing import List


def get_filename(test=False):
    return f'day25_input{"_test" if test else ""}.txt'


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


MAP_ = {
    ">": 0,
    "v": 1,
    ".": None,
}


def parse1(line: str):
    return [MAP_[c] for c in line]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def pretty_print(east, south, xw, yw):
    sea_map = [["." for _ in range(xw)] for _ in range(yw)]

    for x, y in east:
        sea_map[y][x] = ">"
    for x, y in south:
        sea_map[y][x] = "v"

    for r in sea_map:
        print("".join(r))


def run_sim(sea_map: List[List[int]]):
    east_locs = set()
    south_locs = set()

    for y, row in enumerate(sea_map):
        for x, cc in enumerate(row):
            if cc == 0:
                east_locs.add((x, y))
            elif cc == 1:
                south_locs.add((x, y))

    xw = len(sea_map[0])
    yw = len(sea_map)

    iterations = 0

    # print(f'Iteration #{iterations}')
    # pretty_print(east_locs, south_locs, xw, yw)
    # print('-'*20)

    while True:
        moved = False
        new_east = set()
        new_south = set()
        for east in east_locs:
            nxt_x, nxt_y = (east[0] + 1) % xw, east[1]
            if (nxt_x, nxt_y) not in east_locs and (nxt_x, nxt_y) not in south_locs:
                moved = True
                new_east.add((nxt_x, nxt_y))
            else:
                new_east.add(east)

        east_locs = new_east

        for south in south_locs:
            nxt_x, nxt_y = south[0], (south[1] + 1) % yw
            if (nxt_x, nxt_y) not in east_locs and (nxt_x, nxt_y) not in south_locs:
                moved = True
                new_south.add((nxt_x, nxt_y))
            else:
                new_south.add(south)

        south_locs = new_south

        iterations += 1
        if not moved:
            break

    return iterations


################################################################################


def day25p1():
    data = get_input(parse1, test=False)

    return run_sim(data)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day25p2():
    data = get_input(parse2, test=True)
    for d in data:
        pass


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 25 - Part 1", "-" * n)
    print("Result =>", day25p1())
    print()
    print("-" * (n), "Day 25 - Part 2", "-" * n)
    print("Result =>", day25p2())
    print()


main()

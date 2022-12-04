def get_filename(test=False):
    return f'day11_input{"_test" if test else ""}.txt'


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


def adjacents(x, y, matrix):
    adj = set()

    wy = len(matrix)
    wx = len(matrix[0])

    for cy in range(max(0, y - 1), min(wy, y + 2)):
        for cx in range(max(0, x - 1), min(wx, x + 2)):
            adj.add((cx, cy))

    adj.discard((x, y))

    return adj


def pp(grid):
    print("-----")
    for d in grid:
        print(d)
    print("-----")


def calc_flashed(grid, only_flashes) -> bool:
    wx = len(grid[0])
    wy = len(grid)

    flash_remains = False
    flashes = 0

    lighted = set()

    for x in range(wx):
        for y in range(wy):
            if not only_flashes:
                grid[y][x] += 1

            if grid[y][x] > 9:
                flashes += 1
                grid[y][x] = 0

                lighted.add((x, y))

                adjs = adjacents(x, y, grid)
                for ax, ay in adjs:
                    if (ax, ay) in lighted:
                        continue

                    if grid[ay][ax] == 0 and only_flashes:
                        continue

                    grid[ay][ax] += 1
                    if grid[ay][ax] > 9:
                        flash_remains = True

    return flashes, flash_remains


def reshape(grid):
    newgrid = [[] for _ in range(len(grid))]
    for ri, row in enumerate(grid):
        for oct in row:
            newgrid[ri].append(int(oct))
    return newgrid


################################################################################


def day11p1():
    data = get_input(parse1, test=False)

    grid = reshape(data)

    step = 1
    flash_remain = False
    total_flashes = 0

    while step <= 100:
        flashes, flash_remain = calc_flashed(grid, only_flashes=flash_remain)
        total_flashes += flashes
        # print('Run', step, 'Remain?', flash_remain)
        # pp(grid)
        if not flash_remain:
            step += 1

    return total_flashes


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day11p2():
    data = get_input(parse2, test=False)

    grid = reshape(data)

    step = 1
    flash_remain = False

    while True:
        _, flash_remain = calc_flashed(grid, only_flashes=flash_remain)
        # print('Run', step, 'Remain?', flash_remain)

        all_zero = True
        for row in grid:
            for oct in row:
                if oct != 0:
                    all_zero = False
                    break

        if all_zero:
            break

        if not flash_remain:
            step += 1

    return step


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 11 - Part 1", "-" * n)
    print("Result =>", day11p1())
    print()
    print("-" * (n), "Day 11 - Part 2", "-" * n)
    print("Result =>", day11p2())
    print()


main()

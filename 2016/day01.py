

def get_filename(test=False):
    return f'day01_input{"_test" if test else ""}.txt'


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


def parse1(line: str):
    return line.split(", ")


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day01p1():
    data = get_input(parse1, test=False)[0]

    # N E S W
    curr_dir = 0
    position = [0, 0]
    for step in data:
        count = int(step[1:])
        turn = step[0]
        if turn == "L":
            curr_dir = (curr_dir - 1) % 4
        else:
            curr_dir = (curr_dir + 1) % 4

        if curr_dir == 0:
            position[1] += count
        elif curr_dir == 1:
            position[0] += count
        elif curr_dir == 2:
            position[1] -= count
        elif curr_dir == 3:
            position[0] -= count
        else:
            raise Exception("INVALID DIR")

    return "Pos", position, "Distance", abs(position[0]) + abs(position[1])


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def add(i1, i2):
    return list(map(lambda x: x[0] + x[1], zip(i1, i2)))


print("a", add([1, 2, 3, 4], [1, 1, 1, 1]))

################################################################################


def day01p2():
    data = get_input(parse2, test=False)[0]

    # N E S W
    curr_dir = 0
    position = [0, 0]
    visited = set()
    for step in data:
        count = int(step[1:])

        if step[0] == "L":
            curr_dir = (curr_dir - 1) % 4
        else:
            curr_dir = (curr_dir + 1) % 4

        d = None
        if curr_dir == 0:
            d = [0, 1]
        elif curr_dir == 1:
            d = [1, 0]
        elif curr_dir == 2:
            d = [0, -1]
        elif curr_dir == 3:
            d = [-1, 0]
        else:
            raise Exception("INVALID DIR")

        for _ in range(count):
            position = add(position, d)
            if tuple(position) in visited:
                return "Pos", position, "Distance", abs(position[0]) + abs(position[1])
            visited.add(tuple(position))


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 01 - Part 1", "-" * n)
    print("Result =>", day01p1())
    print()
    print("-" * (n), "Day 01 - Part 2", "-" * n)
    print("Result =>", day01p2())
    print()


main()

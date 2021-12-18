import re


def get_filename(test=False):
    return f'day17_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    return list(map(int, re.findall(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', line)[0]))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def find_path(initialV, xmin, xmax, ymin, ymax):
    cx, cy = 0, 0
    cvx, cvy = initialV[0], initialV[1]

    steps = []
    while cy >= ymin:
        steps.append((cx, cy))

        if xmin <= cx <= xmax and ymin <= cy <= ymax:
            return steps, True

        cx += cvx
        cy += cvy

        if cvx > 0:
            cvx -= 1
        elif cvx < 0:
            cvx += 1

        cvy -= 1
    return [], False


################################################################################


def day17p1():
    data = get_input(parse1, test=False)
    for d in data:
        xmin, xmax, ymin, ymax = d

        maxy = -10
        mS = None
        for x in range(xmax+1):
            for y in range(-ymin):
                steps, isL = find_path((x, y), xmin, xmax, ymin, ymax)
                if isL:
                    maxS = max(steps, key=lambda x: x[1])
                    if maxS[1] > maxy:
                        maxy = maxS[1]
                        mS = maxS
        return mS

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day17p2():
    data = get_input(parse2, test=False)[0]

    xmin, xmax, ymin, ymax = data

    total_steps = 0
    for x in range(xmax+1):
        for y in range(ymin, -ymin+1):
            _, isL = find_path((x, y),  xmin, xmax, ymin, ymax)
            if isL:
                total_steps += 1

    return total_steps


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 17 - Part 1", '-'*n)
    print('Result =>', day17p1())
    print()
    print('-'*(n), "Day 17 - Part 2", '-'*n)
    print('Result =>', day17p2())
    print()


main()

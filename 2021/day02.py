def get_filename(test=False):
    return f'day02_input{"_test" if test else ""}.txt'


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
    return line.split(' ')

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day02p1():
    data = get_input(parse1, test=False)

    x = 0
    depth = 0
    for inst in data:
        if inst[0] == 'forward':
            x += int(inst[1])
        elif inst[0] == 'up':
            depth -= int(inst[1])
        elif inst[0] == 'down':
            depth += int(inst[1])

    return x * depth

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day02p2():
    data = get_input(parse2, test=False)

    x = 0
    depth = 0
    aim = 0
    for inst in data:
        if inst[0] == 'forward':
            x += int(inst[1])
            depth += aim*int(inst[1])
        elif inst[0] == 'up':
            aim -= int(inst[1])
        elif inst[0] == 'down':
            aim += int(inst[1])

    return x * depth


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Dadepth 02 - Part 1", '-'*n)
    print('Result =>', day02p1())
    print()
    print('-'*(n), "Dadepth 02 - Part 2", '-'*n)
    print('Result =>', day02p2())
    print()


main()

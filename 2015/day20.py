def get_filename(test=False):
    return f'day20_input{"_test" if test else ""}.txt'


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


def parse1(line):
    return int(line)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day20p1():
    data = get_input(parse1, test=False)
    data = data[0]

    top = data // 10
    houses = [0 for _ in range(top)]
    for elf in range(1, top):
        gifts = elf * 10
        for house in range(elf, top, elf):
            houses[house] += gifts

    print('Total houses', len(houses))

    a = []
    for house in range(len(houses)):
        if houses[house] >= data:
            a.append(house)
            break

    print('len', len(a))

    return min(a)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day20p2():
    data = get_input(parse2, test=False)
    data = data[0]

    top = data // 10
    houses = [0 for _ in range(top)]
    for elf in range(1, top):
        gifts = elf * 11
        visited = 0
        for house in range(elf, top, elf):
            if visited == 50:
                break
            houses[house] += gifts
            visited += 1

    print('Total houses', len(houses))

    a = []
    for house in range(len(houses)):
        if houses[house] >= data:
            a.append(house)
            break

    print('len', len(a))

    return min(a)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 20 - Part 1", '-'*n)
    print('Result =>', day20p1())
    print()
    print('-'*(n), "Day 20 - Part 2", '-'*n)
    print('Result =>', day20p2())
    print()


main()

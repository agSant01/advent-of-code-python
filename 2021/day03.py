import collections


def get_filename(test=False):
    return f'day03_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################

def day03p1():
    data = get_input(parse1, test=False)
    map = collections.defaultdict(list)

    for binary in data:
        for idx, bit in enumerate(binary):
            if idx not in map:
                map[idx] = [0, 0]
            map[idx][int(bit)] += 1

    gamma = 0
    ep = 0
    bits = len(data[0])-1
    for idx, value in map.items():
        if value[0] > value[1]:
            ep += 2**(bits-idx)
        else:
            gamma += 2**(bits-idx)

    return gamma*ep


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day03p2():
    data = get_input(parse2, test=False)
    bit_len = len(data[0])

    oxygen_gen = [d for d in data]
    co2_scrub = [d for d in data]

    pos = 0
    while len(oxygen_gen) > 1:
        s0 = 0
        s1 = 0

        for binary in oxygen_gen:
            if binary[pos] == '0':
                s0 += 1
            else:
                s1 += 1

        win_ox = '1' if s1 >= s0 else '0'

        oxygen_gen = list(filter(lambda x: x[pos] == win_ox, oxygen_gen))
        pos += 1

    pos = 0
    while len(co2_scrub) > 1 and pos < bit_len:
        s0 = 0
        s1 = 0
        for binary in co2_scrub:
            if binary[pos] == '0':
                s0 += 1
            else:
                s1 += 1

        win_co = '0' if s0 <= s1 else '1'

        co2_scrub = list(filter(lambda x: x[pos] == win_co, co2_scrub))
        pos += 1

    return int(oxygen_gen[0], base=2)*int(co2_scrub[0], base=2)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 03 - Part 1", '-'*n)
    print('Result =>', day03p1())
    print()
    print('-'*(n), "Day 03 - Part 2", '-'*n)
    print('Result =>', day03p2())
    print()


main()

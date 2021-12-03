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
    bits = len(data[0])
    numbers = len(data)

    gamma = 0
    for pos in range(bits):
        s1 = 0
        for binary in data:
            s1 += int(binary[pos])
        if numbers-s1 < s1:
            gamma += 2**(bits-pos-1)

    # epsilon is negation of gamma
    # python truncates the binary of a number
    # -> ~gamma and (with a binary number of bits length of 1's)
    return gamma * (~gamma & (1 << bits)-1)


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

    def count(numbers: list, pos: int):
        s1 = 0
        for binary in numbers:
            s1 += int(binary[pos])
        return len(numbers)-s1, s1

    pos = 0
    while len(oxygen_gen) > 1:
        s0, s1 = count(oxygen_gen, pos)

        win_ox = '1' if s1 >= s0 else '0'

        oxygen_gen = list(filter(lambda x: x[pos] == win_ox, oxygen_gen))
        pos += 1

    pos = 0
    while len(co2_scrub) > 1 and pos < bit_len:
        s0, s1 = count(co2_scrub, pos)

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

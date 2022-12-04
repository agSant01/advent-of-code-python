import re


def get_filename(test=False):
    return f'day19_input{"_test" if test else ""}.txt'


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
    return line.split(" => ")


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def calibrate(mappings, ADN):
    possible_patterns = set()

    for mapping in mappings:
        for match in re.finditer(mapping[0], ADN):
            possible_patterns.add(ADN[: match.start()] + mapping[1] + ADN[match.end() :])

    return possible_patterns


################################################################################


def day19p1():
    data = get_input(parse1, test=False)
    ADN: str = data[-1][0]
    data = data[:-2]

    possible_patterns = calibrate(data, ADN)

    return len(possible_patterns)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day19p2():
    data = get_input(parse2, test=False)
    ADN: str = data[-1][0]

    symb = "".join(filter(lambda c: c.isupper(), ADN))
    Ar = ADN.count("Ar")
    Rn = ADN.count("Rn")
    Y = 2 * ADN.count("Y")

    return len(symb) - Ar - Rn - Y - 1


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 19 - Part 1", "-" * n)
    print("Result =>", day19p1())
    print()
    print("-" * (n), "Day 19 - Part 2", "-" * n)
    print("Result =>", day19p2())
    print()


main()

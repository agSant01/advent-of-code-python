import re


def get_filename(test=False):
    return f'day16_input{"_test" if test else ""}.txt'


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


PAT = re.compile(
    r"(children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes):"
    r" ([0-9]+)"
)


def parse1(line: str):
    dict_ = {}
    for tag, qty in PAT.findall(line):
        dict_[tag] = int(qty)

    return dict_


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


UNKNOWN_AUNT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


################################################################################
def day16p1():
    data: list = get_input(parse1, test=False)

    posible_aunts = []

    for idx, aunt in enumerate(data):
        aunt: dict = aunt
        is_aunt = True
        for tag in aunt.keys():
            if UNKNOWN_AUNT[tag] != aunt[tag]:
                is_aunt = False
                break
        if is_aunt:
            print(aunt)
            posible_aunts.append(idx + 1)

    return posible_aunts


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day16p2():
    data = get_input(parse2, test=False)

    posible_aunts = []

    for idx, aunt in enumerate(data):
        aunt: dict = aunt
        is_aunt = True
        for tag in aunt.keys():
            if tag in ["cats", "trees"]:
                if aunt[tag] <= UNKNOWN_AUNT[tag]:
                    is_aunt = False
            elif tag in ["pomeranians", "goldfish"]:
                if aunt[tag] >= UNKNOWN_AUNT[tag]:
                    is_aunt = False
            elif UNKNOWN_AUNT[tag] != aunt[tag]:
                is_aunt = False
                break
        if is_aunt:
            print(aunt)
            posible_aunts.append(idx + 1)

    return posible_aunts


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 16 - Part 1", "-" * n)
    print("Result =>", day16p1())
    print()
    print("-" * (n), "Day 16 - Part 2", "-" * n)
    print("Result =>", day16p2())
    print()


main()

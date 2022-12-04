def get_filename(test=False):
    return f'day02_input{"_test" if test else ""}.txt'


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
    return line.strip()


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


"""
1 2 3
4 5 6  => [1 2 3 4 5 6 7 8 9]
7 8 9
"""


def move_keypad(sequence, start):
    def UP(x):
        return x - 3 if x - 3 >= 0 else x

    def DOWN(x):
        return x + 3 if x + 3 < 9 else x

    def LEFT(x):
        return x if (x % 3 - 1) < 0 else x - 1

    def RIGHT(x):
        return x if (x % 3 + 1) > 2 else x + 1

    for inst in sequence:
        if inst == "L":
            start = LEFT(start)
        if inst == "R":
            start = RIGHT(start)
        if inst == "U":
            start = UP(start)
        if inst == "D":
            start = DOWN(start)
    return start


################################################################################


def day02p1():
    sequences = get_input(parse1, test=False)

    pwd = ""
    button = 4
    for sequence in sequences:
        button = move_keypad(sequence, button)
        pwd += str(button + 1)

    return pwd


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


""" 
0 0 1 0 0
0 2 3 4 0
5 6 7 8 9 => [0, 0, 1, 0, ..., D, ..., 0]
0 A B C 0
0 0 D 0 0
"""

KEYPAD = [
    "0",
    "0",
    "1",
    "0",
    "0",
    "0",
    "2",
    "3",
    "4",
    "0",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "A",
    "B",
    "C",
    "0",
    "0",
    "0",
    "D",
    "0",
    "0",
]


def move_keypad_diamond(sequence, start):
    WIDTH = 5

    def UP(x):
        return x - WIDTH if x - WIDTH >= 0 and KEYPAD[x - WIDTH] != "0" else x

    def DOWN(x):
        return x + WIDTH if x + WIDTH < 25 and KEYPAD[x + WIDTH] != "0" else x

    def LEFT(x):
        return x - 1 if (x % WIDTH - 1) >= 0 and KEYPAD[x - 1] != "0" else x

    def RIGHT(x):
        return x + 1 if (x % WIDTH + 1) < WIDTH and KEYPAD[x + 1] != "0" else x

    for inst in sequence:
        if inst == "L":
            start = LEFT(start)
        if inst == "R":
            start = RIGHT(start)
        if inst == "U":
            start = UP(start)
        if inst == "D":
            start = DOWN(start)

    return start


################################################################################


def day02p2():
    sequence = get_input(parse2, test=False)

    position = KEYPAD.index("5")
    pwd = ""
    for seq in sequence:
        position = move_keypad_diamond(seq, position)
        pwd += KEYPAD[position]

    return pwd


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 02 - Part 1", "-" * n)
    print("Result =>", day02p1())
    print()
    print("-" * (n), "Day 02 - Part 2", "-" * n)
    print("Result =>", day02p2())
    print()


main()

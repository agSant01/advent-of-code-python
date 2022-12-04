import hashlib
import math


def get_filename(test=False):
    return f'day17_input{"_test" if test else ""}.txt'


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


################################################################################
SHORTEST_SEQ = ""
SHORTEST = math.inf
OPEN = "bcdef"


def shortest_path_vault(hash_, sequence, pos_x, pos_y):
    global SHORTEST_SEQ, SHORTEST

    if pos_x < 0 or pos_x > 3:
        return

    if pos_y < 0 or pos_y > 3:
        return

    if len(sequence) > SHORTEST:
        return

    if pos_x == 3 and pos_y == 3:
        if len(sequence) < SHORTEST:
            SHORTEST_SEQ = sequence
            SHORTEST = len(sequence)
        return

    directions = hashlib.md5(str(hash_ + sequence).encode()).hexdigest()

    # up
    if directions[0] in OPEN:
        shortest_path_vault(hash_, sequence + "U", pos_x, pos_y - 1)

    # down
    if directions[1] in OPEN:
        shortest_path_vault(hash_, sequence + "D", pos_x, pos_y + 1)

    # left
    if directions[2] in OPEN:
        shortest_path_vault(hash_, sequence + "L", pos_x - 1, pos_y)

    # right
    if directions[3] in OPEN:
        shortest_path_vault(hash_, sequence + "R", pos_x + 1, pos_y)


def day17p1():
    global SHORTEST_SEQ

    shortest_path_vault("ihgpwlah", "", 0, 0)

    return SHORTEST_SEQ


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


LONGEST_SEQ = ""
LONGEST = -math.inf


def longest_path_vault(hash_, sequence, pos_x, pos_y):
    global LONGEST_SEQ, LONGEST

    if pos_x < 0 or pos_x > 3:
        return

    if pos_y < 0 or pos_y > 3:
        return

    if pos_x == 3 and pos_y == 3:
        if len(sequence) > LONGEST:
            LONGEST_SEQ = sequence
            LONGEST = len(sequence)
        return

    directions = hashlib.md5(str(hash_ + sequence).encode()).hexdigest()

    # up
    if directions[0] in OPEN:
        longest_path_vault(hash_, sequence + "U", pos_x, pos_y - 1)

    # down
    if directions[1] in OPEN:
        longest_path_vault(hash_, sequence + "D", pos_x, pos_y + 1)

    # left
    if directions[2] in OPEN:
        longest_path_vault(hash_, sequence + "L", pos_x - 1, pos_y)

    # right
    if directions[3] in OPEN:
        longest_path_vault(hash_, sequence + "R", pos_x + 1, pos_y)


################################################################################
def day17p2():
    passcode = "njfxhljp"
    longest_path_vault(passcode, "", 0, 0)
    return LONGEST


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 17 - Part 1", "-" * n)
    print("Result =>", day17p1())
    print()
    print("-" * (n), "Day 17 - Part 2", "-" * n)
    print("Result =>", day17p2())
    print()


main()

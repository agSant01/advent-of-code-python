import functools
import re


def get_filename(test=False):
    return f'day18_input{"_test" if test else ""}.txt'


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


# Its left and center tiles are traps, but its right tile is not.
RULE1 = re.compile('\^\^\.')
# Its center and right tiles are traps, but its left tile is not.
RULE2 = re.compile('\.\^\^')
# Only its left tile is a trap.
RULE3 = re.compile('\^\.\.')
# Only its right tile is a trap.
RULE4 = re.compile('\.\.\^')


# @functools.lru_cache(maxsize=None)
def is_a_trap(lcr: str):
    # return bool(RULE1.match(lcr) or
    #             RULE2.match(lcr) or
    #             RULE3.match(lcr) or
    #             RULE4.match(lcr))
    return lcr[0] != lcr[2]


################################################################################


def day18p1():
    MAX_ROWS = 40

    # prev_row = '..^^.'
    prev_row = get_input(parse1, test=False)[0]

    safe_tiles = 0
    row = 0
    row_width = len(prev_row)

    while row < MAX_ROWS:
        safe_tiles += prev_row.count('.')
        crow = ''

        for idx in range(row_width):
            topLCR = ''
            if idx == 0:
                topLCR = '.'

            topLCR += prev_row[max(idx-1, 0):min(idx+2, row_width)]

            if idx == row_width-1:
                topLCR += '.'

            crow += '^' if is_a_trap(topLCR) else '.'

        prev_row = crow

        row += 1

    return 'SafeTiles: {}'.format(safe_tiles)

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day18p2_mem_eff():
    MAX_ROWS = 400_000

    initial_row = get_input(parse2, test=False)[0]
    width = len(initial_row)

    mask = 2 ** width - 1

    row = functools.reduce(
        lambda acc, tile: acc << 1 | (tile == '^'),
        initial_row,
        0
    )

    safe_tiles = width - bin(row).count('1')

    for _ in range(MAX_ROWS-1):
        # (Shifted LEFT) XOR (Shifted RIGHT)
        #   - to find which tiles have distinct LEFT and RIGHT top tiles, where the resulting bit is '1' then it is a trap
        row = ((row << 1) ^ (row >> 1)) & mask
        safe_tiles += width - bin(row).count('1')

    return 'SafeTiles: {}'.format(safe_tiles)


def day18p2():
    MAX_ROWS = 400_000

    prev_row = get_input(parse2, test=False)[0]

    safe_tiles = 0
    row = 0
    row_width = len(prev_row)

    while row < MAX_ROWS:
        safe_tiles += prev_row.count('.')
        crow = []

        for idx in range(row_width):
            topLCR = ''

            if idx == 0:
                topLCR += '.'
            topLCR += ''.join(prev_row[max(idx-1, 0):min(idx+2, row_width)])

            if idx == row_width-1:
                topLCR += '.'

            crow += '^' if is_a_trap(topLCR) else '.'

        prev_row = crow
        row += 1

    return 'SafeTiles: {}'.format(safe_tiles)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 18 - Part 1", '-'*n)
    print('Result =>', day18p1())
    print()
    print('-'*(n), "Day 18 - Part 2", '-'*n)
    print('Result (Mem and Time Efficient) =>', day18p2_mem_eff())
    print('Result (Naive Solution) =>', day18p2())
    print()


main()

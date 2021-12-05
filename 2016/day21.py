import itertools
import collections
import re
from typing import Collection, List


def get_filename(test=False):
    return f'day21_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################

# The scrambling function is a series of operations (the exact list is provided in your puzzle input). Starting with the password to be scrambled, apply each operation in succession to the string. The individual operations behave as follows:


# swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
# swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
# rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
# rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
# reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
# move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.


def find_idx(item, arr):
    idx_list = []
    for idx, value in enumerate(arr):
        if value == item:
            idx_list.append(idx)
    return idx_list


def scrambler(initial_text: str, instructions: List[str]):
    char_arr = [c for c in initial_text]
    total_chars = len(char_arr)

    for inst in instructions:
        if inst.startswith('swap position'):
            x, y = map(int, re.findall(
                r'swap position (\d+) with position (\d+)', inst)[0])
            temp = char_arr[x]
            char_arr[x] = char_arr[y]
            char_arr[y] = temp
        elif inst.startswith('swap letter'):
            x, y = re.findall(r'letter ([a-z]) with letter ([a-z])', inst)[0]
            x_idx = find_idx(x, char_arr)
            y_idx = find_idx(y, char_arr)
            for i in x_idx:
                char_arr[i] = y
            for i in y_idx:
                char_arr[i] = x
        elif inst.startswith('rotate based'):
            letter = re.findall(r'letter ([a-z]+)', inst)[0]
            # print(letter, char_arr)
            if letter not in char_arr:
                continue
            x = char_arr.index(letter)
            if x >= 4:
                x += 1
            x += 1
            tmp = []
            for i in range(total_chars):
                tmp.append(char_arr[(i-x) % total_chars])
            char_arr = tmp
        elif inst.startswith('rotate'):
            x = re.findall(r'\d+', inst)[0]
            x = int(x)
            if 'right' in inst:
                tmp = []
                for i in range(total_chars):
                    tmp.append(char_arr[(i-x) % total_chars])
                char_arr = tmp
            elif 'left' in inst:
                tmp = []
                for i in range(total_chars):
                    tmp.append(char_arr[(i+x) % total_chars])
                char_arr = tmp
        elif inst.startswith('reverse positions'):
            x, y = map(int, re.findall(
                r'reverse positions (\d+) through (\d+)', inst)[0])
            char_arr = char_arr[:x] + \
                list(reversed(char_arr[x:y+1])) + char_arr[y+1:]
        elif inst.startswith('move position'):
            x, y = map(int, re.findall(
                r'move position (\d+) to position (\d+)', inst)[0])
            tmp = char_arr.pop(x)
            char_arr.insert(y, tmp)

    return ''.join(char_arr)

################################################################################


def day21p1():
    test = False
    data = get_input(parse1, test)
    text = 'abcde'
    if not test:
        text = 'abcdefgh'

    return scrambler(text, data)

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day21p2():
    data = get_input(parse2, test=False)

    pwd = 'fbgdceah'

    for p in itertools.permutations(pwd):
        if scrambler(''.join(p), data) == pwd:
            return ''.join(p)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 21 - Part 1", '-'*n)
    print('Result =>', day21p1())
    print()
    print('-'*(n), "Day 21 - Part 2", '-'*n)
    print('Result =>', day21p2())
    print()


main()

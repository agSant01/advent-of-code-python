import collections
import sys
from typing import List


def get_filename(test=False):
    return f'day04_input{"_test" if test else ""}.txt'


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
def day04p1():
    data: List[str] = get_input(parse1, test=False)
    s = set()
    valid = 0
    for d in data:
        is_valid = True
        for word in d.split():
            if word in s:
                is_valid = False
                break
            s.add(word)
        if is_valid:
            valid += 1
        s.clear()

    return valid

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day04p2():
    data: List[str] = get_input(parse2, test=False)
    valid = 0
    char_dict = collections.defaultdict(list)
    for passphrase in data:
        is_valid = True
        for word in passphrase.split():
            if len(word) == 0:
                print(word)
                exit()
            word_code = sum(idx * ord(c)
                            for idx, c in enumerate(sorted(word)))  # o(n)

            if word_code in char_dict:
                possible_words = char_dict[word_code]
                for pw in possible_words:
                    if all(char in pw for char in word):
                        is_valid = False
                        break
                if not is_valid:
                    break
            else:
                char_dict[word_code].append(list(word))

        if is_valid:
            valid += 1

        char_dict.clear()

    return valid


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print('-'*(n), "Day 04 - Part 1", '-'*n)
        print('Result =>', day04p1())
        print()
    if run_two:
        print('-'*(n), "Day 04 - Part 2", '-'*n)
        print('Result =>', day04p2())
    print()


main()

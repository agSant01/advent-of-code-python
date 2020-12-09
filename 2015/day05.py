from os import nice
import utils as ut


def get_filename(test=False):
    return f'day05_input{"_test" if test else ""}.txt'


def parse(line):
    return line


def contains(s, a):
    for i in a:
        if i in s:
            return True
    return False


def hasThreeVowels(s):
    vowls = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}

    for c in s:
        if c in vowls:
            vowls[c] += 1

    return sum(list(vowls.values())) >= 3


def hasTwoLetterSeq(s):
    i = 0
    while i < len(s)-1:
        if s[i] == s[i+1]:
            return True
        i += 1
    return False


def isValid(s: str):
    if contains(s, ['ab', 'cd', 'pq', 'xy']):
        return False

    if not hasThreeVowels(s):
        return False

    # It contains at least one letter that appears twice in a row,
    # like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    if not hasTwoLetterSeq(s):
        return False

    return True


def day05p1():
    data = ut.get_input(get_filename(test=False), parse)
    nice_ = 0
    for word in data:
        if isValid(word):
            nice_ += 1
    return nice_


def containPairs(w: str):
    for i in range(len(w)-1):
        check = w.find(w[i:(i+2)], i+2)
        if check != -1:
            return True

    return False


def repeated(word):
    for i in range(0, len(word)-2):
        if word[i] == word[i+2] and word[i+1] != word[i+2]:
            return True
    return False


def day05p2():
    words = ut.get_input(get_filename(test=False), parse)
    nice_ = 0
    for word in words:

        if not containPairs(word):
            continue

        if not repeated(word):
            continue

        nice_ += 1

    return nice_


def main():
    print("Day 05 - Part 1")
    print(day05p1())

    print("Day 05 - Part 2")
    print(day05p2())


main()

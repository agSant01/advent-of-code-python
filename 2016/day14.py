import collections
import functools
import hashlib
import re


def get_filename(test=False):
    return f'day14_input{"_test" if test else ""}.txt'


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


def day14p1():
    test = False
    salt = "cuanljph"
    if test:
        salt = "abc"

    index = 0
    key_cnt = 0
    h = None

    map_ = collections.defaultdict(list)

    keys = []

    COMPILED_3 = re.compile(r"(.)\1{2}")
    COMPILED_5 = re.compile(r"(.)\1{4}")

    while key_cnt < 64:
        h = hashlib.md5(str(salt + str(index)).encode()).hexdigest()

        match5 = COMPILED_5.search(h)
        if match5:
            indices = map_[match5.group(0)[0]]
            for idx in indices:
                if idx + 1000 >= index:
                    keys.append(idx)
                    key_cnt += 1

        match3 = COMPILED_3.search(h)
        if match3:
            map_[match3.group(0)[0]].append(index)

        index += 1

    return keys[63]


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


@functools.lru_cache(maxsize=None)
def getlongmd5(s):
    for _ in range(2017):
        s = hashlib.md5(s.encode("utf-8")).hexdigest()
    return s


################################################################################


def day14p2():
    test = False
    salt = "cuanljph"
    if test:
        salt = "abc"

    COMPILED_3 = re.compile(r"([abcdef0-9])\1{2}")
    COMPILED_5 = re.compile(r"([abcdef0-9])\1{4}")

    map_ = collections.defaultdict(list)

    keys = set()

    index = 0
    md5Hash = None

    while len(keys) < 64:
        md5Hash = getlongmd5(salt + str(index)).lower()

        match5 = COMPILED_5.search(md5Hash)
        if match5:
            indices = map_[match5.group(0)[0]]
            for idx in indices:
                if index <= idx + 1000:
                    keys.add(idx)

        match3 = COMPILED_3.search(md5Hash)
        if match3:
            map_[match3.group(0)[0]].append(index)

        index += 1

    return sorted(list(keys))[63]


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 14 - Part 1", "-" * n)
    print("Result =>", day14p1())
    print()
    print("-" * (n), "Day 14 - Part 2", "-" * n)
    print("Result =>", day14p2())
    print()


main()

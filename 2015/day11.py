import itertools
from os import stat


def get_filename(test=False):
    return f'day11_input{"_test" if test else ""}.txt'


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


def encode(s: str):
    return [ord(char) for char in s]


def decode(s: list):
    return [chr(ord) for ord in s]

# returns: (newInc: int, isFlipped: bool)


def inc(s: list):
    print('prev', s)
    carry = 0
    internal = s.copy()
    internal.reverse()

    internal[0] += 1
    if internal[0] > 122:
        carry = internal[0] - 122
        internal[0] = (internal[0] % 122) + 96

    for pos in range(1, len(internal)):
        internal[pos] += carry
        carry = 0
        if internal[pos] > 122:
            carry = internal[pos] - 122
            internal[pos] = 97  # a

    # print('aft', list(reversed(internal)))
    return list(reversed(internal))


def valid_chars(s: list):
    # i, o, l
    for c in s:
        if c in [105, 108, 111]:
            return False
    return True


def contains_rep(s: list):
    count = 0
    for _, g in itertools.groupby(s):
        if len(list(g)) == 2:
            count += 1
    return count >= 2


def contains_inc_char(s: list):
    window = 3
    start = 0
    limit = len(s)
    while start + window < limit:
        v = s[start:start+window]
        if v[0] + 1 == v[1] and v[1] + 1 == v[2]:
            return True
        start += 1

    return False


def increment_string(s: list):
    i = 0
    while True:
        s = inc(s)

        if not valid_chars(s):
            continue

        if contains_rep(s) and contains_inc_char(s):
            break

    return s
################################################################################


def day11p1():
    data = get_input(parse1, test=True)
    res = []
    for d in data:
        print(d)
        print(encode(d))
        enc = encode(d)
        new_ = increment_string(enc)
        print('New_:', new_)
        res.append(('password', ''.join(decode(new_))))
    return res

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day11p2():
    data = get_input(parse2, test=False)
    for d in data:
        print(d)
        print(encode(d))
        enc = encode(d)
        new_ = increment_string(enc)
        print('New_:', new_)
        new_ = increment_string(new_)
        print('New_:', new_)
        return ('password', ''.join(decode(new_)))


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 11 - Part 1", '-'*n)
    print('Result =>', day11p1())
    print()
    print('-'*(n), "Day 11 - Part 2", '-'*n)
    print('Result =>', day11p2())
    print()


main()

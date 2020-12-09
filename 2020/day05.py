import utils as ut
import math


def parse(line):
    return (line[:7], line[7:])


def get_row(code):
    h = 127
    l = 0
    for c in code:
        if c == 'F':
            h = l + (h-l)//2
        else:
            l = l + (h-l)//2
    s = ''
    for c in code:
        if c == 'F':
            s += '1'
        else:
            s += '0'
    print(s)
    print(int(s, 2))
    print(int(code, 2))
    return h


def get_col(code):
    h = 7
    l = 0
    for c in code:
        if c == 'R':
            l = l + (h-l)//2
        else:
            h = l + (h-l)//2
    return h


def day5p1():
    bpas = ut.get_input('day05_input_test.txt', parse)
    ids = []
    for p in bpas:
        # print(get_row(p[0]), get_col(p[1]), get_row(p[0]) * 8+get_col(p[1]))
        ids.append(get_row(p[0]) * 8 + get_col(p[1]))

    return max(ids)


def day5p2():
    bpas = ut.get_input('day05_input_test.txt', parse)
    ids = []
    for p in bpas:
        # print(get_row(p[0]), get_col(p[1]), get_row(p[0]) * 8+get_col(p[1]))
        ids.append(get_row(p[0]) * 8 + get_col(p[1]))

    ids = sorted(ids)
    print(ids)
    for i in range(len(ids)-1):
        if ids[i] + 1 != ids[i+1]:
            return ids[i] + 1


def main():
    print("Day 05 - Part 1")
    print(day5p1())

    print("Day 05 - Part 2")
    print(day5p2())


main()

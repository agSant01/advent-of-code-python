from os import getresgid
import utils as ut


def get_filename(test=False):
    return f'day02_input{"_test" if test else ""}.txt'


def parse(line):
    return list(map(lambda x: int(x), line.split('x')))


def getArea(a):
    #  (l,w,h)
    l = a[0]
    w = a[1]
    h = a[2]
    return 2*l*w + 2*w*h + 2*l*h + min(l*w, w*h, l*h)


def getRibonWrap(a):
    sorted_ = sorted(a)
    return 2*sorted_[0] + 2*sorted_[1]


def getBow(a):
    l = a[0]
    w = a[1]
    h = a[2]
    return l*w*h


def day02p1():
    # (l,w,h)
    data = ut.get_input(get_filename(test=False), parse)
    total_area = 0
    for d in data:
        total_area += getArea(d)
    return total_area


def day02p2():
    data = ut.get_input(get_filename(test=False), parse)
    total_area = 0
    for d in data:
        total_area += getBow(d)
        total_area += getRibonWrap(d)
    return total_area


def main():
    print("Day 02 - Part 1")
    print(day02p1())

    print("Day 02 - Part 2")
    print(day02p2())


main()

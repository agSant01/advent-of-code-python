import itertools
import math
import collections
from os import stat
from typing import Collection, List
import yearutils as yu


def get_filename(test=False):
    return f'day10_input{"_test" if test else ""}.txt'


def parse1(line):
    return int(line)


def find_jolt_diffs(joltages: List[int]):
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    joltages.sort()

    joltage_diffs = collections.defaultdict(int)

    for i in range(0, len(joltages)-1):
        diff = joltages[i+1] - joltages[i]
        if diff <= 3:
            joltage_diffs[diff] += 1

    return joltage_diffs


def day10p1():
    joltages = yu.get_input(get_filename(test=False), parse1)

    joltage_diffs = find_jolt_diffs(joltages)

    return joltage_diffs[1] * joltage_diffs[3]


def parse2(line):
    return parse1(line)


def find_arr_rec(joltages, DP, idx):
    if idx == len(joltages)-1:
        return 1

    if idx in DP:
        return DP[idx]

    curr_s = idx+1
    ans = 0
    while curr_s < len(joltages):
        if joltages[curr_s] - joltages[idx] <= 3:
            ans += find_arr_rec(joltages, DP, curr_s)
        curr_s += 1

    DP[idx] = ans

    return ans


def day10p2():
    joltages = yu.get_input(get_filename(test=False), parse2)

    joltages.append(0)
    joltages.append(max(joltages) + 3)
    joltages.sort()

    return find_arr_rec(joltages,  {}, 0)


def main():
    print("Day 10 - Part 1")
    print(day10p1())

    print("Day 10 - Part 2")
    print(day10p2())


main()

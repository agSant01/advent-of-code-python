import collections
from copy import deepcopy


def get_filename(test=False):
    return f'day17_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def parse1(line):
    return [1 if char == '#' else 0 for char in line]


"""
active (#)
inative (.)

energy boot up by SIX "cycles"

During a cycle, all cubes simultaneously change their state according to the following rules:

If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
"""


def getOnNb3D(on_bulbs, coordinate):
    x, y, z = coordinate
    adj = set()
    deltas = [-1, 0, 1]

    for i in deltas:
        for j in deltas:
            for k in deltas:
                if (x+i, y+j, z+k) in on_bulbs:
                    adj.add((x+i, y+j, z+k))

    adj.discard((x, y, z))

    return adj, len(adj)


def boot_energy_source_3D(initial_slice, cycles=6):
    on_bulbs = set()

    for r, R in enumerate(initial_slice):
        for c, val in enumerate(R):
            if val == 1:
                on_bulbs.add((r, c, 0))

    max_dim_xy = len(initial_slice) + cycles
    max_dim_z = cycles

    for _ in range(cycles):
        new_on = set()
        for i in range(-max_dim_xy, max_dim_xy + 1):
            for j in range(-max_dim_xy, max_dim_xy + 1):
                for k in range(-max_dim_z, max_dim_z + 1):
                    _, onQty = getOnNb3D(on_bulbs, (i, j, k))
                    if (i, j, k) not in on_bulbs and onQty == 3:
                        new_on.add((i, j, k))
                    if (i, j, k) in on_bulbs and onQty in [2, 3]:
                        new_on.add((i, j, k))
        on_bulbs = new_on

    return len(on_bulbs)


def day17p1():
    data = get_input(parse1, test=False)
    print(data)
    return boot_energy_source_3D(data)


def parse2(line):
    return parse1(line)


def getOnNb4D(on_bulbs, coordinate):
    x, y, z, w = coordinate
    adj = set()
    deltas = [-1, 0, 1]

    for i in deltas:
        for j in deltas:
            for k in deltas:
                for l in deltas:
                    if (x+i, y+j, z+k, w+l) in on_bulbs:
                        adj.add((x+i, y+j, z+k, w+l))

    adj.discard((x, y, z, w))

    return adj, len(adj)


def boot_energy_source_4D(initial_slice, cycles=6):
    on_bulbs = set()

    for r, R in enumerate(initial_slice):
        for c, val in enumerate(R):
            if val == 1:
                on_bulbs.add((r, c, 0, 0))

    max_dim_xy = len(initial_slice) + cycles
    max_dim_z = cycles

    for _ in range(cycles):
        new_on = set()

        for x in range(-max_dim_xy, max_dim_xy + 1):
            for y in range(-max_dim_xy, max_dim_xy + 1):
                for z in range(-max_dim_z, max_dim_z + 1):
                    for w in range(-max_dim_z, max_dim_z + 1):
                        _, nbr = getOnNb4D(on_bulbs, (x, y, z, w))
                        if (x, y, z, w) not in on_bulbs and nbr == 3:
                            new_on.add((x, y, z, w))
                        if (x, y, z, w) in on_bulbs and nbr in [2, 3]:
                            new_on.add((x, y, z, w))
        on_bulbs = new_on

    return len(on_bulbs)


def day17p2():
    data = get_input(parse2, test=False)
    return boot_energy_source_4D(data)


def main():
    print("Day 17 - Part 1")
    print(day17p1())

    print("Day 17 - Part 2")
    print(day17p2())


main()

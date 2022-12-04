import copy
import heapq
from typing import List


def get_filename(test=False):
    return f'day15_input{"_test" if test else ""}.txt'


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


def parse1(line: str):
    return list(map(int, list(line)))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def adjacents(x, y, matrix):
    adj = set()

    wy = len(matrix)
    wx = len(matrix[0])

    for cy in range(max(0, y - 1), min(wy, y + 2)):
        adj.add((x, cy))
    for cx in range(max(0, x - 1), min(wx, x + 2)):
        adj.add((cx, y))

    adj.discard((x, y))

    return adj


def dijkstra(matrix, start, target):
    dist = dict()

    dist[start] = 0


    todo = [(start, 0)]

    while len(todo) > 0:
        node, cost = heapq.heappop(todo)

        for x, y in adjacents(node[0], node[1], matrix):
            new_cost = cost + matrix[y][x]
            if (x, y) not in dist or new_cost < dist[(x, y)]:
                dist[(x, y)] = new_cost
                heapq.heappush(todo, ((x, y), new_cost))

    return dist[target]


################################################################################


def day15p1():
    data = get_input(parse1, test=False)

    lrx = len(data[0]) - 1
    lry = len(data) - 1

    return dijkstra(data, (0, 0), (lrx, lry))


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################
def inc(items: List[int], wrap: int):
    return [(i % wrap) + 1 for i in items]


def expand_map(mapping, times):
    nm = []

    for y in range(len(mapping) * times):
        nrow = []

        cp: list = copy.copy(mapping[y % len(mapping)])

        for _ in range(y // len(mapping)):
            cp = inc(cp, 9)

        for _ in range(times):
            nrow.extend(cp.copy())
            cp = inc(cp, 9)

        nm.append(nrow.copy())

    return nm


################################################################################


def day15p2():
    data = get_input(parse2, test=False)
    nm = expand_map(data, 5)

    # for p in nm:
    #     print(''.join(map(str, p)))

    lrx = len(nm[0]) - 1
    lry = len(nm) - 1

    print(lrx, lry)

    # for i in nm:
    #     print(''.join(map(str, i)))

    return dijkstra(nm, (0, 0), (lrx, lry))


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 15 - Part 1", "-" * n)
    print("Result =>", day15p1())
    print()
    print("-" * (n), "Day 15 - Part 2", "-" * n)
    print("Result =>", day15p2())
    print()


main()

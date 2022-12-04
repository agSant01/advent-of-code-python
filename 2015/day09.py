import itertools
import sys


def get_filename(test=False):
    return f'day09_input{"_test" if test else ""}.txt'


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
    nodes, cost = line.split(" = ")
    nodes = nodes.split(" to ")
    return (nodes, cost)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def calc_floyd_warshall(data, nodes: int, loc_map):
    # V x V Matrix
    dist = [[sys.maxsize for _ in range(nodes)] for _ in range(nodes)]

    for edge in data:
        fromV, toV = edge[0]
        cost = edge[1]
        dist[loc_map[fromV]][loc_map[toV]] = int(cost)
        dist[loc_map[toV]][loc_map[fromV]] = int(cost)

    for i in range(nodes):
        dist[i][i] = 0

    for k in range(len(dist)):
        for i in range(len(dist)):
            for j in range(len(dist)):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


################################################################################


def day09p1():
    data = get_input(parse1, test=False)

    nodes = set()
    for d in data:
        fromV, toV = d[0]
        nodes.update([fromV, toV])

    vert_map = {}
    for idx, vert in enumerate(nodes):
        vert_map.update({vert: idx})

    #  init distance matrix and calculate min distance between nodes
    floyd_marshal_dist = calc_floyd_warshall(data, len(nodes), vert_map)

    result = sys.maxsize
    for permutation in itertools.permutations(range(len(nodes))):
        cost = 0
        previous = permutation[0]
        for node in permutation:
            cost += floyd_marshal_dist[previous][node]
            previous = node
        if cost < result:
            result = cost

    return "Shortest Len:", result


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day09p2():
    data = get_input(parse2, test=False)

    nodes = set()
    for d in data:
        fromV, toV = d[0]
        nodes.update([fromV, toV])

    vert_map = {}
    for idx, vert in enumerate(nodes):
        vert_map.update({vert: idx})

    nodes = len(nodes)

    dist = [[sys.maxsize for _ in range(nodes)] for _ in range(nodes)]

    # Init distance matrix
    for edge in data:
        fromV, toV = edge[0]
        cost = edge[1]
        dist[vert_map[fromV]][vert_map[toV]] = int(cost)
        dist[vert_map[toV]][vert_map[fromV]] = int(cost)

    for i in range(nodes):
        dist[i][i] = 0

    # calculate the paths of every permutation
    result = 0
    for permutation in itertools.permutations(range(nodes)):
        cost = 0
        previous = permutation[0]
        for node in permutation:
            cost += dist[previous][node]
            previous = node
        if cost > result:
            result = cost

    return "Longest path", result


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 09 - Part 1", "-" * n)
    print("Result =>", day09p1())
    print()
    print("-" * (n), "Day 09 - Part 2", "-" * n)
    print("Result =>", day09p2())
    print()


main()

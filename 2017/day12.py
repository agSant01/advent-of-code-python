import sys


def get_filename(test=False):
    return f'day12_input{"_test" if test else ""}.txt'


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
    line = line.replace(" ", "")
    node, neighbors = line.split("<->")
    return int(node), [int(n) for n in neighbors.split(",")]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def create_graph(nodes: list):
    graph = {}
    for node in nodes:
        graph[node[0]] = node[1]
    return graph


################################################################################


def day12p1():
    data = get_input(parse1, test=False)

    graph = create_graph(data)

    visited = set()
    to_visit = [0]
    while len(to_visit) > 0:
        current_node = to_visit.pop()

        if current_node in visited:
            continue

        visited.add(current_node)

        for n in graph[current_node]:
            if n in visited:
                continue
            to_visit.append(n)

    print(visited)
    return len(visited)


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day12p2():
    data = get_input(parse2, test=False)
    graph = create_graph(data)
    groups = 0
    globally_visited = set()
    for node_id in graph:
        if node_id in globally_visited:
            continue
        to_visit = [node_id]
        visited = set()
        is_globally_visited = False
        while len(to_visit) > 0:
            current_node = to_visit.pop()

            if current_node in visited:
                continue

            if current_node in globally_visited:
                is_globally_visited = True
                break

            globally_visited.add(current_node)
            visited.add(current_node)

            for n in graph[current_node]:
                if n in visited:
                    continue
                to_visit.append(n)

        if is_globally_visited:
            continue

        groups += 1

    return groups


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print("-" * (n), "Day 12 - Part 1", "-" * n)
        print("Result =>", day12p1())
        print()
    if run_two:
        print("-" * (n), "Day 12 - Part 2", "-" * n)
        print("Result =>", day12p2())
    print()


main()

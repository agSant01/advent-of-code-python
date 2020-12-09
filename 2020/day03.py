def get_input(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line))
    return data


def parse(line):
    return line.strip()


def day3p1():
    trees = get_input("day03_input.txt")
    x = 0
    trees_seen = 0
    for y in range(1, len(trees)):
        tree = trees[y]
        x += 3
        if tree[x % len(tree)] == '#':
            trees_seen += 1

    return trees_seen


def traverse_with_slope(deltaRight, deltaDown, trees):
    x = 0
    trees_seen = 0
    for y in range(deltaDown, len(trees), deltaDown):
        tree = trees[y]
        x += deltaRight
        if tree[x % len(tree)] == '#':
            trees_seen += 1

    return trees_seen


def day3p2():
    trees = get_input('day03_input_test.txt')

    # tupple (deltaRight , deltaDown)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    res = []
    for slope in slopes:
        res.append(traverse_with_slope(slope[0], slope[1], trees))

    mult = 1
    for r in res:
        mult *= r
    return mult


def main():
    print("Day 03 - Part 1")
    print(day3p1())

    print("Day 03 - Part 2")
    print(day3p2())


main()

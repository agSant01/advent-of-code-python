import yearutils as yu


def get_filename(test=False, opt=''):
    return f'day07_input{f"_test{opt}" if test else ""}.txt'


def parse1(line: str):
    # (adj color) : { (adj color):qty }
    bags = line.split('contain')

    restOfBags = bags[1].strip()

    # bags_dict = dict()
    dict_to_ret = dict()
    bags_dict = set()

    dict_to_ret[bags[0].replace('bags', '').replace(
        'bag', '').strip()] = bags_dict
    for bag_data in restOfBags.split(','):
        qty = bag_data.split()[0]

        if qty == 'no':
            continue

        bag = " ".join(bag_data.split()[1:]).replace(
            'bags', '').replace('bag', '').strip()
        bags_dict.add(bag.replace('.', '').strip())

    return dict_to_ret


def parse2(line: str):
    # (adj color) : { (adj color):qty }
    bags = line.split('contain')

    restOfBags = bags[1].strip()

    bags_dict = dict()
    dict_to_ret = dict()

    dict_to_ret[bags[0].replace(' bags', '').strip()] = bags_dict
    for bag_data in restOfBags.split(','):
        qty = bag_data.split()[0]

        if qty == 'no':
            continue

        bag = " ".join(bag_data.split()[1:]).replace(
            ' bags', '').replace(
            ' bag', '').replace('.', '')
        bags_dict[bag] = qty

    return dict_to_ret


def find_parents(find, g_dict):
    parents = []
    for r in g_dict.keys():
        if find in g_dict[r]:
            parents.append(r)
    return parents


def day07p1():
    data = yu.get_input(get_filename(test=False), parse1)
    g_dict = dict()

    for d in data:
        g_dict.update(d)

    can_contain = set()
    stack = ['shiny gold']
    visited = []
    while len(stack) != 0:
        bag = stack.pop()

        if bag in visited:
            continue

        visited.append(bag)

        parents = find_parents(bag, g_dict)

        can_contain.update(parents)

        for p in parents:
            if p not in visited:
                stack.append(p)

    return len(can_contain)


def find_childs(parent, g_dict):
    childs = []
    for inside in g_dict[parent].items():
        childs.append(inside)
    return childs


def day07p2():
    data = yu.get_input(get_filename(test=False, opt=''), parse2)
    g_dict = dict()

    for d in data:
        g_dict.update(d)

    total_sum = 0

    stack = [('shiny gold', 1)]
    while len(stack) != 0:
        bag, qty = stack.pop()

        if g_dict.get(bag) is None:
            continue

        for child in find_childs(bag, g_dict):
            total_sum += int(qty) * int(child[1])
            stack.append((child[0], int(qty) * int(child[1])))

    return total_sum


def main():
    print("Day 07 - Part 1")
    print(day07p1())

    print("Day 07 - Part 2")
    print(day07p2())


main()

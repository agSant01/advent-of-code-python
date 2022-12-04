import collections
import sys
from typing import Dict, List


def get_filename(test=False):
    return f'day07_input{"_test" if test else ""}.txt'


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
    info: List[str] = line.split()
    weight = info[1].replace("(", "").replace(")", "")

    children = []
    if len(info) > 2:
        children = list(map(lambda x: x.replace(",", ""), info[3:]))

    return Disk(info[0], int(weight), children)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


class Disk:
    def __init__(self, name, weight, children) -> None:
        self.name = name
        self.weight = weight
        self.children: List[str] = children
        self.parent = None
        self.sub_tree_weight = None

    def get_children(self, table) -> List:
        return [table[nb_name] for nb_name in self.children]

    def __str__(self) -> str:
        return (
            "<Disk"
            f" name={self.name} weight={self.weight} tw={self.sub_tree_weight} parent={self.parent.name if self.parent else None} children={self.children}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


def get_parent(table: Dict[str, Disk], start_node: Disk):
    if start_node.parent:
        return

    # search all table to find parent node
    for node_name, node_obj in table.items():
        node_obj: Disk
        if start_node.name in node_obj.children:
            start_node.parent = table[node_name]
            break

    if start_node.parent is None:
        return start_node

    return None


def get_root(table: Dict[str, Disk]):
    # search all table to find parent node
    for node_obj in table.values():
        node_obj: Disk
        get_parent(table, node_obj)

    for node_obj in table.values():
        if node_obj.parent is None:
            return node_obj


def build_table(data: List[Disk]):
    _table = {}
    for disk in data:
        _table[disk.name] = disk
    return _table


################################################################################


def day07p1():
    data: List[Disk] = get_input(parse1, test=True)

    disk_mapping_table = build_table(data)
    root = get_root(disk_mapping_table)
    print(root)

    return root.name


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def get_weights(table: Dict[str, Disk], root: Disk):
    weight = root.weight
    for child in root.get_children(table):
        child: Disk
        weight += get_weights(table, child)
    root.sub_tree_weight = weight
    return weight


def has_balanced_children(table: dict, root: Disk):
    children = root.get_children(table)
    counter = collections.defaultdict(int)
    for child in children:
        counter[child.sub_tree_weight] += 1
    return len(counter) > 1


def balance_weights(table, root: Disk, value=None):
    new_value = None
    children = root.get_children(table)
    counter = collections.defaultdict(int)
    for child in children:
        counter[child.sub_tree_weight] += 1

    if len(counter) > 1:
        pivot = None
        pivot_stw = None
        other_stw = None
        for value, count in counter.copy().items():
            if count == 1:
                pivot_stw = value
                counter.pop(value)

        for child in children:
            if child.sub_tree_weight == pivot_stw:
                pivot = child
                break
        other_stw, _ = counter.popitem()
        diff_ = pivot.sub_tree_weight - other_stw
        new_value = pivot.weight - diff_
        return balance_weights(table, pivot, new_value)

    return value


################################################################################
def day07p2():
    data = get_input(parse2, test=False)
    disk_mapping_table = build_table(data)
    root = get_root(disk_mapping_table)

    get_weights(disk_mapping_table, root)

    print("root", root)
    dw = balance_weights(disk_mapping_table, root)
    return dw


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
        print("-" * (n), "Day 07 - Part 1", "-" * n)
        print("Result =>", day07p1())
        print()
    if run_two:
        print("-" * (n), "Day 07 - Part 2", "-" * n)
        print("Result =>", day07p2())
    print()


main()

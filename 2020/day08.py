from os import curdir
import utils as ut


def get_filename(test=False):
    return f'day08_input{"_test" if test else ""}.txt'


def parse(line):
    cmd_prm = line.split()
    return (cmd_prm[0], int(cmd_prm[1]))


def day08p1():
    data = ut.get_input(get_filename(test=False), parse)

    cntr = 0
    curr_ = 0
    visited = set()

    while curr_ < len(data):
        if curr_ in visited:
            return cntr

        visited.add(curr_)

        curr_inst = data[curr_]

        if curr_inst[0] == 'acc':
            cntr += curr_inst[1]
            curr_ += 1
        elif curr_inst[0] == 'jmp':
            curr_ += curr_inst[1]
        elif curr_inst[0] == 'nop':
            curr_ += 1
        else:
            print('Invalid cmd:', data[curr_][0], 'Instr:', curr_)
            exit(1)

    return cntr


def switch_instr(curr, instr):
    prev = instr[curr]
    if prev[0] == 'jmp':
        instr[curr] = ('nop', int(prev[1]))
    elif prev[0] == 'nop':
        instr[curr] = ('jmp', int(prev[1]))
    else:
        print('INvalid op')
        exit(1)

    return instr


def run_boot(data):
    cntr = 0
    curr_ = 0
    visited = set()

    while curr_ < len(data):
        if curr_ in visited:
            # print('Repeated cmd:', data[curr_], 'Instr:', curr_)
            return None

        visited.add(curr_)

        curr_inst = data[curr_]

        if curr_inst[0] == 'acc':
            cntr += curr_inst[1]
            curr_ += 1
        elif curr_inst[0] == 'jmp':
            curr_ += curr_inst[1]
        elif curr_inst[0] == 'nop':
            curr_ += 1
        else:
            print('Invalid cmd:', data[curr_][0], 'Instr:', curr_)
            return None

    return cntr


def day08p2():
    original = ut.get_input(get_filename(test=False), parse)
    check_points = []
    for idx, val in enumerate(original):
        if val[0] in ['jmp', 'nop']:
            check_points.append(idx)

    for cp in check_points:
        new_instr = switch_instr(cp, original.copy())
        res = run_boot(new_instr)
        if res:
            return res


def main():
    print("Day 08 - Part 1")
    print(day08p1())

    print("Day 08 - Part 2")
    print(day08p2())


main()

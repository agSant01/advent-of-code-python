import re


def get_filename(test=False):
    return f'day14_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data

################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    return line.split(' = ')

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def get_val(value: int, mask: str):
    res = []
    for vb, mb in zip(bin(value)[2:].zfill(36), mask):
        res.append(vb if mb == 'X' else mb)
    return int(''.join(res), base=2)


def run_program(program, memory: dict):
    curr_mask = None
    for instruction in program:
        if instruction[0] == 'mask':
            curr_mask = instruction[1]
        elif 'mem' in instruction[0]:
            s: str = instruction[0].index('[')
            e: str = instruction[0].index(']')
            memory[
                int(instruction[0][s+1: e])
            ] = get_val(int(instruction[1]), curr_mask)

################################################################################


def day14p1():
    program = get_input(parse1, test=False)

    memory = dict()

    run_program(program, memory)

    return sum(memory.values())

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def decode_addresses(value: int, mask: str):
    values = []
    masked_val = []
    for vb, mb in zip(bin(value)[2:].zfill(36), mask):
        if mb == '0':
            masked_val.append(vb)
        else:
            masked_val.append(mb)

    values.append(masked_val)

    cnt = masked_val.count('X')

    while len(values) != 2 ** cnt:
        mv: list = values.pop(0)

        try:
            i = mv.index('X')
        except:
            i = -1
            values.append(mv)

        while 0 <= i < 36:
            if mv[i] == 'X':
                mv[i] = '0'
                values.append(mv.copy())
                mv[i] = '1'
                values.append(mv.copy())
                break
            i += 1
    return list(int(v, base=2) for v in map(''.join, values))


def run_program_v2(program, memory: dict):
    curr_mask = None
    for instruction in program:
        if instruction[0] == 'mask':
            curr_mask = instruction[1]
        elif 'mem' in instruction[0]:
            s: str = instruction[0].index('[')
            e: str = instruction[0].index(']')
            encoded_addr = int(instruction[0][s+1: e])
            for address in decode_addresses(encoded_addr, curr_mask):
                memory[address] = int(instruction[1])


################################################################################
def day14p2():
    program = get_input(parse2, test=False)

    memory = dict()

    run_program_v2(program, memory)

    return sum(memory.values())


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 21 - Part 1", '-'*n)
    print('Result =>', day14p1())
    print()
    print('-'*(n), "Day 21 - Part 2", '-'*n)
    print('Result =>', day14p2())
    print()


main()

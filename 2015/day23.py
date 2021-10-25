def get_filename(test=False):
    return f'day23_input{"_test" if test else ""}.txt'


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
    opcode, params = line.split(' ', 1)
    params = params.replace(' ', '').split(',')
    return (opcode, params)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


"""
hlf r sets register r to half its current value, then continues with the next instruction.
tpl r sets register r to triple its current value, then continues with the next instruction.
inc r increments register r, adding 1 to it, then continues with the next instruction.
jmp offset is a jump; it continues with the instruction offset away relative to itself.
jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
"""


def execute(pc, register, opcode, params):
    r = 0 if params[0] == 'a' else 1
    if opcode == 'hlf':
        register[r] //= 2
    if opcode == 'tpl':
        register[r] *= 3
    if opcode == 'inc':
        register[r] += 1
    if opcode == 'jmp':
        pc += int(params[0]) - 1
    if opcode == 'jie':
        if register[r] % 2 == 0:
            pc += int(params[1]) - 1
    if opcode == 'jio':
        if register[r] == 1:
            pc += int(params[1]) - 1

    return pc + 1


def run_program(registers: list, instructions: list):
    pc = 0
    instr_len = len(instructions)
    while pc < instr_len:
        instruction = instructions[pc]
        pc = execute(pc, registers, instruction[0], instruction[1])

################################################################################


def day23p1():
    data = get_input(parse1, test=False)
    for d in data:
        print(d)

    registers = [0, 0]  # [A, B]

    run_program(registers, data)

    print('registers', registers)

    return registers[1]


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day23p2():
    data = get_input(parse2, test=False)

    for d in data:
        print(d)

    registers = [1, 0]  # [A, B]

    run_program(registers, data)

    print('registers', registers)

    return registers[1]


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 23 - Part 1", '-'*n)
    print('Result =>', day23p1())
    print()
    print('-'*(n), "Day 23 - Part 2", '-'*n)
    print('Result =>', day23p2())
    print()


main()

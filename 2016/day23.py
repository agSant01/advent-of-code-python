import copy


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
    return line.split()

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


"""
`cpy x y` *copies* `x` (either an integer or the *value* of a register) into register `y`.
* `inc x` *increases* the value of register `x` by one.
* `dec x` *decreases* the value of register `x` by one.
* `jnz x y` *jumps* to an instruction `y` away (positive means forward; negative means backward), but only if `x` is *not zero*.
"""

LET_TO_INT = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
}


def tgl(instruction, registers, program):
    x = instruction[1]
    if x in 'abcd':
        x = registers[LET_TO_INT[x]]

    print(instruction, x)

    if x < 0 or x > len(program):
        return

    target_inst = program[x]

    print(target_inst)

    if len(target_inst[:1]) == 1:
        if target_inst[0] == 'inc':
            program[x][0] = 'dec'
        else:
            program[x][0] = 'inc'
    else:
        if target_inst[0] == 'jnz':
            program[x][0] = 'cpy'
        else:
            program[x][0] = 'jnz'

    print('prog', program[x])


def execute(instruction, registers, pc, program):
    opcode = instruction[0]

    if pc == 4:
        a, b, c, d = LET_TO_INT['a'], LET_TO_INT['b'], LET_TO_INT['c'],  LET_TO_INT['d']
        registers[a] = registers[b]*registers[d]
        registers[c] = 0
        registers[d] = 0
        return pc+6

    if opcode == 'inc':
        x = instruction[1]
        registers[LET_TO_INT[x]] += 1
    elif opcode == 'dec':
        x = instruction[1]
        registers[LET_TO_INT[x]] -= 1
    elif opcode == 'jnz':
        x, y = instruction[1:]
        if x in 'abcd':
            x = registers[LET_TO_INT[x]]
        if y in 'abcf':
            y = registers[LET_TO_INT[y]]
        if int(x) != 0:
            pc += int(y) - 1
    elif opcode == 'cpy':
        x, y = instruction[1:]
        if x in 'abcd':
            x = registers[LET_TO_INT[x]]
        registers[LET_TO_INT[y]] = int(x)
    elif opcode == 'tgl':
        x = instruction[1]
        if x in 'abcd':
            x = registers[LET_TO_INT[x]]

        if 0 <= pc+x < len(program):
            target_inst = program[pc+x]
            if len(target_inst[1:]) == 1:
                if target_inst[0] == 'inc':
                    program[pc+x][0] = 'dec'
                else:
                    program[pc+x][0] = 'inc'
            else:
                if target_inst[0] == 'jnz':
                    program[pc+x][0] = 'cpy'
                else:
                    program[pc+x][0] = 'jnz'
    else:
        raise Exception('INVALID OPCODE:' + opcode)

    return pc + 1


def run_program(program, registers):
    pc = 0
    while pc < len(program):
        inst = program[pc]
        # print('pc', pc, 'inst', inst)
        pc = execute(inst, registers, pc, program)
        # print(registers)
    return registers

################################################################################


def day23p1():
    program = get_input(parse1, test=False)

    result = run_program(program, [7, 0, 0, 0])

    return result

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
    program = get_input(parse2, test=False)

    result = run_program(copy.deepcopy(program), [12, 0, 0, 0])

    return result


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



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
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
}


def execute(instruction, registers, pc):
    opcode = instruction[0]
    if opcode == "cpy":
        x, y = instruction[1:]
        if x in "abcd":
            x = registers[LET_TO_INT[x]]
        registers[LET_TO_INT[y]] = int(x)
    elif opcode == "inc":
        x = instruction[1]
        registers[LET_TO_INT[x]] += 1
    elif opcode == "dec":
        x = instruction[1]
        registers[LET_TO_INT[x]] -= 1
    elif opcode == "jnz":
        x, y = instruction[1:]
        if x in "abcd":
            x = registers[LET_TO_INT[x]]
        if int(x) != 0:
            pc += int(y) - 1
    else:
        raise Exception("INVALID OPCODE:" + opcode)

    return pc + 1


################################################################################


def run_program(program, registers):
    pc = 0
    while pc < len(program):
        inst = program[pc]
        # print('pc', pc, 'inst', inst)
        pc = execute(inst, registers, pc)
        # print(registers)
    return registers


def day12p1():
    program = get_input(parse1, test=False)

    registers = [0, 0, 0, 0]
    run_program(program, registers)

    return registers


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
    program = get_input(parse2, test=False)

    registers = [0, 0, 1, 0]
    run_program(program, registers)

    return registers


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 12 - Part 1", "-" * n)
    print("Result =>", day12p1())
    print()
    print("-" * (n), "Day 12 - Part 2", "-" * n)
    print("Result =>", day12p2())
    print()


main()

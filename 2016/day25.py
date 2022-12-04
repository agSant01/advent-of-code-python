import queue


def get_filename(test=False):
    return f'day25_input{"_test" if test else ""}.txt'


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

STREAM = queue.Queue()


def io_stdout(value):
    STREAM.put(value)


def read_from_stream():
    if STREAM.qsize() == 0:
        return "<empty>"
    return STREAM.get()


def execute(instruction, registers, pc, program):
    opcode = instruction[0]

    if opcode == "inc":
        x = instruction[1]
        registers[x] += 1
    elif opcode == "dec":
        x = instruction[1]
        registers[x] -= 1
    elif opcode == "jnz":
        x, y = instruction[1:]
        if x in "abcd":
            x = registers[x]
        if y in "abcd":
            y = registers[y]
        if int(x) != 0:
            pc += int(y) - 1
    elif opcode == "cpy":
        x, y = instruction[1:]
        if x in "abcd":
            x = registers[x]
        registers[y] = int(x)
    elif opcode == "tgl":
        x = instruction[1]
        if x in "abcd":
            x = registers[x]

        if 0 <= pc + x < len(program):
            target_inst = program[pc + x]
            if len(target_inst[1:]) == 1:
                if target_inst[0] == "inc":
                    program[pc + x][0] = "dec"
                else:
                    program[pc + x][0] = "inc"
            else:
                if target_inst[0] == "jnz":
                    program[pc + x][0] = "cpy"
                else:
                    program[pc + x][0] = "jnz"
    elif opcode == "out":
        x = instruction[1]
        if x in "abcd":
            x = registers[x]
        io_stdout(x)
    else:
        raise Exception("INVALID OPCODE:" + opcode)

    return pc + 1


next_ = {1: 0, 0: 1}


def run_program(program, registers):
    pc = 0
    clk = 0
    clk_cycles = 0
    while pc < len(program):
        inst = program[pc]
        # print('pc', pc, 'inst', inst)

        pc = execute(inst, registers, pc, program)

        out = read_from_stream()

        if out == "<empty>":
            continue

        # print('stdout:', out)

        if out != clk:
            return 1  # invalid next clock

        clk = next_[clk]
        clk_cycles += 1

        if clk_cycles > 1000:
            return 0

    return 0


################################################################################
def day25p1():
    program = get_input(parse1, test=False)

    for i in range(30, 500):
        registers = {"a": i, "b": 0, "c": 0, "d": 0}
        exit_result = run_program(program, registers)
        if exit_result == 0:
            return f"a: {i}", registers

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
def day25p2():
    data = get_input(parse2, test=True)
    for d in data:
        pass


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 25 - Part 1", "-" * n)
    print("Result =>", day25p1())
    print()
    print("-" * (n), "Day 25 - Part 2", "-" * n)
    print("Result =>", day25p2())
    print()


main()

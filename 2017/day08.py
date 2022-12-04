import collections
import sys
from typing import List


def get_filename(test=False):
    return f'day08_input{"_test" if test else ""}.txt'


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


def get_condition(instruction: List[str], registers):
    register, condition, value = instruction[4:]

    computation = False  # default state: "do nothing"

    if condition == "<":
        computation = registers[register] < int(value)
    elif condition == ">":
        computation = registers[register] > int(value)
    elif condition == "==":
        computation = registers[register] == int(value)
    elif condition == "!=":
        computation = registers[register] != int(value)
    elif condition == ">=":
        computation = registers[register] >= int(value)
    elif condition == "<=":
        computation = registers[register] <= int(value)
    else:
        print("Error: Instruction not valid", instruction)

    return computation


def execute_instructions(registers, instructions):
    max_value = -1 * sys.maxsize
    for inst in instructions:
        if get_condition(inst, registers):
            value = int(inst[2])
            if inst[1] == "inc":
                registers[inst[0]] += value
            elif inst[1] == "dec":
                registers[inst[0]] -= value
            if registers[inst[0]] > max_value:
                max_value = registers[inst[0]]

    return max_value


################################################################################


def day08p1():
    data = get_input(parse1, test=False)

    registers = collections.defaultdict(int)

    execute_instructions(registers, data)

    return max(registers.values())


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day08p2():
    data = get_input(parse2, test=False)

    registers = collections.defaultdict(int)

    max_ = execute_instructions(registers, data)

    return max_


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
        print("-" * (n), "Day 08 - Part 1", "-" * n)
        print("Result =>", day08p1())
        print()
    if run_two:
        print("-" * (n), "Day 08 - Part 2", "-" * n)
        print("Result =>", day08p2())
    print()


main()

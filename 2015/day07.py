import collections


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


def parse1(line):
    temp = line.split("->")

    return {"instruction": temp[0].strip().split(" "), "out": temp[1].strip()}


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def decode_wire(variable_table, wire):
    inst = variable_table[wire]
    # print('Wire', wire, inst)

    result = None

    if not isinstance(inst, list):
        return str(inst)

    if len(inst) == 1:
        # <pos0>
        pos0 = inst[0]
        if pos0.isdigit():
            result = pos0
        else:
            result = decode_wire(variable_table, pos0)
        variable_table[wire] = str(result)
    elif "NOT" in inst:
        # NOT <pos0>
        print("[NOT]", inst)
        pos0 = inst[1]
        if pos0 in variable_table:
            pos0_res = decode_wire(variable_table, pos0)
        elif pos0.isdigit():
            pos0_res = int(pos0)
        else:
            raise Exception(f"Inst:{inst}, {pos0} not Valid")
        result = int(pos0_res) ^ 65535
        variable_table[wire] = str(result)

    elif "OR" in inst:
        # <pos0> OR <pos1>
        # print('[OR]', inst)
        pos0, _, pos1 = inst
        pos0_res, pos1_res = None, None
        # print(pos0,  pos1)
        if pos0 in variable_table:
            pos0_res = decode_wire(variable_table, pos0)
        elif pos0.isdigit():
            pos0_res = int(pos0)
        else:
            raise Exception(f"Inst:{inst}, {pos0} not Valid")

        if pos1 in variable_table:
            pos1_res = decode_wire(variable_table, pos1)
        elif pos1.isdigit():
            pos1_res = int(pos1)
        else:
            raise Exception(f"Inst:{inst}, {pos1} not Valid")

        result = int(pos0_res) | int(pos1_res)
        variable_table[wire] = str(result)

    elif "AND" in inst:
        # <pos0> AND <pos1>
        # print('[AND]', inst)
        pos0, _, pos1 = inst
        pos0_res, pos1_res = None, None
        # print(pos0,  pos1)
        if pos0 in variable_table:
            pos0_res = decode_wire(variable_table, pos0)
        elif pos0.isdigit():
            pos0_res = int(pos0)
        else:
            raise Exception(f"Inst:{inst}, {pos0} not Valid")

        if pos1 in variable_table:
            pos1_res = decode_wire(variable_table, pos1)
        elif pos1.isdigit():
            pos1_res = int(pos1)
        else:
            raise Exception(f"Inst:{inst}, {pos1} not Valid")

        result = int(pos0_res) & int(pos1_res)
        variable_table[wire] = str(result)

    elif "LSHIFT" in inst:
        # <pos0> LSHIFT <shift_left:int16>
        # print('[LSHIFT]', inst)
        pos0, _, shift_left = inst
        pos0_res = None

        # print(pos0,  shift_left)

        if pos0 in variable_table:
            pos0_res = decode_wire(variable_table, pos0)
        elif pos0.isdigit():
            pos0_res = int(pos0)
        else:
            raise Exception(f"Inst:{inst}, {pos0} not Valid")

        result = int(pos0_res) << int(shift_left)
        variable_table[wire] = str(result)

    elif "RSHIFT" in inst:
        # <pos0> LSHIFT <shift_left:int16>
        # print('[RSHIFT]', inst)
        pos0, _, shift_right = inst
        pos0_res = None

        # print(pos0,  shift_right)

        if pos0 in variable_table:
            pos0_res = decode_wire(variable_table, pos0)
        elif pos0.isdigit():
            pos0_res = int(pos0)
        else:
            raise Exception(f"Inst:{inst}, {pos0} not Valid")

        result = int(pos0_res) >> int(shift_right)
        variable_table[wire] = str(result)
    else:
        raise Exception(f"Inst:{inst}. Invalid")

    return str(result)


################################################################################


def day07p1():
    is_test = False
    data = get_input(parse1, test=is_test)

    variable_table = collections.defaultdict(list)

    wire_ = "a"
    if is_test:
        wire_ = "i"

    for d in data:
        out = d["out"]
        inst = d["instruction"]
        variable_table[out] += inst

    signal_a = decode_wire(variable_table, wire_)

    return signal_a, variable_table


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day07p2():
    is_test = False
    data = get_input(parse2, test=is_test)

    variable_table = collections.defaultdict(list)

    for d in data:
        out = d["out"]
        inst = d["instruction"]
        variable_table[out] += inst

    wire_ = "a"
    if is_test:
        wire_ = "i"

    signal_a = decode_wire(variable_table.copy(), wire_)

    variable_table["b"] = [signal_a]

    stat_2 = variable_table.copy()
    signal_b = decode_wire(stat_2, wire_)

    return signal_b, stat_2


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 07 - Part 1", "-" * n)
    print("Result =>", day07p1())
    print()
    print("-" * (n), "Day 07 - Part 2", "-" * n)
    print("Result =>", day07p2())
    print()


main()

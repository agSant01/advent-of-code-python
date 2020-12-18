def get_filename(test=False):
    return f'day18_input{"_test" if test else ""}.txt'


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
def parse1(line):
    return [char for char in line.strip().replace(' ', '')]

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def calculate(tokens, index=0):
    result = 0

    s = []
    idx = index
    while idx < len(tokens):
        token = tokens[idx]
        if token == '(':
            value, idx = calculate(tokens, idx + 1)
            s.append(value)

        if token == ')':
            break

        if token.isdigit() or token in ['+', '*']:
            s.append(token)

        idx += 1

    s.reverse()

    result = int(s.pop())
    while len(s) != 0:
        op = s.pop()
        num_b = int(s.pop())
        if op == '+':
            result += num_b

        if op == '*':
            result *= num_b
    return result, idx


################################################################################
def day18p1():
    tokenized_data = get_input(parse1, test=False)
    result = 0
    for d in tokenized_data:
        val, _ = calculate(d)
        result += val
    return result

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def calculate2(tokens, index=0):
    result = 0

    s = []
    idx = index
    while idx < len(tokens):
        token = tokens[idx]
        if token == '(':
            value, idx = calculate2(tokens, idx + 1)
            s.append(value)

        if token == ')':
            break

        if token.isdigit() or token in ['+', '*']:
            s.append(token)

        idx += 1
    n_s = []
    i = 0
    while i < len(s):
        if s[i] == '+':
            na = n_s.pop()
            i += 1
            nb = s[i]
            n_s.append(int(na)+int(nb))
        else:
            n_s.append(s[i])

        i += 1

    s = n_s
    result = int(s.pop())
    while len(s) != 0:
        op = s.pop()
        num_b = int(s.pop())
        if op == '+':
            result += num_b

        if op == '*':
            result *= num_b
    return result, idx


################################################################################
def day18p2():
    tokenized_data = get_input(parse2, test=True)
    result = 0
    for d in tokenized_data:
        val, _ = calculate2(d)
        result += val

    return result


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 18 - Part 1", '-'*n)
    print('Result =>', day18p1())
    print()
    print('-'*(n), "Day 18 - Part 2", '-'*n)
    print('Result =>', day18p2())
    print()



main()

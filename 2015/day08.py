import re


def get_filename(test=False):
    return f'day08_input{"_test" if test else ""}.txt'


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
    return line.strip()

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


hex_match = re.compile(r'\\x[a-z0-9]{2}')


def in_mem_len(s: str):
    s = s.replace('\\\\', '.')
    s = s.replace('\\\"', '"')
    matches = hex_match.findall(s)
    return len(s) - 3 * len(matches) - 2


################################################################################

def day08p1():
    data = get_input(parse1, test=False)

    string_code = 0
    in_memory_string_val = 0

    for strings_ in data:
        string_code += len(strings_)
        in_memory_string_val += in_mem_len(strings_)

    return (string_code, in_memory_string_val, string_code - in_memory_string_val)

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


q_match = re.compile(r'"')
s_match = re.compile(r'\\')


def encode_(s: str):
    qreq = len(q_match.findall(s))
    sreq = len(s_match.findall(s))
    return len(s) + qreq + sreq + 2

################################################################################


def day08p2():
    data = get_input(parse2, test=False)

    encoded_len = 0
    string_code = 0

    for strings_ in data:
        string_code += len(strings_)
        encoded_len += encode_(strings_)

    return (string_code, encoded_len, encoded_len - string_code)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 08 - Part 1", '-'*n)
    print('Result =>', day08p1())
    print()
    print('-'*(n), "Day 08 - Part 2", '-'*n)
    print('Result =>', day08p2())
    print()


main()

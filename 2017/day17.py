import sys


def get_filename(test=False):
    return f'day17_input{"_test" if test else ""}.txt'


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
    return int(line)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day17p1():
    steps = get_input(parse1, test=False)[0]
    buffer = [0]
    buffer_len = 1
    current_pos = 0
    for i in range(1, 2018):
        current_pos += steps+1
        if current_pos >= buffer_len:
            current_pos %= buffer_len
        buffer.insert(current_pos+1, i)
        buffer_len += 1

    return buffer[current_pos], buffer[current_pos+1], buffer[current_pos+2]


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day17p2():
    """Get the number next to the 0th index value. Follow the same logic as part 1, but we only need to track the 
    values that fall on index 1 to add (current_pos+1). Do not need to allocate an array for this.

    Returns:
        _type_: _description_
    """
    steps = get_input(parse2, test=False)[0]
    buffer_len = 1
    current_pos = 0
    last_num_in_first_idx = None
    for i in range(1, 50_000_000):
        current_pos += steps+1
        if current_pos >= buffer_len:
            current_pos %= buffer_len
        if current_pos+1 == 1:
            last_num_in_first_idx = i
        buffer_len += 1
    return last_num_in_first_idx


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print('-'*(n), "Day 17 - Part 1", '-'*n)
        print('Result =>', day17p1())
        print()
    if run_two:
        print('-'*(n), "Day 17 - Part 2", '-'*n)
        print('Result =>', day17p2())
    print()


main()

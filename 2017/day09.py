import sys


def get_filename(test=False):
    return f'day09_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day09p1():
    data = get_input(parse1, test=False)
    results = []
    for line in data:
        level = 0
        score = 0
        is_garbage = False
        i = 0
        while i < len(line):
            c = line[i]
            if c == '!':
                i += 1
            elif c == '<' and not is_garbage:
                # garbage
                is_garbage = True
            elif c == '>':
                # end garbage
                is_garbage = False
            elif c == '{' and not is_garbage:
                level += 1
            elif c == '}' and not is_garbage:
                score += level
                level -= 1

            i += 1

        results.append(score)
    return results
################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day09p2():
    data = get_input(parse2, test=False)
    results = []
    for line in data:
        level = 0
        score = 0
        is_garbage = False
        garbage_chars = 0
        i = 0
        while i < len(line):
            c = line[i]
            if c == '!':
                i += 1
            elif c == '<' and not is_garbage:
                # garbage
                is_garbage = True
            elif c == '>':
                # end garbage
                is_garbage = False
            elif is_garbage:
                garbage_chars += 1
            elif c == '{':
                level += 1
            elif c == '}':
                score += level
                level -= 1
            i += 1
        results.append(garbage_chars)
    return results


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
        print('-'*(n), "Day 09 - Part 1", '-'*n)
        print('Result =>', day09p1())
        print()
    if run_two:
        print('-'*(n), "Day 09 - Part 2", '-'*n)
        print('Result =>', day09p2())
    print()


main()

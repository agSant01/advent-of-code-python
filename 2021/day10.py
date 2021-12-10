def get_filename(test=False):
    return f'day10_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


SE_TABLE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

PAIRS = {
    ')': '(',
    ']': '[',
    '>': '<',
    '}': '{',
}


def syntax_error_score(chunk: str):
    open_ = []

    for bracket in chunk:
        if bracket in ['(', '[', '{', '<']:
            open_.append(bracket)
        elif PAIRS[bracket] == open_[-1]:
            open_.pop()
        else:
            return SE_TABLE[bracket]

    return 0


################################################################################
def day10p1():
    data = get_input(parse1, test=False)
    total_ses = 0
    for chunk in data:
        total_ses += syntax_error_score(chunk)
    return total_ses

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


AUTOCOMPLETE_TABLE = {
    '(': (1, ')'),
    '[': (2, ']'),
    '{': (3, '}'),
    '<': (4, '>'),
}


def autocomplete(chunk: str):
    auto_score = 0
    open_ = []

    for bracket in chunk:
        if bracket in ['(', '[', '{', '<']:
            open_.append(bracket)
        elif PAIRS[bracket] == open_[-1]:
            open_.pop()

    sequence = []
    for missing_pair in reversed(open_):
        bracket_score, closing = AUTOCOMPLETE_TABLE[missing_pair]
        auto_score = auto_score * 5 + bracket_score
        sequence.append(closing)

    return auto_score, ''.join(sequence)
################################################################################


def day10p2():
    data = get_input(parse2, test=True)

    incomplete = []
    for chunk in data:
        if syntax_error_score(chunk) == 0:
            incomplete.append(chunk)

    print('Total Incomplete:', len(incomplete))

    auto_scores = []
    for seq in incomplete:
        score, sequence = autocomplete(seq)
        # print(seq, sequence, score)
        auto_scores.append(score)

    return sorted(auto_scores)[len(auto_scores)//2]


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 10 - Part 1", '-'*n)
    print('Result =>', day10p1())
    print()
    print('-'*(n), "Day 10 - Part 2", '-'*n)
    print('Result =>', day10p2())
    print()


main()

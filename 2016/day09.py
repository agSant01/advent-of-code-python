

def get_filename(test=False):
    return f'day09_input{"_test" if test else ""}.txt'


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
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def decompress(line: str, only_count: bool = True):
    index = 0
    count = 0
    res = []
    while index < len(line):
        if line[index] == "(":
            closing_paren = line.find(")", index)

            format: str = line[index + 1 : closing_paren]

            span, repetitions = map(int, format.split("x"))

            repeat = line[closing_paren + 1 : closing_paren + span + 1]

            if not only_count:
                res.append(repeat * repetitions)

            count += span * repetitions

            index = closing_paren + span + 1
        else:
            res.append(line[index])
            index += 1
            count += 1

    if only_count:
        return count, None

    return count, "".join(res)


################################################################################
# 13867 - Wrong
# 123896
# 110057 -w rong
# 123924 - is too high 123924


def day09p1():
    lines = get_input(parse1, test=False)

    dec_len = 0
    for line in lines:
        dec_len += decompress(line, only_count=True)[0]

    return "Decompressed len", dec_len


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def decompress_v2(line: str, only_count: bool = True):
    index = 0
    count = 0
    res = []
    while index < len(line):
        if line[index] == "(":
            closing_paren = line.find(")", index)

            format: str = line[index + 1 : closing_paren]

            span, repetitions = map(int, format.split("x"))

            repeat = line[closing_paren + 1 : closing_paren + span + 1]

            if "(" in repeat:
                # print('Rep', repeat)
                dcount, text = decompress_v2(repeat, only_count)
                count += dcount * repetitions
                if text:
                    res.append(text * repetitions)
            else:
                count += span * repetitions

                if not only_count:
                    res.append(repeat * repetitions)

            index = closing_paren + span + 1

        else:
            res.append(line[index])
            index += 1
            count += 1

    if only_count:
        return count, None

    return count, "".join(res)


################################################################################


def day09p2():
    data = get_input(parse2, test=False)

    dec_len = 0
    for line in data:
        # print('New', line)
        count, string = decompress_v2(line, only_count=True)
        # print('Dec:', string, 'Len:', count)
        dec_len += count

    return "V2 Decompressed Len ", dec_len


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 09 - Part 1", "-" * n)
    print("Result =>", day09p1())
    print()
    print("-" * (n), "Day 09 - Part 2", "-" * n)
    print("Result =>", day09p2())
    print()


main()

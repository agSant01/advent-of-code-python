import functools
import itertools


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
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def has_abba(string: str):
    WINDOW = 3
    len_ = len(string)
    idx = 0
    while idx + WINDOW < len_:
        a, b, c, d = string[idx : idx + WINDOW + 1]
        if a != b and a == d and b == c:
            return True, idx, string[idx]
        idx += 1

    return False, idx, string[idx]


def supports_tls(ip: str):
    chunks = ip.replace("[", " ").replace("]", " ").split()
    can_have_abba = True
    is_valid = False
    for chunk in chunks:
        ha, _, _ = has_abba(chunk)
        if ha and can_have_abba:
            is_valid = True

        if ha and not can_have_abba:
            return False

        can_have_abba = not can_have_abba

    return is_valid


################################################################################


def day07p1():
    data = get_input(parse1, test=False)
    cnt = 0
    for d in data:
        cnt += supports_tls(d)

    return cnt


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def has_aba(string: str):
    WINDOW = 2
    len_ = len(string)
    idx = 0
    aba_list = []
    while idx + WINDOW < len_:
        a, b, c = string[idx : idx + WINDOW + 1]
        if a == c and a != b:
            aba_list.append(a + b + c)
        idx += 1

    return aba_list


def has_bab(string: str, abas: list):
    return len(list(itertools.filterfalse(lambda aba: aba not in string, abas))) > 0


def support_ssl(ip: str):
    chunks = ip.replace("[", " ").replace("]", " ").split()

    def allocate(list, item):
        list[item[0] % 2].append(item[1])
        return list

    supernet, hypernet = functools.reduce(allocate, enumerate(chunks), [[], []])

    bab_list = []
    for chunk in supernet:
        aba_list = has_aba(chunk)
        if len(aba_list) > 0:
            bab_list.extend(list(map(lambda x: x[1] + x[0] + x[1], aba_list)))

    for chunk in hypernet:
        if has_bab(chunk, bab_list):
            return True

    return False


################################################################################


def day07p2():
    is_test = False
    data = get_input(parse2, test=is_test)

    if is_test:
        data = [
            "aba[bab]xyz",
            "xyx[xyx]xyx",
            "aaa[kek]eke",
            "zazbz[bzb]cdb",
        ]

    counter = 0
    for d in data:
        counter += support_ssl(d)
    return counter


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

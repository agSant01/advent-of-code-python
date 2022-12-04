import re


def get_filename(test=False):
    return f'day19_input{"_test" if test else ""}.txt'


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


def getRules(lines):
    m = {}
    idx = 0
    for idx, line in enumerate(lines):
        if len(line) == 0:
            break
        divs = line.split(":")
        items = []
        for char in divs[1].split("|"):
            items.append(char.strip().replace('"', "").split())
        m[divs[0]] = items

    return m, idx + 1


def createRuleStr_rec(rules: dict, id: str, rep=None):
    rule = rules[id]

    if rep:
        if id == "8":
            rep[0] += 1
            if rep[0] > 10:
                return ""
        if id == "11":
            rep[1] += 1
            if rep[1] > 10:
                return ""

    if len(rule) == 1:
        if rule[0][0] in ["a", "b"]:
            return rule[0][0]

    curr = []
    for sr in rule:
        k = ""
        for item in sr:
            k += createRuleStr_rec(rules, item, rep)
        curr.append(k)

    return "(" + "|".join(curr) + ")"


################################################################################


def day19p1():
    data = get_input(parse1, test=False)
    rules, idx = getRules(data)
    data = data[idx:]

    cr = createRuleStr_rec(rules, "0")

    i = 0
    for d in data:
        if re.fullmatch(rf"{cr}", d):
            i += 1

    return i


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day19p2():
    data = get_input(parse2, test=False)

    rules, idx = getRules(data)

    rules["8"] = [["42"], ["42", "8"]]
    rules["11"] = [["42", "31"], ["42", "11", "31"]]

    data = data[idx:]

    cr = createRuleStr_rec(rules, "0", rep=[0, 0])

    i = 0
    for d in data:
        if re.fullmatch(rf"{cr}", d):
            i += 1

    return i


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 19 - Part 1", "-" * n)
    print("Result =>", day19p1())
    print()
    print("-" * (n), "Day 19 - Part 2", "-" * n)
    print("Result =>", day19p2())
    print()


main()

def get_filename(test=False):
    return f'day19_input{"_test" if test else ""}.txt'


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


def getRules(lines):
    m = {}
    idx = 0
    for idx, line in enumerate(lines):
        if len(line) == 0:
            break
        divs = line.split(':')
        items = []
        for char in divs[1].split('|'):
            items.append(char.strip().replace('\"', '').split())
        m[int(divs[0])] = items

    return m, idx + 1


def createRuleStr(rules):
    final_rule = ''
    import collections
    new_rules = collections.defaultdict(list)
    visited = set()
    stack = [(0, [])]
    while len(stack) > 0:
        id, rs = stack.pop()

        if id in visited:
            continue

        # see if subrule exists
        # if id in new_rules:
        print(id, rs)

        for sr in rules[int(id)]:
            for r in sr:
                if r in ['a', 'b']:
                    # stack.append((id, [r]))
                    new_rules[int(id)] = r
                else:
                    if int(r) in new_rules:
                        new_rules[id].append(new_rules[int(r)])
                    else:
                        stack.append((id, sr+r))

                print(r)

    print(new_rules)
    # for id, rule in rules.items():
    #     newSubRuleList = []
    #     for subRule in rule:
    #         if len(subRule) == 1 and subRule[0] in ['a', 'b']:
    #             newSubRuleList.append()


################################################################################


def day19p1():
    data = get_input(parse1, test=True)
    rules, idx = getRules(data)
    print(idx, rules)

    cr = createRuleStr(rules)
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
    data = get_input(parse2, test=True)
    for d in data:
        pass


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 19 - Part 1", '-'*n)
    print('Result =>', day19p1())
    print()
    print('-'*(n), "Day 19 - Part 2", '-'*n)
    print('Result =>', day19p2())
    print()


main()

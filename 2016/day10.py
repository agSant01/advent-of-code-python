import collections
import re


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
    if 'value' in line:
        return ['value', *re.findall('\d+|bot', line)]
    else:
        return re.findall(r'\d+|low|high|bot|output', line)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################

bot_map = collections.defaultdict(list)
output_map = collections.defaultdict(list)


def day10p1():
    data = get_input(parse1, test=False)
    queue = []

    for d in data:
        if d[0] == 'value':
            bot_map[d[-1]].append(int(d[1]))
        else:
            queue.append(d)

    the_bot = None
    while len(queue) > 0:
        d = queue.pop()
        bot = d[1]

        if bot not in bot_map:
            queue.insert(0, d)
            continue

        if len(bot_map[bot]) != 2:
            queue.insert(0, d)
            continue

        min_, max_ = min(bot_map[bot]), max(bot_map[bot])

        if min_ == 17 and max_ == 61:
            the_bot = bot

        bot_map[bot].clear()

        if d[3] == 'output':
            output_map[d[4]].append(min_)
        else:
            bot_map[d[4]].append(min_)

        if d[6] == 'output':
            output_map[d[7]].append(max_)
        else:
            bot_map[d[7]].append(max_)

    # print('bot', bot_map, 'out', output_map)

    return 'Bot', the_bot
################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day10p2():
    mult = 1
    for i in range(3):
        print(output_map[str(i)])
        mult *= output_map[str(i)][0]

    return mult


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

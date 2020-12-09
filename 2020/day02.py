def parse(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(tuple(line.strip().replace(':', '').split()))
    return data


def char_count(string, char):
    cnt = 0
    for c in string:
        if c == char:
            cnt += 1
    return cnt


def day2p1():
    passwords = parse("day02_input.txt")
    valid = 0
    for p in passwords:
        lower, upper = p[0].split('-')
        if int(lower) <= char_count(p[2], p[1]) <= int(upper):
            valid += 1

    return valid


def day2p2():
    passwords = parse("day02_input.txt")
    valid = 0
    for p in passwords:
        lower, upper = p[0].split('-')

        if p[2][int(lower)-1] == p[1] and p[2][int(upper)-1] == p[1]:
            continue

        if p[2][int(lower)-1] == p[1] or p[2][int(upper)-1] == p[1]:
            valid += 1

    return valid


def main():
    print("Day 02 - Part 1")
    print(day2p1())

    print("Day 02 - Part 2")
    print(day2p2())


main()

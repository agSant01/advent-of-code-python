def get_filename(test=False):
    return f'day16_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def parse1(line):
    return line


def isValid(t, rules):
    for field in t:
        f = False
        for r in rules.values():
            for c in r:
                # print(r, field)
                if c[0] <= int(field) <= c[1]:
                    f = True
        if f is False:
            return field, False

    return None, True


def day16p1():
    data = get_input(parse1, test=False)

    rules = {}
    my_ticket = []
    nearby_tickets = []
    currLine = 0
    while len(data[currLine]) != 0:
        line = data[currLine]
        line = line.split(':')
        ranges = list(map(lambda x: x.strip(), line[1].split(' or ')))

        key = line[0]

        rules[key] = list(
            map(lambda x: list(map(int, x.split('-'))), ranges))

        currLine += 1

    currLine += 2
    my_ticket = list(map(int, data[currLine].split(',')))

    currLine += 3
    while currLine < len(data) and len(data[currLine]) != 0:
        nearby_tickets.append(list(map(int, data[currLine].split(','))))
        currLine += 1
    # print(rules)
    # print(my_ticket)
    # print(nearby_tickets)

    invalid = []
    for n in nearby_tickets:
        value, f = isValid(n, rules)
        if not f:
            invalid.append(value)
    # print(invalid)
    # print(len(invalid))

    return sum(invalid)


def parse2(line):
    return parse1(line)


def getValidLocation(tck, rules):
    valid_locations = set(rules.keys())
    for f in tck:
        vt = set()
        for k, rs in rules.items():
            flg = False
            for r in rs:
                if r[0] <= f <= r[1]:
                    flg = True
            if flg:
                vt.add(k)
        valid_locations = valid_locations.intersection(vt)

    return valid_locations


def day16p2():
    data = get_input(parse2, test=False)

    rules = {}
    my_ticket = []
    nearby_tickets = []
    currLine = 0
    while len(data[currLine]) != 0:
        line = data[currLine]
        line = line.split(':')
        ranges = list(map(lambda x: x.strip(), line[1].split(' or ')))

        key = line[0]

        rules[key] = list(
            map(lambda x: list(map(int, x.split('-'))), ranges))

        currLine += 1

    currLine += 2
    my_ticket = list(map(int, data[currLine].split(',')))

    currLine += 3
    while currLine < len(data) and len(data[currLine]) != 0:
        nearby_tickets.append(list(map(int, data[currLine].split(','))))
        currLine += 1
    # print(rules)
    # print(my_ticket)
    # print(nearby_tickets)

    valid_tck = []
    for n in nearby_tickets:
        value, f = isValid(n, rules)
        if f:
            valid_tck.append(n)

    # print(valid_tck)
    # print(rules)

    valid_type_col = {}

    for c in range(len(valid_tck[0])):
        col_i = [row[c] for row in valid_tck]
        print(col_i)
        valid_type_col[c] = getValidLocation(col_i, rules)

    print(valid_type_col)

    used = set()

    new_m = {}
    for col, vtc in valid_type_col.items():
        new_m[len(vtc)] = col
    print(new_m)

    my_t_map = {}
    for k in sorted(new_m.keys()):
        col = new_m[k]
        class_ = valid_type_col[col]
        print(class_, k, col)

        my_t_map[col] = list(class_.symmetric_difference(used))[0]

        used = used.union(class_)
        print(class_, used)

    print(my_t_map)

    filtered_cols = list(
        filter(lambda x: 'departure' in x[1], my_t_map.items()))

    res = 1
    for col, _ in filtered_cols:
        print(my_ticket[col])
        res *= my_ticket[col]

    return res


def main():
    print("Day 16 - Part 1")
    print(day16p1())

    print("Day 16 - Part 2")
    print(day16p2())


main()

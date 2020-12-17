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


def getRules(currLine, data):
    rules = {}
    while currLine < len(data) and len(data[currLine]) != 0:
        line = data[currLine]
        line = line.split(':')
        ranges = list(map(lambda x: x.strip(), line[1].split(' or ')))

        key = line[0]

        rules[key] = list(
            map(lambda x: list(map(int, x.split('-'))), ranges))

        currLine += 1
    return rules, currLine


def parseTickets(currLine, data):
    nearby_tickets = []
    while currLine < len(data) and len(data[currLine]) != 0:
        nearby_tickets.append(list(map(int, data[currLine].split(','))))
        currLine += 1
    return nearby_tickets, currLine


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

    rules, currLine = getRules(0, data)
    currLine += 2
    currLine += 3
    nearby_tickets, currLine = parseTickets(currLine, data)

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


def getValidLocations(tckt_col_i, rules):
    valid_locations = set(rules.keys())
    for f in tckt_col_i:
        vt = set()
        for k, rs in rules.items():
            for r in rs:
                if r[0] <= f <= r[1]:
                    vt.add(k)
        valid_locations.intersection_update(vt)

    return valid_locations


def day16p2():
    data = get_input(parse2, test=False)

    # Get Rules
    rules, currLine = getRules(0, data)
    # Get My Ticket
    currLine += 2
    my_ticket = list(map(int, data[currLine].split(',')))
    # Get Nearby Ticket
    currLine += 3
    nearby_tickets, currLine = parseTickets(currLine, data)

    # print(rules)
    # print(my_ticket)
    # print(nearby_tickets)

    valid_tckt = []
    for n in nearby_tickets:
        _, flg = isValid(n, rules)
        if flg:
            valid_tckt.append(n)

    # print(valid_tckt)
    # print(rules)

    # Get the valid labels for columns
    valid_type_col = {}
    for c in range(len(valid_tckt[0])):
        # Get all the values of column c
        col_i = [row[c] for row in valid_tckt]

        # There exists valid ranges for Rule r
        # find Rules that satisfiy values in col_i
        # col_i: [] get all tha valid labels for given column values
        # set() of valid labels
        valid_type_col[c] = getValidLocations(col_i, rules)

    # used labels
    used = set()

    # new map of len(Labels): ColNumber
    lbl_len_to_col = {}
    for col, vtc in valid_type_col.items():
        lbl_len_to_col[len(vtc)] = col

    # Find the remaining labels for the Col
    # start by the col with only 1 option
    my_tckt_map = {}

    # instead of sorting the keys with O(n*log(n))
    # to have the columns sorted in least labels (1 to n)
    # Find the max and iterate through 1 -> MaxKey, Time Complexity O(n)
    #
    max_key = max(lbl_len_to_col.keys())

    for k in range(1, max_key + 1):
        # ignore if amount of labels does not exist
        if k not in lbl_len_to_col:
            continue

        col = lbl_len_to_col[k]
        labels = valid_type_col[col]

        # if label has not been used, then it will appear only on Labels
        # get the symetric diff
        my_tckt_map[col] = list(labels.symmetric_difference(used))[0]

        # add labels to used
        used.update(labels)

    # filter the columns by those that contain 'departure'
    filtered_cols = list(
        filter(lambda x: 'departure' in x[1], my_tckt_map.items()))

    # get the multiplication of the Values on the Labels
    res = 1
    for col, _ in filtered_cols:
        res *= my_ticket[col]

    return res


def main():
    print("Day 16 - Part 1")
    print(day16p1())

    print("Day 16 - Part 2")
    print(day16p2())


main()

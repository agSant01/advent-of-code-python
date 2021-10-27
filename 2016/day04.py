from functools import reduce
import itertools
import collections


def get_filename(test=False):
    return f'day04_input{"_test" if test else ""}.txt'


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
    idx = line.index('[')
    checksum = line[idx+1:-1]
    sector_id = line[idx-3:idx]
    letters = line[:idx-4]
    return (letters,  int(sector_id), checksum)

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def increment(map, key):
    map[key] += 1
    return map


"""
Invert char.
a -> z; z -> a; b -> y;
"""
def invert(x: str): return chr(122-ord(x))


def get_letter_count(string):
    return reduce(
        increment,   # m[key] += 1
        string.replace('-', ''),
        collections.defaultdict(int)
    )


def get_top_n(letter_count: dict, n: int):
    return sorted(
        letter_count.items(),
        key=lambda item: str(item[1]) + invert(item[0]),
        reverse=True
    )[:n]


def join(iterable, sep=''): return sep.join(iterable)


def get_items_at(iterable, n): return map(lambda x: x[n], iterable)


def is_valid_room_func(room: list):
    return join(
        get_items_at(
            get_top_n(
                get_letter_count(room[0]),
                5),
            0)) == room[2]


def is_valid_room_imp(room: list):
    letter_count = collections.defaultdict(int)
    room_cypher, _, checksum = room

    for letter in room_cypher.replace('-', ''):
        letter_count[letter] += 1

    top_5 = list(letter_count.items())

    # sort by descending count and ascending char
    top_5.sort(
        # str(int) + inverted(char)
        key=lambda tuple: str(tuple[1]) + invert(tuple[0]),
        reverse=True
    )

    proposed_checksum = ''
    for tuple in top_5:
        proposed_checksum += tuple[0]

    return proposed_checksum == checksum


print('aaaaa-bbb-z-y-x-123[abxyz]',
      is_valid_room_imp(['aaaaa-bbb-z-y-x', 123, 'abxyz']))


################################################################################

def day04p1():
    data = get_input(parse1, test=False)

    total_sum = 0
    for room_data in data:
        total_sum += room_data[1] if is_valid_room_func(room_data) else 0

    return 'Sum', total_sum

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def decrypt(room_data: list):
    enc_name, sector_id, _ = room_data
    def inc_char(char, increment): return chr(
        ((ord(char) - 97 + increment) % 26) + 97)

    def decrypt(let): return inc_char(let, sector_id) if let != '-' else ' '
    return join(map(decrypt, enc_name))


################################################################################


def day04p2():
    rooms = get_input(parse2, test=False)

    tmp = []
    for room_data in rooms:
        if not is_valid_room_func(room_data):
            continue
        decripted_name = decrypt(room_data)
        if 'object' in decripted_name:
            tmp.append((decripted_name, room_data[1]))

    return tmp


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 04 - Part 1", '-'*n)
    print('Result =>', day04p1())
    print()
    print('-'*(n), "Day 04 - Part 2", '-'*n)
    print('Result =>', day04p2())
    print()


main()

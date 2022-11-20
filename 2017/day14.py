import sys


def get_filename(test=False):
    return f'day14_input{"_test" if test else ""}.txt'


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


def twist_hash_string(hash_string, lengths, skip_size=0, current_pos=0):
    internal_hash_string = hash_string.copy()
    hash_len = len(hash_string)
    # print('hash_string:', internal_hash_string)
    # print('lengths:', lengths)

    for length in lengths:
        if length > 1:
            end_pos = ((current_pos+length) % hash_len)-1
            iters_ = abs(length)//2
            # pretty_print(internal_hash_string, current_pos, length)
            # print(f'iters {iters_} | end: {end_pos}')
            start_ptr = current_pos % hash_len
            # print('start:', start_ptr)
            for _ in range(iters_):
                temp = internal_hash_string[start_ptr]
                internal_hash_string[start_ptr] = internal_hash_string[end_pos]
                internal_hash_string[end_pos] = temp
                end_pos -= 1
                start_ptr = (start_ptr + 1) % hash_len

        current_pos = (current_pos+skip_size+length) % hash_len
        skip_size += 1

    return internal_hash_string, current_pos % hash_len, skip_size


def knot_hash(lengths, hash_len=256, rounds=1):
    internal_lengths = []
    for char in lengths:
        internal_lengths.append(ord(char))
    internal_lengths += [17, 31, 73, 47, 23]
    rounds = 64
    sparse_hash = [i for i in range(hash_len)]
    curr_pos = 0
    skip_size = 0
    for _ in range(rounds):
        sparse_hash, curr_pos, skip_size = twist_hash_string(
            sparse_hash, internal_lengths, skip_size=skip_size, current_pos=curr_pos)
    dense_hash = []
    for i in range(16):
        blk_start = i * 16
        acc = sparse_hash[blk_start]
        for i in range(15):
            acc ^= sparse_hash[blk_start+i+1]
        dense_hash.append(acc)

    dense_hashes = ''.join([hex(value)[2:].zfill(2) for value in dense_hash])

    return dense_hashes


################################################################################


def day14p1():
    data = get_input(parse1, test=False)[0]
    ones = 0
    for row in range(128):
        row_hash = f'{data}-{row}'
        hash_ = knot_hash(row_hash)
        bits = ''
        for h in hash_:
            bits += bin(int(h, 16))[2:].zfill(4)
        for k in bits:
            ones += int(k)

    return ones

# 3ecaf0d2646e9dc1483e752d52688a1e
################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def print_groups(group_dict, r=128, c=128):
    for ridx in range(r):
        for cidx in range(c):
            print(f'{group_dict.get((ridx, cidx), ".")}\t', end='')
        print()


def get_neighbors(r, c):
    n = []
    if r > 0:
        n.append((r-1, c))
    if r < 127:
        n.append((r+1, c))
    if c > 0:
        n.append((r, c-1))
    if c < 127:
        n.append((r, c+1))
    return n

################################################################################


def day14p2():
    data = get_input(parse2, test=False)[0]
    ones = 0
    bit_map = []
    for row in range(128):
        row_hash = f'{data}-{row}'
        hash_ = knot_hash(row_hash)
        bits = ''
        for h in hash_:
            converted = bin(int(h, 16))[2:].zfill(4)
            bits += converted
        for k in bits:
            ones += int(k)
        bit_map.append(bits)

    groups = 1
    group_dict = {}
    for ext_r in range(128):
        for ext_c in range(128):
            if bit_map[ext_r][ext_c] == '0':
                continue

            to_visit = [(ext_r, ext_c)]
            visited = set()
            while len(to_visit) > 0:
                r, c = to_visit.pop()
                if bit_map[r][c] == '0':
                    continue

                if (r, c) in visited:
                    continue

                visited.add((r, c))
                if (r, c) not in group_dict:
                    group_dict[(r, c)] = groups
                    groups += 1

                for n_r, n_c in get_neighbors(r, c):
                    if bit_map[n_r][n_c] == '1':
                        to_visit.append((n_r, n_c))
                        group_dict[(n_r, n_c)] = group_dict[(r, c)]

    return ones,  max(group_dict.values())


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print('-'*(n), "Day 14 - Part 1", '-'*n)
        print('Result =>', day14p1())
        print()
    if run_two:
        print('-'*(n), "Day 14 - Part 2", '-'*n)
        print('Result =>', day14p2())
    print()


main()

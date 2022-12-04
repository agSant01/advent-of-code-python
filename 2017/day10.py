import sys


def get_filename(test=False):
    return f'day10_input{"_test" if test else ""}.txt'


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


def parse1(line: str):
    return list(map(int, line.split(",")))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def pretty_print(hash_list, curr, sub_list_length):
    end_pos = ((curr + sub_list_length) % len(hash_list)) - 1
    to_print = []
    for idx, hc in enumerate(hash_list):
        if idx == curr:
            to_print.append(" ([" + str(hc) + "]")
        else:
            to_print.append(" " + str(hc))
        if idx == end_pos:
            to_print.append(")")
    print(
        "Repr:",
        "".join(map(str, to_print))[1:],
        f"\t| Curr:{ curr} | Length: {sub_list_length}",
    )


def twist_hash_string(hash_string, lengths, skip_size=0, current_pos=0):
    internal_hash_string = hash_string.copy()
    hash_len = len(hash_string)
    # print('hash_string:', internal_hash_string)
    # print('lengths:', lengths)

    for length in lengths:
        if length > 1:
            end_pos = ((current_pos + length) % hash_len) - 1
            iters_ = abs(length) // 2
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

        current_pos = (current_pos + skip_size + length) % hash_len
        skip_size += 1

    return internal_hash_string, current_pos % hash_len, skip_size


################################################################################


def day10p1():
    test = False
    lengths = get_input(parse1, test)[0]

    is_debug_print = False
    if is_debug_print:
        pretty_print([0, 1, 2, 3, 4], 0, 3)
        pretty_print([0, 1, 2, 3, 4], 3, 4)
        pretty_print([0, 1, 2, 3, 4], (5 + 3) % 5, 1)
        exit(0)

    hash_len = 5 if test else 256
    hash_string = [i for i in range(hash_len)]
    twisted_hash_string, _, _ = twist_hash_string(hash_string, lengths)

    return twisted_hash_string[0] * twisted_hash_string[1]


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line: str):
    result_arr = []
    for char in line:
        result_arr.append(ord(char))
    return result_arr


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day10p2():
    test = False
    lengths = get_input(parse2, test)
    rounds = 64
    dense_hashes = []
    hash_len = 256
    for l in lengths:
        sparse_hash = [i for i in range(hash_len)]
        curr_pos = 0
        skip_size = 0
        l += [17, 31, 73, 47, 23]
        for _ in range(rounds):
            sparse_hash, curr_pos, skip_size = twist_hash_string(
                sparse_hash, l, skip_size=skip_size, current_pos=curr_pos
            )

        dense_hash = []
        for i in range(16):
            blk_start = i * 16
            acc = sparse_hash[blk_start]
            for i in range(15):
                acc ^= sparse_hash[blk_start + i + 1]
            dense_hash.append(acc)

        # print(dense_hash)
        dense_hashes += ["".join([hex(value)[2:].zfill(2) for value in dense_hash])]

    return dense_hashes[0]


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print("-" * (n), "Day 10 - Part 1", "-" * n)
        print("Result =>", day10p1())
        print()
    if run_two:
        print("-" * (n), "Day 10 - Part 2", "-" * n)
        print("Result =>", day10p2())
    print()


main()

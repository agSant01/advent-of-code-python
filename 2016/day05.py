import random
import hashlib
import crypt


def get_filename(test=False):
    return f'day05_input{"_test" if test else ""}.txt'


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


################################################################################
def day05p1():
    is_test = False

    door_id = 'abc'
    if not is_test:
        door_id = 'ffykfhsq'

    index = 0
    pwd = ''
    while len(pwd) < 8:
        text = hashlib.md5(str(door_id + str(index)).encode())
        if text.hexdigest()[:5] == '00000':
            pwd += text.hexdigest()[5]
        index += 1

    return pwd

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day05p2():
    is_test = False

    door_id = 'abc'
    if not is_test:
        door_id = 'ffykfhsq'

    index = 0
    pwd = [None for _ in range(8)]
    print('Hacking Animation:')
    while None in pwd:
        text = hashlib.md5(str(door_id + str(index)).encode())
        text = text.hexdigest()

        index += 1

        pos = int(text[5], 16)

        if text[:5] == '00000' and 0 <= pos < 8 and pwd[pos] == None:
            pwd[pos] = text[6]

        if index % 100_000 == 0:
            tmp = ''.join([i if i != None else chr(
                random.randint(97, 122)) for i in pwd])
            print(tmp, end='\r')

    return ''.join(pwd)


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 05 - Part 1", '-'*n)
    print('Result =>', day05p1())
    print()
    print('-'*(n), "Day 05 - Part 2", '-'*n)
    print('Result =>', day05p2())
    print()


main()

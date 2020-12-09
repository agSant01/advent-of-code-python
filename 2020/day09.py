import utils as ut


def get_filename(test=False):
    return f'day09_input{"_test" if test else ""}.txt'


def parse(line):
    return int(line)


def find(sum_, numbers):
    for i in range(len(numbers)):
        if (sum_ - int(numbers[i])) in numbers:
            return True, (sum_ - int(numbers[i]), int(numbers[i]))
    return False


def day09p1():
    data = ut.get_input(get_filename(test=False), parse)

    preamble = 25

    valid_numbers = []

    cur = 0

    while cur < preamble:
        valid_numbers.append(data[cur])
        cur += 1

    while cur < len(data):
        res = find(data[cur], valid_numbers[(cur-preamble):cur])
        if not res:
            return data[cur]

        valid_numbers.append(data[cur])
        cur += 1


def findInvalidNum(data, preamble=25):
    valid_numbers = []

    cur = 0

    while cur < preamble:
        valid_numbers.append(data[cur])
        cur += 1

    while cur < len(data):
        res = find(data[cur], valid_numbers[(cur-preamble):cur])
        if not res:
            return data[cur]

        valid_numbers.append(data[cur])
        cur += 1


def contSumRec(numToSum, data, window):
    curr = 0
    sum_ = sum(data[0:window])

    while curr < len(data) - window-1:
        sum_ -= data[curr]
        sum_ += data[curr+window]
        curr += 1
        if sum_ == numToSum:
            return data[curr:(curr+window)]

    return contSumRec(numToSum, data, window-1)


def contSum(numToSum, data):
    return contSumRec(numToSum, data, len(data)-1)


def day09p2():
    data = ut.get_input(get_filename(test=False), parse)

    invalid_num = findInvalidNum(data)
    seq = contSum(invalid_num, data)
    return min(seq)+max(seq)


def main():
    print("Day 09 - Part 1")
    print(day09p1())

    print("Day 09 - Part 2")
    print(day09p2())


main()

def get_filename(test=False):
    return f"day08_input{'_test' if test else ''}.txt"


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


def parse1(line):
    data = line.split(" | ")
    return [data[0].split(), data[1].split()]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


################################################################################
def day08p1():
    data = get_input(parse1, test=False)

    s7 = [2, 4, 3, 7]
    c = 0
    for d in data:
        for i in d[1]:
            if len(i) in s7:
                c += 1

    return c


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################

################################################################################


def day08p2():
    data = get_input(parse2, test=False)

    total = 0
    for line in data:
        mapping_ = {}
        signals, finals = line

        signals = sorted(signals, key=len)
        for signal in signals:
            signal = set(signal)

            if len(signal) == 2:
                mapping_[1] = signal
            elif len(signal) == 3:
                mapping_[7] = signal
            elif len(signal) == 4:
                mapping_[4] = signal
            elif len(signal) == 7:
                mapping_[8] = signal

        # interpret result
        res = ""
        for digit in finals:
            digit = set(digit)
            if len(digit) == 2:
                res += "1"
            elif len(digit) == 3:
                res += "7"
            elif len(digit) == 4:
                res += "4"
            elif len(digit) == 7:
                res += "8"
            elif len(digit) == 5:
                if len(digit.intersection(mapping_[1])) == 2:
                    res += "3"
                elif len(digit.intersection(mapping_[4])) == 3:
                    res += "5"
                else:
                    res += "2"
            elif len(digit) == 6:
                if len(digit.intersection(mapping_[1])) == 1:
                    res += "6"
                elif len(digit.intersection(mapping_[4])) == 4:
                    res += "9"
                else:
                    res += "0"

        total += int(res)
    return total


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 08 - Part 1", "-" * n)
    print("Result =>", day08p1())
    print()
    print("-" * (n), "Day 08 - Part 2", "-" * n)
    print("Result =>", day08p2())
    print()


main()

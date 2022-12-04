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


def parse1(line):
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def look_and_say(s: str):
    result = ""

    prev = s[0]
    count = 0
    for char in s:
        if char == prev:
            count += 1
        else:
            result += f"{count}{prev}"
            count = 1
            prev = char

    if count > 0:
        result += f"{count}{char}"

    return result


################################################################################
def day10p1():
    is_test = False
    data = get_input(parse1, test=is_test)

    if is_test:
        for d in data:
            print("Input,", d)
            print("res,", look_and_say(d))
    else:
        results = []
        for d in data:
            original = d
            print("Org:", original)
            for _ in range(40):
                original = look_and_say(original)

            results.append(len(original))

        return results


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
    is_test = False
    data = get_input(parse1, test=is_test)

    if is_test:
        for d in data:
            print("Input,", d)
            print("res,", look_and_say(d))
    else:
        results = []
        for d in data:
            original = d
            print("Org:", original)
            for _ in range(50):
                original = look_and_say(original)

            results.append((d, "original", len(original)))
        return results


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 10 - Part 1", "-" * n)
    print("Result =>", day10p1())
    print()
    print("-" * (n), "Day 10 - Part 2", "-" * n)
    print("Result =>", day10p2())
    print()


main()

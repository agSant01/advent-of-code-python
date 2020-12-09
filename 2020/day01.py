def parse(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(int(line.strip()))
    return lines


def find(sum_, numbers):
    subs = []
    for i in range(len(numbers)):
        if (sum_ - int(numbers[i])) in numbers:
            return int(numbers[i]) * (sum_ - int(numbers[i]))


def main():
    numbers = parse('day01_input.txt')

    for i in range(len(numbers)):
        val = numbers[i]
        res = find(2020 - val, numbers)
        if res:
            print(val, res)
            print(res * val)


main()

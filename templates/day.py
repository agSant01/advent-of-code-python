def lines(day):
    opt_filename = '{"_test" if test else ""}'
    return [
        'def get_filename(test=False):',
        f'    return f\'day{day}_input{opt_filename}.txt\'',
        '',
        'def get_input(parse, test=False):',
        '    data = []',
        '    filename = get_filename(test)',
        '    with open(filename, \'r\') as file:',
        '        for line in file:',
        '            data.append(parse(line.strip()))',
        '    return data',
        '',
        'def parse1(line):',
        '    return line',
        '',
        f'def day{day}p1():',
        '    data = get_input(parse1, test=True)',
        '    for d in data:',
        '        print(d)',
        '',
        'def parse2(line):',
        '    return parse1(line)',
        '',
        f'def day{day}p2():',
        '    data = get_input(parse2, test=True)',
        '    for d in data:',
        '        pass',
        '',
        'def main():',
        f'    print("Day {day} - Part 1")',
        f'    print(day{day}p1())',
        '',
        f'    print("Day {day} - Part 2")',
        f'    print(day{day}p2())',
        '',
        'main()',
    ]

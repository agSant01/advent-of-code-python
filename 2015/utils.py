from os import path


def get_input(filename, parse):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def init_day(day):
    _create_py_file(day)
    _create_test_data(day)


def _create_test_data(day):
    day = str(day).zfill(2)

    input_f = f"day{day}_input.txt"
    if path.exists(input_f):
        print(f'File: {input_f} already exists!!!')
        exit(1)

    with open(input_f, 'w') as f:
        f.write('')

    input_ft = f"day{day}_input_test.txt"
    if path.exists(input_ft):
        print(f'File: {input_ft} already exists!!!')
        exit(1)

    with open(input_ft, 'w') as f:
        f.write('')


def _create_py_file(day: str):
    day = str(day).zfill(2)
    py_filename = f"day{day}.py"

    if path.exists(py_filename):
        print(f'File: {py_filename} already exists!!!')
        exit(1)

    opt_filename = '{"_test" if test else ""}'

    lines = [
        'import utils as ut',
        '',
        'def get_filename(test=False):',
        f'   return f\'day{day}_input{opt_filename}.txt\'',
        '',
        'def parse1(line):',
        '    return line',
        '',
        f'def day{day}p1():',
        '   data = ut.get_input(get_filename(test=True), parse1)',
        '   for d in data:',
        '       print(d)',
        '',
        'def parse2(line):',
        '    return parse1(line)',
        '',
        f'def day{day}p2():',
        '   data = ut.get_input(get_filename(test=True), parse2)',
        '   for d in data:',
        '       pass',
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
    with open(py_filename, 'w') as f:
        for l in lines:
            f.write(l + '\n')

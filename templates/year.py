def lines():
    return [
        'def get_input(filename, parse):',
        '    data = []',
        '    with open(filename, \'r\') as file:',
        '        for line in file:',
        '            data.append(parse(line.strip()))',
        '    return data'
    ]

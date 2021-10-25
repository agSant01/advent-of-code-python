import requests
import datetime
import argparse
from datetime import datetime
import os

from templates \
    import \
    day as dayutils, \
    year as yearutils


def console(msg):
    print(f'==>', msg)


def config():
    cfg = {}
    with open('.env') as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            c = line.strip().split('=', 1)
            cfg[c[0]] = c[1]
    return cfg


CONFIG = {}
BASE_URL = 'https://adventofcode.com'


def init_year(year: int = None):
    if not year:
        year = datetime.today().year

    year_file_name = f'yearutils.py'

    fp = os.path.join(str(year), year_file_name)

    console(f'Initializing year directory: ./{year}')

    if os.path.isdir(str(year)):
        console(f'[ERROR] Directory: ./{year} already exists!!!')
        exit(1)
    else:
        os.makedirs(str(year))

    console(f'Creating dependency: ./{fp}')
    with open(fp, 'w') as f:
        for l in yearutils.lines():
            f.write(l + '\n')


def create_input_files(day, data, year=None, force=False):
    day = str(day).zfill(2)
    if not year:
        year = datetime.today().year

    console('Creating Input files')

    input_f = os.path.join(str(year), f"day{day}_input.txt")
    if os.path.exists(input_f) and not force:
        console(f'File: {input_f} already exists!!!')
        exit(1)

    console(f'Creating Input file: {input_f}')
    with open(input_f, 'w') as f:
        f.write(data)

    input_ft = os.path.join(str(year), f"day{day}_input_test.txt")
    if os.path.exists(input_ft) and not force:
        console(f'File: {input_ft} already exists!!!')
        exit(1)

    console(f'Creating Input file: {input_ft}')
    with open(input_ft, 'w') as f:
        f.write('')


def get_input_data(day, year=None, force=False):
    day = int(day)
    if not year:
        year = datetime.today().year
    console(f'Get input data for year:{year} \u272D day:{day}')

    complete_url = f'{BASE_URL}/{year}/day/{day}/input'

    console(f'GET at {complete_url}')

    headers = dict(cookie=CONFIG['SESSION_COOKIE'])
    data = requests.get(complete_url, headers=headers)

    if data.status_code == 200:
        console(f'Success:  {data.status_code}')
    else:
        console(f'Error:  {data.status_code}')
        console(f'Response Content: {data.content}')
        exit(1)

    create_input_files(day, data.content.decode(), year, force)


def create_day(day: str, year: str = None):

    day = str(day).zfill(2)
    if not year:
        year = datetime.today().year

    py_filename = os.path.join(str(year), f"day{day}.py")

    console(f'Creating day template: ./{py_filename}')

    if os.path.exists(py_filename):
        console(f'File: {py_filename} already exists!!!')
        exit(1)

    with open(py_filename, 'w') as f:
        for l in dayutils.lines(day):
            f.write(l + '\n')

    get_input_data(day, year)


def run(day, year=None):
    day = str(day).zfill(2)
    if not year:
        year = datetime.today().year

    console(f'Running script: ./{year}/day{day}.py')

    os.chdir(f'./{year}')
    os.system(f'python3 ./day{day}.py')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--create-day', '-cd',
                        type=int, required=False)
    parser.add_argument('--input-data', '-i',
                        type=int, required=False)

    parser.add_argument('--run', '-r',
                        type=int, required=False)

    parser.add_argument('--year', '-y',
                        type=int, default=None, required=False)
    parser.add_argument('--init-year', '-iy',
                        type=int, nargs='?', default=False, required=False)

    parser.add_argument('--force', '-f', action='store_true',
                        default=False, required=False)

    args = parser.parse_args()
    # Debug
    # console(args)

    if bool(args.run):
        run(args.run, args.year)
        exit()

    if args.init_year is None or bool(args.init_year):
        init_year(args.init_year)

    if args.create_day:
        create_day(args.create_day, args.year)
    elif args.input_data:
        get_input_data(args.input_data, args.year, args.force)


if __name__ == "__main__":
    CONFIG = config()
    main()

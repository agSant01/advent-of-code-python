import argparse
import datetime
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Union

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify  # type:ignore

from templates import day as day_template

BASE_URL = "https://adventofcode.com"
PREV_VERSIONS = [1]
VERSION = 2


def __init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--create-day", "-cd", type=int, required=False)
    parser.add_argument("--input-data", "-i", type=int, required=False)
    parser.add_argument(
        "--day-desc",
        "-dd",
        type=int,
        default=None,
        required=False,
        help=(
            "Day description. Download the instructions of the day at AOC as"
            " Markdown.Will only be able to download unlocked instructions. Would not"
            ' download "Part 2" if "Part 1" is not completed.'
        ),
    )

    parser.add_argument("--run", "-r", type=int, required=False)

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.today().year,  # type:ignore
        required=False,
    )
    parser.add_argument(
        "--init-year", "-iy", type=int, nargs="?", default=False, required=False
    )

    parser.add_argument(
        "--force", "-f", action="store_true", default=False, required=False
    )

    parser.add_argument(
        "--comp",
        type=int,
        choices=PREV_VERSIONS + [VERSION],
        help=(
            "Run in compatibility mode.\nAvailable versions:"
            f' {", ".join(map(str, PREV_VERSIONS + [VERSION]))}'
        ),
        required=False,
        default=VERSION,
    )

    return parser.parse_known_args()[0]


ARGS = __init_args()


def __config():
    cfg: Dict[str, str] = {}
    with open(".env") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if len(line.strip()) == 0:
                continue
            c = line.strip().split("=", 1)
            cfg[c[0]] = c[1]
    return cfg


CONFIG = __config()


def console(msg: Any):
    print(f"==>", msg)


def error(msg: Any):
    print(f"[ERROR]", msg)


def init_year(year: int = None):  # type:ignore
    if not year:
        year: int = datetime.today().year  # type:ignore

    console(f"Initializing year directory: ./{year}")

    if os.path.isdir(str(year)):
        console(f"[ERROR] Directory: ./{year} already exists!")
        exit(1)
    else:
        os.makedirs(str(year))


def create_instruction_file(day_str: str, year: int = None):  # type:ignore
    day = str(day_str).zfill(2)
    if not year:
        year: int = datetime.today().year  # type:ignore

    file_path = Path(str(year), f"day{day}", "instructions.md")
    console(f"Downloading instructions file: {file_path}")
    complete_url = f"{BASE_URL}/{year}/day/{int(day)}"
    console(f"GET at {complete_url}")
    headers = dict(cookie=f"session={CONFIG['SESSION_COOKIE']}")
    data = requests.get(complete_url, headers=headers)
    if data.status_code == 200:
        console(f"Success:  {data.status_code}")
    else:
        console(f"Error:  {data.status_code}")
        console(f"Response Content: {data.content}")
        exit(1)

    soup = BeautifulSoup(data.content.decode(), "html.parser")

    tags = soup.find_all("article", class_=re.compile("day-desc"))

    def remove_dash(tag: Any):
        str_ = tag.h2.string.replace("---", "").strip()
        tag.h2.string.replace_with(str_)
        return str(tag)

    markdown = markdownify(  # type:ignore
        "".join(map(remove_dash, tags)), heading_style="ATX"  # type:ignore
    )

    with open(file_path, "w") as f:
        f.write(markdown)  # type:ignore

    console("Created instructions MD file...")


def create_input_files(day: str, year: int = None, force: bool = False):  # type:ignore
    day = str(day).zfill(2)
    if not year:
        year: int = datetime.today().year  # type:ignore

    console("Creating Input files...")

    input_test_file: Path = Path(str(year), f"day{day}", "input_test.txt")
    if input_test_file.exists() and not force:
        console(f"File: {input_test_file} already exists!")
    else:
        console(f"Creating Input file: {input_test_file}")
        input_test_file.touch()

    input_file: Path = Path(str(year), f"day{day}", "input.txt")
    if input_file.exists() and not force:
        console(f"File: {input_file} already exists!")
    else:
        data = get_input_data(day, year)
        if not data:
            exit(1)

        console(f"Creating Input file: {input_file}")
        with open(input_file, "w") as f:
            f.write(data)


def get_input_data(day_str: str, year: int = None) -> Union[str, None]:  # type:ignore
    day = int(day_str)
    if not year:
        year: int = datetime.today().year  # type:ignore

    console(f"Get input data for year: {year} \u272D day:{day}")

    complete_url = f"{BASE_URL}/{year}/day/{day}/input"

    console(f"GET at {complete_url}")

    headers = dict(cookie=f"session={CONFIG['SESSION_COOKIE']}")
    data = requests.get(complete_url, headers=headers)

    if data.status_code == 200:
        console(f"Success:  {data.status_code}")
    else:
        console(f"Error:  {data.status_code}")
        console(f"Response Content: {data.content}")
        return None

    return data.content.decode()


def create_day(day: str, year: int = None):  # type: ignore
    day = str(day).zfill(2)
    if not year:
        year: int = datetime.today().year  # type: ignore

    daycode_filepath: Path = Path(str(year), f"day{day}")

    console(f"Creating day template: ./{daycode_filepath}")

    if daycode_filepath.exists():
        console(f"File: {daycode_filepath} already exists!")
        exit(1)

    daycode_filepath.mkdir()

    file_name = daycode_filepath / f"day{day}_code.py"
    with open(file_name, "w") as f:
        f.write(day_template.lines(day))

    create_input_files(day, year)
    create_instruction_file(day, year)


def run(day: str, year: int = None):  # type: ignore
    if not year:
        year: int = datetime.today().year  # type: ignore
    day = str(day).zfill(2)
    if ARGS.comp < 2:
        console(f"Running script: ./{year}/day{day}.py")
        os.chdir(f"./{year}")
        os.system(f"python3.8 ./day{day}.py {' '.join(sys.argv[1:])}")
    else:
        try:
            console(f"Running script: ./{year}/day{day}/day{day}_code.py")
            fp = Path(str(year), f"day{day}", f"day{day}_code.py")
            if not fp.exists():
                error("FileNotFoundError: Try using compatibility mode --comp")
            else:
                os.system(f"python3.8 {fp.absolute()} {' '.join(sys.argv[1:])}")
        except FileNotFoundError:
            error("FileNotFoundError: Try using compatibility mode --comp")


def main():
    # Debug
    # console(args)

    if bool(ARGS.run):
        run(ARGS.run, ARGS.year)
        exit()

    if ARGS.init_year is None or bool(ARGS.init_year):
        init_year(ARGS.init_year)

    if ARGS.create_day:
        create_day(ARGS.create_day, ARGS.year)
    elif ARGS.input_data:
        create_input_files(ARGS.input_data, ARGS.year, ARGS.force)
    elif ARGS.day_desc:
        create_instruction_file(ARGS.day_desc, ARGS.year)


if __name__ == "__main__":
    main()

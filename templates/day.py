from pathlib import Path
from string import Template


def lines(day: str) -> str:
    data = {"opt_filename": '{"_test" if test else ""}', "day": day}
    with open(Path(__file__).parent / "code.txt", "r") as file:
        code_lines = Template(file.read())
        return code_lines.substitute(data)

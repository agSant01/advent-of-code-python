import argparse
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Set, TypeVar, Union

###########################################################################
############################### Setup #####################################
###########################################################################

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "--input", "-i", help="Input file path.", type=Path, required=False
)
arg_parser.add_argument(
    "--part",
    "-p",
    type=int,
    default=(1, 2),
    choices=(1, 2),
    nargs=1,
    help="Run part 1 or 2",
    required=False,
)
arg_parser.add_argument(
    "--puzzle",
    "-a",
    help="Use real puzzle data.",
    default=False,
    action="store_true",
    required=False,
)
arg_parser.add_argument(
    "--debug",
    help="Debug mode.",
    default=False,
    action="store_true",
    required=False,
)
args, _ = arg_parser.parse_known_args(sys.argv)

args, _ = arg_parser.parse_known_args(sys.argv)

ParsedInput = TypeVar("ParsedInput")


def get_input(
    parse: Callable[[str], ParsedInput], puzzle: bool = False
) -> List[ParsedInput]:
    data: List[ParsedInput] = []
    if args.input:
        filename = Path(args.input)
    else:
        filename: Path = (
            Path(__file__).parents[0] / f'input{"" if puzzle else "_test"}.txt'
        )
        if not filename.exists():
            print(f"[Warning] {filename.absolute()} does not exists.")
            print(
                f"[Info] Defaulting to {filename.parents[0] / 'input_test.txt'} for"
                " input."
            )
            print("-" * 42)
            filename = Path(__file__).parents[0] / "input_test.txt"

    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


def debug_print(*s: Any):
    if args.debug:
        print(*s)


###########################################################################

################################################################################
############################### Start of Part 1 ################################
################################################################################
def parse1(line: str):
    return line.split()


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f"File(name={self.name} size={self.size})"


class Folder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.files: Set[File] = set()
        self.folders: Dict[str, Folder] = {}
        self.parent: Union[Folder, None] = None

    def add_folder(self, folder: Any):
        self.folders[folder.name] = folder

    def size(self) -> int:
        return sum(file.size for file in self.files) + sum(
            folder.size() for folder in self.folders.values()
        )

    def __repr__(self) -> str:
        return (
            f"Folder(name={self.name} files={self.files} folders={self.folders} parent={self.parent})"
        )


def parse_files(cmds: List[List[str]], i: int, folder: Union[Folder, None]):
    if not folder:
        return

    for k in range(i, len(cmds)):
        fs_info = cmds[k]
        if fs_info[0] == "dir":
            new_folder = Folder(fs_info[-1])
            new_folder.parent = folder
            folder.add_folder(new_folder)
        elif fs_info[0] == "$":
            return k
        else:
            folder.files.add(File(fs_info[1], int(fs_info[0])))
    return i


def pretty_print(root: Folder, level: int = 0):
    print(" " * (level), f"-> {root.name} (dir)")
    for folder in root.folders.values():
        pretty_print(folder, level + 1)

    for file in sorted(root.files, key=lambda f: f.name):
        file: File
        print(" " * ((level + 1)), f"- {file.name} (file, size={file.size})")


def traverse_list(cmds: List[List[str]]):
    root = current_folder = Folder("/")
    debug_print("Parsing cmd list...")
    i: int = 1
    while i < len(cmds):
        cmd = cmds[i]
        if cmd[1] == "cd":
            folder_name: str = cmd[2]
            if current_folder is None:
                print("ERROR current_folder is None")
                exit(1)
            elif folder_name == "..":
                current_folder = current_folder.parent
            elif folder_name in current_folder.folders:
                current_folder = current_folder.folders[folder_name]
            else:
                new_folder = Folder(folder_name)
                new_folder.parent = current_folder
                current_folder = new_folder
            debug_print("cd to", current_folder.name)  # type:ignore
        elif cmd[1] == "ls":
            i = parse_files(cmds, i + 1, current_folder) - 1  # type:ignore
        i += 1
    debug_print("End of parsing list...")
    return root


################################################################################
def day07p1():
    data = get_input(parse1, args.puzzle)

    root = traverse_list(data)

    if args.debug:
        pretty_print(root)

    to_visit = [root]
    total_mem = 0

    while len(to_visit) > 0:
        cwd = to_visit.pop(0)

        size = cwd.size()
        if size < 100_000:
            total_mem += size

        for folder in cwd.folders.values():
            to_visit.append(folder)

    return total_mem


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day07p2():
    data = get_input(parse2, args.puzzle)

    root = traverse_list(data)

    total_mem = 70_000_000
    needed_mem = 30_000_000

    available_mem = total_mem - root.size()

    to_visit = [root]

    candidates: List[Folder] = []

    while len(to_visit) > 0:
        cwd = to_visit.pop()

        size = cwd.size()

        if (available_mem + size) >= needed_mem:
            candidates.append(cwd)

        for folder in cwd.folders.values():
            to_visit.append(folder)

    debug_print("\nCandidates:")
    for c in candidates:
        debug_print(c.name, c.size())
    debug_print()

    selected_folder = min(candidates, key=lambda c: c.size())

    return "Folder", selected_folder.name, selected_folder.size()


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 07 - Part 1", "-" * n)
        print("Result =>", day07p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 07 - Part 2", "-" * n)
        print("Result =>", day07p2())
    print()


main()

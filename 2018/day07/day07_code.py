import argparse
import collections
import sys
from pathlib import Path
from typing import Any, Callable, List, TypeVar, Union

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
        filename = Path(__file__).parents[0] / f'input{"" if puzzle else "_test"}.txt'
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
    data = line.split()
    return data[1], data[-3]


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def create_dependency_graphs(data):
    dependency_graph = collections.defaultdict(set)
    preceding_graph = collections.defaultdict(list)

    for depends, step in data:
        dependency_graph[step].add(depends)
        preceding_graph[depends].append(step)

    debug_print(dependency_graph)
    debug_print(preceding_graph)

    return dependency_graph, preceding_graph


################################################################################
def day07p1():
    data = get_input(parse1, args.puzzle)

    dependency_graph, preceding_graph = create_dependency_graphs(data)

    available = []
    for preceding in preceding_graph.keys():
        if preceding not in dependency_graph:
            available.append(preceding)
    available.sort()

    debug_print(available)

    completed_steps = set()
    completed_order = []

    while len(available) > 0:
        step_to_complete = available.pop(0)

        if step_to_complete not in completed_steps:
            completed_steps.add(step_to_complete)
            completed_order.append(step_to_complete)

        for after in preceding_graph[step_to_complete]:
            dependency_graph[after].remove(step_to_complete)
            if len(dependency_graph[after]) == 0:
                available.append(after)

        available.sort()

    return "".join(completed_order)


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


class Worker:
    def __init__(self, wid: int, task_min_cost: int = 0) -> None:
        self.wid = wid
        self.task: Union[None, str] = None
        self.process_time: Union[None, int] = None
        self.time = 0
        self.task_min_cost = task_min_cost

    def is_working(self):
        return self.task != None

    def set_task(self, task: str):
        self.task = task
        self.process_time = (ord(task) - 64) + self.task_min_cost

    def complete_task(self):
        self.task = None
        self.process_time = None
        self.time = 0

    def tick(self):
        if self.task:
            self.time += 1

    def remaining_time(self) -> int:
        if self.process_time:
            return self.process_time - self.time  # type: ignore
        return 0

    def __repr__(self) -> str:
        return (
            "<Worker"
            f" wid={self.wid} task={self.task} process_time={self.process_time} time={self.time} remaining_time={self.remaining_time()}>"
        )


def print_worker_status_header(workers: int):
    wks = [f"Workers #{i+1}" for i in range(workers)]
    print(f'Second         {"     ".join(wks)}      Done')


def print_worker_status(time: int, workers: List[Worker], completed: str):
    print(str(time).zfill(3), end="            ")
    for w in workers:
        if w.task is None:
            print(w.task, end="            ")
        else:
            print(w.task, end="               ")
    print(completed)


E = TypeVar("E")


def sorted_insert(array: List[E], value: E):
    if len(array) == 0:
        array.append(value)
        return

    left = 0
    right = len(array) - 1
    mid = 0

    while left < right:
        mid = (right + left) // 2
        if value < array[mid]:  # type: ignore
            right = mid
        elif value > array[mid]:  # type: ignore
            left = mid + 1
        else:
            break

    if value > array[mid]:  # type: ignore
        mid += 1

    array.insert(mid, value)


################################################################################
def day07p2():
    data = get_input(parse2, args.puzzle)
    dependency_graph, preceding_graph = create_dependency_graphs(data)

    available: List[str] = []
    for preceding in preceding_graph.keys():
        if preceding not in dependency_graph:
            sorted_insert(available, preceding)

    completed_steps = set()
    completed_order = []

    total_workers = 5 if args.puzzle else 2
    task_min_cost = 60 if args.puzzle else 0

    workers = [
        Worker(
            wid=wid + 1,
            task_min_cost=task_min_cost,
        )
        for wid in range(total_workers)
    ]

    debug_print("Non constrained tasks:", available)

    print_worker_status_header(len(workers))

    total_steps = len(set(preceding_graph.keys()).union(dependency_graph.keys()))
    i = 0
    while len(completed_steps) < total_steps:
        for w in workers:
            if w.task and w.remaining_time() == 0:
                # worker finished task
                task: str = w.task
                w.complete_task()

                if task not in completed_steps:
                    completed_steps.add(task)
                    completed_order.append(task)

                for after in preceding_graph[task]:
                    dependency_graph[after].remove(task)
                    if len(dependency_graph[after]) == 0:
                        debug_print(
                            "New available Task:", after, "| Last constrained by:", task
                        )
                        sorted_insert(available, after)

            if not w.task and len(available) > 0:
                w.set_task(available.pop(0))

            debug_print(w)
            w.tick()
        print_worker_status(i, workers, "".join(completed_order))

        i += 1
        debug_print(list(filter(lambda x: len(x[1]) > 0, dependency_graph.items())))
        debug_print(list(filter(lambda x: len(x[1]) == 0, dependency_graph.items())))

    return i - 1


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

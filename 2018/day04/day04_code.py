import argparse
import collections
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence, Set, Union

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
args, _ = arg_parser.parse_known_args(sys.argv)


def get_input(parse: Callable[[str], Any], puzzle: bool = False) -> List[Any]:
    data: List[str] = []
    if args.input:
        filename = Path(args.input)
    else:
        filename = Path(__file__).parent / f'input{"" if puzzle else "_test"}.txt'
        if not filename.exists():
            print(f"[Warning] {filename.absolute()} does not exists.")
            print(
                f"[Info] Defaulting to {filename.parent / 'input_test.txt'} for input."
            )
            print("-" * 42)
            filename = Path(__file__).parent / "input_test.txt"

    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


###########################################################################

################################################################################
############################### Start of Part 1 ################################
################################################################################


class Log(object):
    def __init__(self, data: str) -> None:
        end_of_datetime = data.index("]")
        self.datetime = data[1:end_of_datetime]
        self.msg = data[end_of_datetime + 2 :]

    def is_begin_of_shift(self):
        if "begins shift" in self.msg:
            return True

    def guard_id(self) -> Union[int, None]:
        if self.is_begin_of_shift():
            return int(re.findall(r"\d+", self.msg).pop())
        return None

    def get_time(self) -> str:
        return self.datetime.split()[1]

    def __lt__(self, o: Any) -> bool:
        if not isinstance(o, Log):
            return False

        return self.datetime < o.datetime

    def __str__(self) -> str:
        return f"<Log datetime={self.datetime} msg='{self.msg}'>"


def parse1(line: str):
    return Log(line)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


class TimeRange:
    def __init__(self, start: Union[str, None], end: str) -> None:
        self.start = start
        self.end = end

    def minutes(self) -> int:
        shours, sminutes = self.start.split(":")  # type:ignore
        ehours, eminutes = self.end.split(":")

        thours = int(ehours) - int(shours)

        return (thours * 60) + (int(eminutes) - int(sminutes))

    def minutes_range(self) -> Sequence[int]:
        _, sminutes = self.start.split(":")  # type:ignore
        _, eminutes = self.end.split(":")

        sminutes = int(sminutes)
        eminutes = int(eminutes)

        if sminutes < eminutes:
            return [i for i in range(sminutes, eminutes)]

        return [i for i in range(eminutes)] + [i for i in range(sminutes, 60)]

    def __str__(self) -> str:
        return f"<TimeRange ({self.start}, {self.end})>"

    def __repr__(self) -> str:
        return self.__str__()


class Guard:
    def __init__(self, gid: int) -> None:
        self.gid = gid
        self.sleep_times: List[TimeRange] = []
        self.start_sleeping_time: Union[None, str] = None

    def start_sleep(self, time: str):
        self.start_sleeping_time = time

    def wake_up(self, time: str):
        self.sleep_times.append(TimeRange(self.start_sleeping_time, time))
        self.start_sleeping_time

    def total_asleep_time(self) -> int:
        return sum(tr.minutes() - 1 for tr in self.sleep_times)

    def __str__(self) -> str:
        return f"<Guard id={self.gid} sleep_times={self.sleep_times}>"

    def __repr__(self) -> str:
        return self.__str__()


def get_common_items(*items: Sequence[Any]) -> Set[Any]:
    if len(items) == 0:
        return set()
    g_set = set(items[0])
    for item in items[1:]:
        g_set.intersection_update(item)
    return g_set


################################################################################
def day04p1():
    data = get_input(parse1, args.puzzle)

    sorted_logs: List[Log] = sorted(data)

    guards_datetimes: Dict[Union[int, None], Guard] = {}
    current_guard: Guard = None  # type: ignore

    for log in sorted_logs:
        # print(log)
        if log.is_begin_of_shift():
            if log.guard_id() in guards_datetimes:
                current_guard = guards_datetimes[log.guard_id()]
            else:
                current_guard = Guard(log.guard_id())  # type: ignore
                guards_datetimes[log.guard_id()] = current_guard
        elif "falls asleep" == log.msg:
            current_guard.start_sleep(log.get_time())
        elif "wakes up" == log.msg:
            current_guard.wake_up(log.get_time())

    sleepiest_guard = max(guards_datetimes.values(), key=lambda x: x.total_asleep_time())
    # print(sleepiest_guard)

    slept_mins: Dict[int, int] = collections.defaultdict(int)
    for st in sleepiest_guard.sleep_times:
        for min_ in st.minutes_range():
            slept_mins[min_] += 1
    # print(slept_mins)

    most_slept_min = max(slept_mins.items(), key=lambda x: x[1])

    return most_slept_min[0] * sleepiest_guard.gid


################################################################################
############################### Start of Part 2 ################################
################################################################################
def parse2(line: str):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def process_logs(logs: List[Log]) -> Dict[Union[int, None], Guard]:
    guards_datetimes: Dict[Union[int, None], Guard] = {}
    current_guard: Guard = None  # type: ignore

    for log in sorted(logs):
        # print(log)
        if log.is_begin_of_shift():
            if log.guard_id() in guards_datetimes:
                current_guard = guards_datetimes[log.guard_id()]
            else:
                current_guard = Guard(log.guard_id())  # type: ignore
                guards_datetimes[log.guard_id()] = current_guard
        elif "falls asleep" == log.msg:
            current_guard.start_sleep(log.get_time())
        elif "wakes up" == log.msg:
            current_guard.wake_up(log.get_time())

    return guards_datetimes


################################################################################
def day04p2():
    data = get_input(parse2, args.puzzle)

    logs_by_guard = process_logs(data)

    max_slept_repetitions = 0
    max_slept_minute = 0
    max_slept_guard = None

    slept_minutes: Dict[int, int] = collections.defaultdict(int)
    for guard in logs_by_guard.values():
        print(guard)
        for st in guard.sleep_times:
            for tr in st.minutes_range():
                slept_minutes[tr] += 1
        # print(slept_minutes.values())
        if len(slept_minutes) == 0:
            continue
        minute, repetitions = max(slept_minutes.items(), key=lambda x: x[1])
        print(slept_minutes)
        if repetitions > max_slept_repetitions:
            max_slept_minute = minute
            max_slept_guard = guard
            max_slept_repetitions = repetitions

        slept_minutes.clear()

    print(max_slept_guard, max_slept_minute, max_slept_repetitions)

    return max_slept_guard.gid * max_slept_minute  # type:ignore

def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    if 1 in args.part:
        print()
        print("-" * (n), "Day 04 - Part 1", "-" * n)
        print("Result =>", day04p1())
        print()
    if 2 in args.part:
        print("-" * (n), "Day 04 - Part 2", "-" * n)
        print("Result =>", day04p2())
    print()


main()

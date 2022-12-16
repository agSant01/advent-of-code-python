from typing import (
    Any,
    Callable,
    Iterable,
    List,
    NamedTuple,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)


def convert_to_int(seq: Sequence[str]) -> Tuple[int, ...]:
    return tuple(map(int, seq))


class Day03:
    @staticmethod
    def get_common_items(*items: Sequence[Any]) -> Set[Any]:
        if len(items) == 0:
            return set()
        g_set = set(items[0])
        for item in items[1:]:
            g_set.intersection_update(item)
        return g_set


class Day04:
    @staticmethod
    def is_full_overlap(range1: Sequence[int], range2: Sequence[int]) -> bool:
        if range1[0] >= range2[0] and range1[1] <= range2[1]:
            return True
        if range2[0] >= range1[0] and range2[1] <= range1[1]:
            return True
        return False

    @staticmethod
    def is_partial_overlap(range1: Sequence[int], range2: Sequence[int]) -> bool:
        if range1[0] < range2[0]:
            return range1[1] >= range2[0]
        return range2[1] >= range1[0]


class Day06:
    @staticmethod
    def index_non_repeating_window(data_stream: str, width: int, start_: int = 0) -> int:
        window: List[str] = list(data_stream[start_:width])
        for i in range(start_ + width, len(data_stream)):
            if len(set(window)) != width:
                window.pop(0)
                window.append(data_stream[i])
            else:
                return i
        return -1


E = TypeVar("E")
K = TypeVar("K")


def sorted_insert(
    array: List[E],
    value: E,
    comparator: Callable[[Any, Any], int] = lambda a, b: a - b,
):
    if len(array) == 0:
        array.append(value)
        return

    left = 0
    right = len(array)
    mid = 0

    while left < right:
        mid = (right + left) // 2
        if comparator(value, array[mid]) < 0:
            right = mid
        elif comparator(value, array[mid]) > 0:
            left = mid + 1
        else:
            break

    if comparator(value, array[mid]) > 0:
        mid += 1

    array.insert(mid, value)


class ToVisit(NamedTuple):
    starting_point: Tuple[int, int]
    steps: int
    trail: List[Tuple[int, int]]


def find_paths(
    get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
    is_end: Union[Callable[[Tuple[int, int]], bool], None],
    starting_point: Tuple[int, int] = (0, 0),
    return_visited=False,
) -> Union[List[ToVisit], Set[Tuple[int, int]]]:
    to_visit: List[Tuple[Tuple[int, int], int, List[Tuple[int, int]]]] = [
        ToVisit(starting_point, 0, [])
    ]
    visited: Set[Tuple[int, int]] = set()
    result = []

    while len(to_visit) > 0:
        c_c, steps, trail = to_visit.pop(0)

        if c_c in visited:
            continue

        visited.add(c_c)

        if is_end and is_end(c_c):
            result.append(ToVisit(c_c, steps, trail))
            continue

        for nb in get_neighbors(c_c):
            if nb not in visited:
                new_trail = trail + [c_c]
                to_visit.append(ToVisit(nb, steps + 1, new_trail))

    if return_visited:
        return visited

    return result


def manhattan_distance(v1: Iterable[int], v2: Iterable[int]) -> int:
    return sum(abs(p - q) for p, q in zip(v1, v2))

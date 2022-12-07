from typing import Any, Callable, Generator, List, Sequence, Set, Tuple, TypeVar


def convert_to_int(seq: Sequence[str]) -> Tuple[int]:
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


def dfs(
    points: Sequence[E],
    visitor_function: Callable[[E], K],
    neighbor_iter: Callable[[E], List[E]],
) -> Generator[K, None, None]:
    to_visit: List[E] = [points[0]]
    visited: Set[E] = set()

    while len(to_visit) > 0:
        c = to_visit.pop(0)

        if c in visited:
            continue

        yield visitor_function(c)

        to_visit.extend(neighbor_iter(c))

    return None


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

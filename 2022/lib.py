from typing import Any, Iterable, Set


class Day03:
    @staticmethod
    def get_common_items(*items: Iterable[Any]) -> Set[Any]:
        if len(items) == 0:
            return set()
        g_set = set(items[0])
        for item in items[1:]:
            g_set.intersection_update(item)
        return g_set

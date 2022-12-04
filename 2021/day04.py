from typing import Dict, List, Tuple


def get_filename(test=False):
    return f'day04_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line):
    return line


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def has_bingo(plays: set) -> bool:
    """
    Time complexity:
     - Worst: O(m*n)

    Args:
        plays (set): set of (x, y) coordinates of valid plays

    Returns:
        bool: True if ig has bingo, otherwise returns False
    """
    # check horizontal
    for x in range(5):
        horizontal = True
        for y in range(5):
            if (x, y) not in plays:
                horizontal = False
                break
        if horizontal:
            return True

    # check vertical
    for y in range(5):
        vertical = True
        for x in range(5):
            if (x, y) not in plays:
                vertical = False
                break
        if vertical:
            return True

    return False


def boards_to_dicts(lines: str) -> List[Dict[int, Tuple[int, int]]]:
    # Worst time complexity: O(TB * m * n)
    boards = []
    tmp_board = []
    tmp_map = {}
    for line in lines:
        if len(line) == 0:
            # O(m * n) = 25
            for i, v1 in enumerate(tmp_board):
                for j, v2 in enumerate(v1):
                    tmp_map[v2] = (i, j)
            boards.append(tmp_map)
            tmp_map = {}
            tmp_board = []
        else:
            # O(m) = 5
            tmp_board.append(list(map(int, line.split())))
    return boards


################################################################################


def day04p1():
    # TB: Total Boards
    # m: matrix columns
    # n: matrix rows
    # p: plays

    # Worst time complexity: O(TB * p * m * n)
    # Mem complexity: O(p * TB * m * n)
    data = get_input(parse1, test=False)

    # Play list
    numbers: List[int] = list(map(int, data[0].split(",")))

    # O(TB * n * m )
    boards = boards_to_dicts(data[2:])

    # O(TB)
    board_plays = [set() for _ in range(len(boards))]

    # O(p * TB * m * n)
    for play in numbers:
        for idx, board in enumerate(boards):
            if play not in board:
                continue
            board_plays[idx].add(board[play])
            # Bingo is O(m*n)
            if has_bingo(board_plays[idx]):
                # Sum of non-used values is: O(m*n)
                sum_all = sum(
                    map(
                        lambda kv: kv[0],
                        filter(lambda kv: kv[1] not in board_plays[idx], board.items()),
                    )
                )
                return play * sum_all


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day04p2():
    data = get_input(parse2, test=False)
    numbers = list(map(int, data[0].split(",")))

    boards = boards_to_dicts(data[2:])

    board_plays = [set() for _ in range(len(boards))]

    loosers = set([i for i in range(len(boards))])
    last_winner = False
    for play in numbers:
        for idx, board in enumerate(boards):
            if len(loosers) == 1:
                last_winner = True
            if play not in board or idx not in loosers:
                continue
            board_plays[idx].add(board[play])
            if has_bingo(board_plays[idx]):
                if last_winner:
                    sum_all = sum(
                        map(
                            lambda kv: kv[0],
                            filter(
                                lambda kv: kv[1] not in board_plays[idx], board.items()
                            ),
                        )
                    )
                    return play * (sum_all)
                loosers.remove(idx)

    # for play in numbers:
    return loosers


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 04 - Part 1", "-" * n)
    print("Result =>", day04p1())
    print()
    print("-" * (n), "Day 04 - Part 2", "-" * n)
    print("Result =>", day04p2())
    print()


main()

import collections
import re
from typing import Dict, Tuple


def get_filename(test=False):
    return f'day21_input{"_test" if test else ""}.txt'


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


def parse1(line: str):
    return tuple(map(int, re.findall(r"Player (\d+) starting position: (\d+)", line)[0]))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def deterministic_dice(max_=100):
    counter = 0

    def roll_dice():
        nonlocal counter
        counter += 1
        counter %= max_
        return counter

    return roll_dice


def player_selector(players):
    curr_player = -1

    def next_():
        nonlocal curr_player
        curr_player += 1
        curr_player %= players
        return curr_player

    return next_


################################################################################


def day21p1():
    data = get_input(parse1, test=False)

    scores = [0 for _ in range(len(data))]  # [player1, player2]
    positions = [pos for _, pos in data]

    LEN_TRACK = 10
    WINNING_SCORE = 1000

    next_player = player_selector(2)
    roll_dice = deterministic_dice()
    dice_rolls = 0

    while True:
        player = next_player()

        steps = 0
        for _ in range(3):
            steps += roll_dice()

        dice_rolls += 3

        next_position = (positions[player] + steps) % LEN_TRACK

        if next_position == 0:
            next_position = 10

        positions[player] = next_position
        scores[player] += positions[player]

        if scores[player] >= WINNING_SCORE:
            looser = next_player()
            return scores[looser] * dice_rolls


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


WINNING_SCORE_P2 = 21
LEN_TRACK = 10

wins = 0


def play_game(positions: list) -> None:
    global wins

    universes: Dict[Tuple[Tuple, Tuple], int] = collections.defaultdict(int)
    universal_wins = [0, 0]

    state = ((0, 0), tuple(positions))
    universes[state] = 1

    rolls = collections.defaultdict(int)

    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                rolls[i + j + k] += 1

    while len(universes) > 0:
        temp = dict(universes)
        universes = collections.defaultdict(int)
        for state, current_branches in temp.items():
            (score_p1, score_p2), (pos_p1, pos_p2) = state
            for roll_p1, created_branches in rolls.items():
                p1_branches = current_branches * created_branches
                new_position_p1 = (pos_p1 + roll_p1 - 1) % LEN_TRACK + 1
                new_score_p1 = score_p1 + new_position_p1
                if new_score_p1 >= 21:
                    universal_wins[0] += p1_branches
                    continue

                for roll_p2, created_branches_p2 in rolls.items():
                    p2_branches = p1_branches * created_branches_p2
                    new_position_p2 = (pos_p2 + roll_p2 - 1) % LEN_TRACK + 1
                    new_score_p2 = score_p2 + new_position_p2
                    if new_score_p2 >= 21:
                        universal_wins[1] += p2_branches
                        continue
                    new_state = (
                        (new_score_p1, new_score_p2),
                        (new_position_p1, new_position_p2),
                    )
                    universes[new_state] += p2_branches

    return universal_wins


################################################################################


def day21p2():
    data = get_input(parse2, test=True)

    positions = [pos for _, pos in data]

    p1_wins, p2_wins = play_game(positions)

    return max(p1_wins, p2_wins)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 21 - Part 1", "-" * n)
    print("Result =>", day21p1())
    print()
    print("-" * (n), "Day 21 - Part 2", "-" * n)
    print("Result =>", day21p2())
    print()


main()

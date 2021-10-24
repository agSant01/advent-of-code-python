import math
import functools
import itertools


def get_filename(test=False):
    return f'day21_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data

################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    return int(line.split(':')[1])

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


Weapons = [  # Cost  Damage  Armor
    ('Dagger', [8, 4, 0]),
    ('Shortsword', [10, 5, 0]),
    ('Warhammer', [25, 6, 0]),
    ('Longsword', [40, 7, 0]),
    ('Greataxe', [74, 8, 0]),
]

# Armor:      Cost  Damage  Armor
Armors = [
    ('Leather', [13, 0, 1]),
    ('Chainmail', [31, 0, 2]),
    ('Splintmail', [53, 0, 3]),
    ('Bandedmail', [75, 0, 4]),
    ('Platemail', [102, 0, 5]),
]

# Rings:      Cost  Damage  Armor
Rings = [
    ('Damage +1', [25, 1, 0]),
    ('Damage +2', [50, 2, 0]),
    ('Damage +3', [100, 3, 0]),
    ('Defense +1', [20, 0, 1]),
    ('Defense +2', [40, 0, 2]),
    ('Defense +3', [80, 0, 3]),
]


def add(value, element):
    return [value[0] + element[0], value[1] + element[1], value[2] + element[2]]


def winner(player1, player2):
    hitpoints1, damage1, armor1 = player1
    hitpoints2, damage2, armor2 = player2

    # resulting damages of each player
    d1_r = max(damage1 - armor2, 0)
    d2_r = max(damage2 - armor1, 0)

    # player 1 goes first
    # hist by player 2
    if d2_r == 0:
        hits_to_p1 = math.inf
    else:
        hits_to_p1 = hitpoints1/d2_r

    if d1_r == 0:
        hits_to_p2 = math.inf
    else:
        hits_to_p2 = hitpoints2/d1_r - 1

    if hits_to_p1 == math.inf and hits_to_p2 == math.inf:
        # both are inf
        return 'player1'

    if hits_to_p1 - hits_to_p2 == 0:
        return 'tie'

    if hits_to_p1 - hits_to_p2 > 0:
        return 'player1'

    return 'player2'


def generate_fight_configurations():
    combinations = []
    for w in Weapons:
        combinations.append(w[1])

    for _, cost in Weapons:
        for _, cost_ in Armors:
            combinations.append(add(cost, cost_))

    temp = combinations.copy()

    for r in range(1, 3):
        for i in itertools.combinations(map(lambda x: x[1], Rings), r):
            k = functools.reduce(add, i, [0, 0, 0])
            for t in temp:
                combinations.append(add(t, k))

    combinations = sorted(combinations, key=lambda x: x[0])

    return combinations

################################################################################


def day21p1():
    battle_boss = get_input(parse1, test=False)

    HITPOINTS = 100

    combinations = generate_fight_configurations()

    #  8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage, and 2 armor:
    for configuration in combinations:
        result = winner([HITPOINTS, configuration[1],
                         configuration[2]], battle_boss)
        if result == 'player1':
            return configuration

    return result


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day21p2():
    battle_boss = get_input(parse2, test=False)

    HITPOINTS = 100

    combinations = generate_fight_configurations()
    combinations = sorted(combinations, key=lambda x: x[0], reverse=True)

    #  8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage, and 2 armor:
    for configuration in combinations:
        result = winner(
            [
                HITPOINTS,
                configuration[1],
                configuration[2]
            ],
            battle_boss)
        if result == 'player2':
            return configuration

    return result


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 21 - Part 1", '-'*n)
    print('Result =>', day21p1())
    print()
    print('-'*(n), "Day 21 - Part 2", '-'*n)
    print('Result =>', day21p2())
    print()


main()

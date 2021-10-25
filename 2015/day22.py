from itertools import filterfalse
import random
import copy
import math


def get_filename(test=False):
    return f'day22_input{"_test" if test else ""}.txt'


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


def parse1(line):
    return int(line.split(':')[1])

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


# SPELLS
# Cost, Damage, Heal, TurnsActive, ArmorIncrease, ManaIncrease
SPELLS = [
    ['MagicMissile', [53, 4, 0, 0, 0, 0]],
    ['Drain', [73, 2, 2, 0, 0, 0]],
    ['Shield', [113, 0, 0, 6, 7, 0]],
    ['Poison', [173, 3, 0, 6, 0, 0]],
    ['Recharge', [229, 0, 0, 5, 0, 101]]
]


class Player:
    def __init__(self, hitpoints, damage, armor=0, mana=0, used_mana=0) -> None:
        self.hitpoints = hitpoints
        self.damage = damage
        self.armor = armor
        self.remaining_mana = mana
        self.used_mana = used_mana
        self.plays = []

    def __copy__(self):
        plyr = Player(
            copy.copy(self.hitpoints),
            copy.copy(self.damage),
            copy.copy(self.armor),
            copy.copy(self.remaining_mana),
            copy.copy(self.used_mana),
        )
        plyr.plays = copy.copy(self.plays)
        return plyr

    def __str__(self) -> str:
        return f'Player {{ Hitpoints:{self.hitpoints} | Damage:{self.damage} | Armor:{self.armor} | RemMana:{self.remaining_mana} | UsedMana:{self.used_mana} }}'


class Container:
    def __init__(self, player_stats: Player, boss_stats: Player) -> None:
        self.player = player_stats
        self.boss = boss_stats

    def __copy__(self):
        return Container(
            copy.copy(self.player),
            copy.copy(self.boss)
        )


class Effects:
    def __init__(self) -> None:
        self.Shield = 0
        self.Poison = 0
        self.Recharge = 0

    def activate_effect(self, id):
        if id == 2:
            self.Shield = 6
        if id == 3:
            self.Poison = 6
        if id == 4:
            self.Recharge = 5

    def use_effects(self, player: Player, boss: Player) -> None:
        """Returns an array with the values of the increments of the stats

        Returns:
            [list]: [armor, damage, additional_mana]
        """
        if self.Shield > 0:
            player.armor = 7
            self.Shield -= 1
        else:
            player.armor = 0

        if self.Poison > 0:
            boss.hitpoints -= 3
            self.Poison -= 1

        if self.Recharge > 0:
            player.remaining_mana += 101
            self.Recharge -= 1

    def is_active(self, id: int):
        if id == 2 and self.Shield > 0:
            return True

        if id == 3 and self.Poison > 0:
            return True

        if id == 4 and self.Recharge > 0:
            return True

        return False

    def __copy__(self):
        eff = Effects()
        eff.Shield = self.Shield
        eff.Poison = self.Poison
        eff.Recharge = self.Recharge
        return eff

    def __str__(self) -> str:
        return f'Shield:{self.Shield} | Poison:{self.Poison} | Recharge:{self.Recharge}'


class Result:
    GLOBAL_MIN = math.inf
    PLAYER: Player = None

    def __str__(self) -> str:
        return f'Result {{ GLOBAL_MIN: {self.GLOBAL_MIN}, PLAYER: {str(self.PLAYER)} }}'


def fight_round(turn: int, spell_to_use: int, container: Container, effects_active: Effects, result: Result, hard_mode=False):
    if container.player.used_mana >= result.GLOBAL_MIN:
        return

    # Player turn
    if hard_mode:
        #  hard mode removes a hitpoint before effects
        container.player.hitpoints -= 1
        if container.player.hitpoints <= 0:
            return

    # Activate effects
    effects_active.use_effects(container.player, container.boss)

    # Is still active? can not activate spell if still active
    if effects_active.is_active(spell_to_use):
        return

    # check boss hits
    if container.boss.hitpoints <= 0:
        if result.GLOBAL_MIN > container.player.used_mana:
            result.GLOBAL_MIN = container.player.used_mana
            result.PLAYER = copy.copy(container.player)
        return

    # try to use spell
    Cost, Damage, Heal, _, _, _ = SPELLS[spell_to_use][1]
    if container.player.remaining_mana < Cost:
        return

    # can use spell
    effects_active.activate_effect(spell_to_use)

    container.player.used_mana += Cost
    container.player.remaining_mana -= Cost
    container.player.hitpoints += Heal
    container.player.plays.append(
        (SPELLS[spell_to_use][0], str(container.player)))

    if spell_to_use != 3:
        container.boss.hitpoints -= max(Damage, 1)

    if container.boss.hitpoints <= 0:
        if result.GLOBAL_MIN > container.player.used_mana:
            result.GLOBAL_MIN = container.player.used_mana
            result.PLAYER = copy.copy(container.player)
        return

    # Boss Turn
    effects_active.use_effects(container.player, container.boss)

    if container.boss.hitpoints <= 0:
        if result.GLOBAL_MIN > container.player.used_mana:
            result.GLOBAL_MIN = container.player.used_mana
            result.PLAYER = copy.copy(container.player)
        return

    container.player.hitpoints -= max(container.boss.damage -
                                      container.player.armor, 1)

    if container.player.hitpoints <= 0:
        return

    container.player.armor = 0

    for id in range(len(SPELLS)):
        fight_round(
            turn+1, id, copy.copy(container), copy.copy(effects_active), result, hard_mode)


################################################################################
"""
You start with 50 hit points and 500 mana points. 
The boss's actual stats are in your puzzle input. What is the least 
amount of mana you can spend and still win the fight? 
(Do not include mana recharge effects as "spending" negative mana.)
"""


def day22p1():
    is_test = False

    # Hit Points, Damage
    evil_wizard = get_input(parse1, test=is_test)
    print('Evil Wiz', evil_wizard)

    if is_test:
        player = Player(10, 0, 0, 250, 0)
        boss = Player(14, 8)
    else:
        MY_MANA = 500
        HIT_POINTS = 50

        player = Player(HIT_POINTS, 0, 0, MY_MANA, 0)
        boss = Player(evil_wizard[0], evil_wizard[1])

    result = Result()

    print('[Debug] Player:', player)
    print('[Debug] Boss:', boss)

    for spell in range(len(SPELLS)):
        container = Container(
            copy.copy(player),
            copy.copy(boss)
        )
        fight_round(0, spell, container, Effects(), result)

    for id, i in enumerate(result.PLAYER.plays):
        print('id:', id, str(i))

    return result.GLOBAL_MIN

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day22p2():
    is_test = False

    # Hit Points, Damage
    evil_wizard = get_input(parse1, test=is_test)
    print('Evil Wiz', evil_wizard)

    if is_test:
        player = Player(10, 0, 0, 250, 0)
        boss = Player(14, 8)
    else:
        MY_MANA = 500
        HIT_POINTS = 50

        player = Player(HIT_POINTS, 0, 0, MY_MANA, 0)
        boss = Player(evil_wizard[0], evil_wizard[1])

    result = Result()

    print('[Debug] Player:', player)
    print('[Debug] Boss:', boss)

    for spell in range(len(SPELLS)):
        container = Container(
            copy.copy(player),
            copy.copy(boss)
        )
        fight_round(0, spell, container, Effects(), result, hard_mode=True)

    for id, i in enumerate(result.PLAYER.plays):
        print('id:', id, str(i))

    return result.GLOBAL_MIN


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 22 - Part 1", '-'*n)
    print('Result =>', day22p1())
    print()
    print('-'*(n), "Day 22 - Part 2", '-'*n)
    print('Result =>', day22p2())
    print()


main()

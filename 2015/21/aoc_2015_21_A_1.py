# aoc_2015_21_A_1.py - Day 21: RPG Simulator 20XX - part 1
# What is the least amount of gold you can spend and still win the fight?
# https://adventofcode.com/2015/day/21


from tools import time_it

from dataclasses import dataclass
from itertools import cycle, product

from pprint import pprint


DATA_PATH = './input_2015_21'

WEAPONS = {
    'Dagger': {'cost': 8, 'damage': 4, 'armor': 0},
    'Shortsword': {'cost': 10, 'damage': 5, 'armor': 0},
    'Warhammer': {'cost': 25, 'damage': 6, 'armor': 0},
    'Longsword': {'cost': 40, 'damage': 7, 'armor': 0},
    'Greataxe': {'cost': 74, 'damage': 8, 'armor': 0},
}

ARMOR = {
    'None': {'cost': 0, 'damage': 0, 'armor': 0},
    'Leather': {'cost': 13, 'damage': 0, 'armor': 1},
    'Chainmail': {'cost': 31, 'damage': 0, 'armor': 2},
    'Splintmail': {'cost': 53, 'damage': 0, 'armor': 3},
    'Bandedmail': {'cost': 75, 'damage': 0, 'armor': 4},
    'Platemail': {'cost': 102, 'damage': 0, 'armor': 5},
}

RINGS = {
    'None': {'cost': 0, 'damage': 0, 'armor': 0},
    'Damage +1': {'cost': 25, 'damage': 1, 'armor': 0},
    'Damage +2': {'cost': 50, 'damage': 2, 'armor': 0},
    'Damage +3': {'cost': 100, 'damage': 3, 'armor': 0},
    'Defense +1': {'cost': 20, 'damage': 0, 'armor': 1},
    'Defense +2': {'cost': 40, 'damage': 0, 'armor': 2},
    'Defense +3': {'cost': 80, 'damage': 0, 'armor': 3},
}


@dataclass
class BasePlayer:
    name: str
    hitpoints: int

    def take_hit(self, damage, verbose=False):
        self.hitpoints -= max(damage - self.defense, 1)
        if verbose:
            print(f'{self.name} takes {max(damage - self.defense, 1)} damage and now has {self.hitpoints} health left')


@dataclass
class Player(BasePlayer):
    weapon: str
    armor: str
    rings: tuple[str, str]

    @property
    def damage(self):
        return (WEAPONS[self.weapon]['damage'] +
                RINGS[self.rings[0]]['damage'] +
                RINGS[self.rings[1]]['damage'])

    @property
    def defense(self):
        return (ARMOR[self.armor]['armor'] +
                RINGS[self.rings[0]]['armor'] +
                RINGS[self.rings[1]]['armor'])

    @property
    def cost(self):
        return (WEAPONS[self.weapon]['cost'] +
                ARMOR[self.armor]['cost'] +
                RINGS[self.rings[0]]['cost'] +
                RINGS[self.rings[1]]['cost'])


@dataclass
class Boss(BasePlayer):
    damage: int
    defense: int


@ dataclass
class Game:
    boss: Boss
    player: Player | Boss

    def play(self, verbose=False) -> tuple[Player | Boss, Player | Boss]:
        attack = cycle([self.player, self.boss])
        defend = cycle([self.boss, self.player])
        while True:
            attacker = next(attack)
            defender = next(defend)
            defender.take_hit(attacker.damage, verbose)
            if defender.hitpoints <= 0:
                return attacker, defender


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_boss(data_lines: list[str], name: str) -> Boss:
    return Boss(
        name,
        int(data_lines[0].split(': ')[-1]),  # hitpoints
        int(data_lines[1].split(': ')[-1]),  # damage
        int(data_lines[2].split(': ')[-1]),  # armor
    )


def get_player(
        data_lines: list[str],
        name: str,
        weapon: str,
        armor: str,
        rings: tuple[str, str]
) -> Player:
    return Player(
        name,
        int(data_lines[0].split(': ')[-1]),  # hitpoints
        weapon,
        armor,
        rings
    )


def try_all(boss_data: list[str], player_data: list[str]) -> list:
    games = []
    for weapon, armor, ring1, ring2 in product(WEAPONS, ARMOR, RINGS, RINGS):
        if ring1 == ring2 and ring1 != 'None':  # cannot have 2 identical rings
            continue
        boss = get_boss(boss_data, 'Boss')
        # print(boss.hitpoints, boss.damage, boss.defense)
        player = get_player(player_data, 'Player', weapon, armor, (ring1, ring2))
        # print(player.hitpoints, player.damage, player.defense)

        game = Game(boss, player)

        winner, loser = game.play()
        # print(f'Winner: {winner}')
        # print(f'Loser: {loser}')

        # games.append({'winner': winner, 'loser': loser})
        if winner == player:
            games.append({'winner': player, 'cost': player.cost})

    return games


test_boss = '''
Hit Points: 12
Damage: 7
Armor: 2
'''.strip().splitlines()

test_player = '''
Hit Points: 8
Damage: 5
Armor: 5
'''.strip().splitlines()

actual_player = '''
Hit Points: 100
'''.strip().splitlines()


@time_it
def main(boss_data: list[str], player_data: list[str]) -> None:
    games = try_all(boss_data, player_data)
    # pprint(games)

    print(f'End result: {min(games, key=lambda g: g["cost"])}')


if __name__ == "__main__":
    boss_data = load_data(DATA_PATH)
    player_data = actual_player
    # boss_data = test_boss
    # player_data = test_player
    # print(data_lines)

    main(boss_data, player_data)
    # using input data:
    #   End result: 91
    #   Finished 'main' in 55 milliseconds

    # # test class Player & class Boss
    # player = Player('Player', 100, 'Dagger', 'Leather', ('Damage +1', 'Defense +3'))
    # print(player, player.hitpoints, player.damage, player.defense, player.cost)
    # boss = Boss('Boss', 100, 8, 2)
    # print(boss, boss.hitpoints, boss.damage, boss.defense)

    # # test class Game
    # boss = get_boss(boss_data, 'Boss')
    # # print(boss, boss.hitpoints, boss.damage, boss.defense)
    # # player = get_player(player_data, 'Player', 'Dagger', 'Leather', ('Damage +1', 'Defense +3'))
    # player = get_boss(player_data, 'Player')
    # # print(player, player.hitpoints, player.damage, player.defense)
    #
    # game = Game(boss, player)
    #
    # winner, loser = game.play(verbose=True)
    # print(f'Winner: {winner}')
    # print(f'Loser: {loser}')

# aoc_2015_21_B_1.py - Day 21: RPG Simulator 20XX - part 2
# What is the least amount of gold you can spend and still win the fight?
# https://adventofcode.com/2015/day/21


from aoc_2015_21_A_1 import (
    DATA_PATH,
    load_data,
    actual_player,
    WEAPONS,
    ARMOR,
    RINGS,
    get_player,
    get_boss,
    Game,
)

from tools import time_it

from itertools import cycle, product

from pprint import pprint


# other constants


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
        if loser == player:
            games.append({'loser': player, 'cost': player.cost})

    return games


@time_it
def main(boss_data: list[str], player_data: list[str]) -> None:
    games = try_all(boss_data, player_data)
    # pprint(games)

    print(f'End result: {max(games, key=lambda g: g["cost"])}')


if __name__ == "__main__":
    boss_data = load_data(DATA_PATH)
    player_data = actual_player
    # boss_data = test_boss
    # player_data = test_player
    # print(data_lines)

    main(boss_data, player_data)
    # using input data:
    #   End result: 158
    #   Finished 'main' in 59 milliseconds

# aoc_2015_22_B_1.py - Day 22: Wizard Simulator 20XX - part 2
# What is the least amount of mana you can spend and still win the fight?
# https://adventofcode.com/2015/day/22


from aoc_2015_22_A_1 import (
    DATA_PATH,
    load_data,
    get_boss,
    get_player,
    test_player,
    actual_player,
    test_boss1,
    test_boss2,
    SPELLS,
    MAX_TRIES,
    spells1,
    spells2,
    Player,
    Boss,
    Game,
    State
)

from tools import time_it

# other imports

from pprint import pprint


MAX_SPELLS = 9

HARD_MODE = True


# other functions


@time_it
def main(boss_data: list[str], player_data: list[str], verbose: int = 0) -> None:
    # initial list of states: every state starts with one of the SPELLS
    states = sorted([State([spell]) for spell in SPELLS], key=lambda s: s.mana_spent)

    # declare variables to be used outside the loop
    state = None
    boss = None
    player = None
    winner = None

    # initialize try counter
    tries = 0

    # determine width of tries string
    tries_width = len(f'{MAX_TRIES:,}')

    while states:
        tries += 1

        state = states.pop(0)  # get first (lowest cost) state from list
        player = get_player(player_data, 'Player')  # create a new player for this game
        boss = get_boss(boss_data, 'Boss')  # create a new boss for this game
        game = Game(boss, player)

        # if verbose > 0:
        if verbose > 0 and tries % 1000 == 0:
            print(f'{tries:{tries_width},} / {MAX_TRIES:{tries_width},} {state.spells}', end=' -> ')

        winner, turns = game.play([spell for spell in state.spells], hard_mode=HARD_MODE, verbose=verbose > 1)

        if winner == player:
            print(f'{player.name} won in {turns} turns')
            break
        # elif winner is None:  # None -> not enough spells
        else:
            # if verbose > 0:
            if verbose > 0 and tries % 1000 == 0:
                print(f'{boss.name} won in {turns} turns') if winner == boss else print(f'undecided in {turns} turns')

            # add spells to current state, except the last one used
            if len(state.spells) < MAX_SPELLS:
                states.extend(State(state.spells + [spell]) for spell in SPELLS)
                states = sorted(states, key=lambda s: s.mana_spent)  # sort states by mana spent

        if verbose > 1:
            print('=' * 100)

        if tries >= MAX_TRIES:
            break

    if verbose:
        print('=' * 100)

    if winner == player:
        print(f'\nEnd result: {states[0].mana_spent} - {", ".join(state.spells)}')
    else:
        print('\nDidn\'t find a solution.')


spells3 = '''
Poison
Drain
Recharge
Poison
Shield
Recharge
Poison
Drain
'''.strip().splitlines()



if __name__ == "__main__":
    player_data = actual_player
    # player_data = test_player
    boss_data = load_data(DATA_PATH)
    # boss_data = test_boss1
    # boss_data = test_boss2
    # spells = spells1
    # spells = spells2
    spells = spells3
    # print(data_lines)

    main(boss_data, player_data, 1)
    # using test_data boss1 with MAX_SPELLS = 2, 3, 4, 5, 6, 7:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 6 minutes and 50 seconds (7)
    # using test_data boss2 with MAX_SPELLS = 5:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 1 second
    # using test_data boss2 with MAX_SPELLS = 6:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 15 seconds
    # using test_data boss2 with MAX_SPELLS = 7:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 6 minutes and 59 seconds
    # using input data with MAX_SPELLS = 7:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 6 minutes and 26 seconds
    # using input data with MAX_SPELLS = 8:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 3 hours, 3 minutes and 57 seconds
    # using input data with MAX_SPELLS = 9:
    #   End result: Didn't find a solution.
    #   Finished 'main' by interruption after +48h
    #   Abandonded this strategy and found a working program online that takes 10 seconds in hard mode

    # # test HARD_MODE
    # player = get_player(player_data, 'Player')
    # # player.hitpoints += 1  # needed for test scenario 1 (test_boss1/spells1) for Player to win
    # # player.hitpoints += 5  # needed for test scenario 2 (test_boss2/spells2) for Player to win
    # boss = get_boss(boss_data, 'Boss')
    # game = Game(boss, player)
    # winner, turns = game.play(spells, hard_mode=HARD_MODE, verbose=True)
    # print('=' * 100)
    # print(f'Winner: {winner}')

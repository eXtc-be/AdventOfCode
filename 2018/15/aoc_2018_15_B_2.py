# aoc_2018_15_B_1.py - Day 15: Beverage Bandits - part 2
# After increasing the Elves' attack power until it is just barely enough for them to win without any Elves dying,
# what is the outcome of the combat described in your puzzle input?
# https://adventofcode.com/2018/day/15
# No correct solution found


from aoc_2018_15_A_1 import (
    DATA_PATH,
    load_data,
    test_data_A, test_data_B, test_data_C, test_data_D, test_data_E, test_data_F,
    clear,
)

from aoc_2018_15_A_extern_1 import (
    Grid,
    Type,
    ElfDied,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


turn = 0


@time_it
def main(
        data_lines: list[str],
        verbose: bool = False,
        confirm_next_round: bool = False,
        confirm_next_step: bool = False,
        elf_start_attack_power: int = 4
) -> None:
    elf_attack_power = elf_start_attack_power

    while True:
        grid = None
        # winner_type = None
        # rounds = 0
        # hp_left = 0

        try:
            print(f'Trying Elf attack power {elf_attack_power}')
            grid = Grid(data_lines, elf_attack_power)
            winner_type, rounds, hp_left = grid.play(True, verbose, confirm_next_round, confirm_next_step)
        except ElfDied:
            print(f'An Elf died in round {grid.rounds}')
            elf_attack_power += 1
            continue
        else:
            print(f'{"Elves" if winner_type == Type.ELF else "Goblins"} win '
                  f'after {rounds} full rounds with {hp_left} hit points left '
                  f'and attack power {elf_attack_power}. '
                  f'Score: {rounds} * {hp_left} = {rounds * hp_left}')
            break


if __name__ == "__main__":
    main(load_data(DATA_PATH), verbose=False, confirm_next_round=False, confirm_next_step=False)

    # main(test_data, verbose=True, confirm_next_round=True, confirm_next_step=True)
    # main(test_data, verbose=True, confirm_next_round=False)

    # main(test_data_A, verbose=False, confirm_next_round=False)
    # main(test_data_C, verbose=False, confirm_next_round=False)
    # main(test_data_D, verbose=False, confirm_next_round=False)
    # main(test_data_E, verbose=False, confirm_next_round=False)
    # main(test_data_F, verbose=False, confirm_next_round=False)

    # using test_data A:
    #   End result: Elves win after 29 full rounds with 172 hit points left and attack power 15. Score: 29 * 172 = 4988
    #   Finished 'main' in 66 milliseconds
    # using test_data C:
    #   End result: Elves win after 33 full rounds with 948 hit points left and attack power 4. Score: 33 * 948 = 31284
    #   Finished 'main' in 14 milliseconds
    # using test_data D:
    #   End result: Elves win after 37 full rounds with 94 hit points left and attack power 15. Score: 37 * 94 = 3478
    #   Finished 'main' in 114 milliseconds
    # using test_data E:
    #   End result: Elves win after 39 full rounds with 166 hit points left and attack power 12. Score: 39 * 166 = 6474
    #   Finished 'main' in 126 milliseconds
    # using test_data F:
    #   End result: Elves win after 30 full rounds with 38 hit points left and attack power 34. Score: 30 * 38 = 1140
    #   Finished 'main' in 466 milliseconds
    # using input data:
    #   End result: Elves win after 38 full rounds with 1508 hit points left and attack power 23. Score: 38 * 1508 = 57304 - too high
    #   Finished 'main' in 28 seconds

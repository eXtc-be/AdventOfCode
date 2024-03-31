# aoc_2018_15_B_1.py - Day 15: Beverage Bandits - part 2
# After increasing the Elves' attack power until it is just barely enough for them to win without any Elves dying,
# what is the outcome of the combat described in your puzzle input?
# https://adventofcode.com/2018/day/15
# No correct solution found


from aoc_2018_15_A_1 import (
    DATA_PATH,
    load_data,
    test_data_A, test_data_B, test_data_C, test_data_D, test_data_E, test_data_F,
    Chars,
    get_grid,
    clear,
    print_grid,
    do_turn,
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
    global turn

    result = None

    elf_attack_power = elf_start_attack_power
    while True:
        print(f'Trying Elf attack power {elf_attack_power}')
        grid = get_grid(data_lines, elf_attack_power)

        while True:
            if verbose:
                clear()
                print(f'Round {turn:3} - Elf attack power {elf_attack_power:3}')
                print_grid(grid)
                if confirm_next_round and not confirm_next_step:
                    input('Press Enter to continue...')
            result = do_turn(grid, no_elf_losses=True, confirm_next_step=confirm_next_step)
            if result:
                break
            turn += 1

        if result[1] < 0:  # an Elf died
            left = sum(unit.hit_points for row in grid for unit in row if unit.alive and unit.type == 'G')
            print(f'An Elf died on turn {turn}; '
                  f'Goblins have {left} hit points left.')
            elf_attack_power += 1
            turn = 0
        else:
            break

    if verbose:
        clear()
        print(f'Round {turn:3} - Elf attack power {elf_attack_power:3}')
        print_grid(grid)

    print(f'{"Elves" if result[0] == Chars.ELF else "Goblins"} win '
          f'after {turn} full rounds with {result[1]} hit points left '
          f'and attack power {elf_attack_power}. '
          f'Score: {turn} * {result[1]} = {turn * result[1]}')


if __name__ == "__main__":
    main(load_data(DATA_PATH), verbose=False, confirm_next_round=False, confirm_next_step=False)
    # main(test_data, verbose=True, confirm_next_round=True, confirm_next_step=True)
    # main(test_data, verbose=True, confirm_next_round=False)
    # main(test_data, verbose=False, confirm_next_round=False)

    # using test_data A:
    #   End result: Elves win after 29 full rounds with 172 hit points left and attack power 15. Score: 29 * 172 = 4988
    #   Finished 'main' in 29 milliseconds
    # using test_data C:
    #   End result: Elves win after 33 full rounds with 948 hit points left and attack power 4. Score: 33 * 948 = 31284
    #   Finished 'main' in 4 milliseconds
    # using test_data D:
    #   End result: Elves win after 37 full rounds with 94 hit points left and attack power 15. Score: 37 * 94 = 3478
    #   Finished 'main' in 39 milliseconds
    # using test_data E:
    #   End result: Elves win after 39 full rounds with 166 hit points left and attack power 12. Score: 39 * 166 = 6474
    #   Finished 'main' in 52 milliseconds
    # using test_data F:
    #   End result: Elves win after 30 full rounds with 38 hit points left and attack power 34. Score: 30 * 38 = 1140
    #   Finished 'main' in 1 second
    # using input data:
    #   End result: Elves win after 38 full rounds with 1508 hit points left and attack power 23. Score: 38 * 1508 = 57304 - too high
    #   Finished 'main' in 57 seconds
    # using previous result, subtracting 1 from the rounds and adding 3 to the hit points:
    #   End result: Elves win after 38 full rounds with 1508 hit points left and attack power 23. Score: 37 * 1511 = 55907 - incorrect
    #   Finished 'main' in 57 seconds

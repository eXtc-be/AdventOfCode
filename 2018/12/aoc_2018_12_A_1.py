# aoc_2018_12_A_1.py - Day 12: Subterranean Sustainability - part 1
# After 20 generations, what is the sum of the numbers of all pots which contain a plant?
# https://adventofcode.com/2018/day/12


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_12'

TURNS = 20

PLANT = '#'
EMPTY = '.'

BOLD = '\033[1m'
ENDC = '\033[0m'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_data(data_lines: list[str]) -> tuple[str, dict[str, str]]:
    initial_state = data_lines[0].split()[-1]

    rules ={}
    for line in data_lines[2:]:
        condition, result = line.split(' => ')
        rules[condition] = result

    return initial_state, rules


def do_turn(state: str, start: int, rules: dict[str, str]) -> tuple[str, int]:
    if state[:2] in [
        condition[-2:]
        for condition, result in rules.items()
        if result == PLANT and condition[:3] == EMPTY * 3
    ]:
        state = '.' + state  # add an empty pot to the left if the first two pots will cause the new pot to grow a plant
        start -= 1

    if state[-2:] in [
        condition[:2]
        for condition, result in rules.items()
        if result == PLANT and condition[-3:] == EMPTY * 3
    ]:
        state = state + '.'  # add an empty pot to the right if the last two pots will cause the new pot to grow a plant

    result = ''
    for i in range(len(state)):
        condition = (
                '.' * (2 - min(2, i)) +
                state[max(i-2, 0):min(len(state), i+2)+1] +
                '.' * (2 - min(2, len(state)-i-1))
        )
        if condition in rules:
            result += rules[condition]
        else:
            result += '.'

    return result, start


test_data = '''
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    initial_state, rules = get_data(data_lines)
    # print(initial_state)
    # pprint(rules)

    state = initial_state
    start = 0
    print(f'{0:2}: {"_" * (start + TURNS)}{state}')
    for turn in range(TURNS):
        state, start = do_turn(state, start, rules)
        print(
            f'{turn+1:2}: '
            f'{"_" * (start + TURNS)}'
            f'{"".join(BOLD+c+ENDC if i+start==0 else c for i, c in enumerate(state))}'
        )

    print(f'End result: {sum(i+start for i, c in enumerate(state) if c==PLANT)}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 325
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 4200
    #   Finished 'main' in 2 milliseconds

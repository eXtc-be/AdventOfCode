# aoc_2015_01_A_1.py - Day 1: Not Quite Lisp - part 1
# To what floor do the instructions take Santa?
# https://adventofcode.com/2015/day/1


from tools import time_it

# other imports


DATA_PATH = './input_2015_01'

UP = '('
DN = ')'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def calculate_floor(instructions: str) -> int:
    return instructions.count(UP) - instructions.count(DN)


test_data = '''
(())
()()
(((
(()(()(
))(((((
())
))(
)))
)())())
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, calculate_floor(line))

    print(f'End result: {calculate_floor(data_lines[0])}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 74
    #   Finished 'main' in less than a millisecond

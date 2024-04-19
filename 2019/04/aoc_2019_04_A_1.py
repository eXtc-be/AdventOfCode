# aoc_2019_04_A_1.py - Day 4: Secure Container - part 1
# How many different passwords within the range given in your puzzle input meet these criteria?
# https://adventofcode.com/2019/day/4


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2019_04'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_range(data: str) -> tuple[int, int]:
    return int(data.split('-')[0]), int(data.split('-')[1])


def validate_code(code: int) -> bool:
    pw_string = str(code)

    if not any(a == b for a, b in zip(pw_string, pw_string[1:])):
        return False

    if any(a > b for a, b in zip(pw_string, pw_string[1:])):
        return False

    return True


test_data = '''
122345
111123
135679
111111
223450
123789
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    start, end = get_range(data)

    valid = [num for num in range(start, end+1) if validate_code(num)]

    print(f'End result: {len(valid)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main('111111-112111')
    # main('111111-121111')
    # main('111111-211111')
    # for line in test_data:
    #     print(line, validate_code(int(line)))

    # using test_data 111111-112111:
    #   End result: 165
    #   Finished 'main' in 2 milliseconds
    # using test_data 111111-121111:
    #   End result: 495
    #   Finished 'main' in 19 milliseconds
    # using test_data:
    #   End result: 1231
    #   Finished 'main' in 145 milliseconds
    # using input data:
    #   End result: 1178
    #   Finished 'main' in 1 second

# aoc_2019_04_B_1.py - Day 4: Secure Container - part 2
# How many different passwords within the range given in your puzzle input meet these criteria?
# https://adventofcode.com/2019/day/4


from aoc_2019_04_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_range,
    validate_code,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def validate_code_2(code: int) -> bool:
    pw_string = str(code)

    unique = set(pw_string)

    return any(pw_string.count(u) == 2 for u in unique)


test_data = '''
112233
123444
111122
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    start, end = get_range(data)

    valid = [num for num in range(start, end+1) if validate_code(num) and validate_code_2(num)]

    print(f'End result: {len(valid)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main('111111-112111')
    # main('111111-121111')
    # main('111111-211111')
    # for line in test_data:
    #     print(line, validate_code_2(int(line)))

    # using test_data 111111-112111:
    #   End result: 64
    #   Finished 'main' in 2 milliseconds
    # using test_data 111111-121111:
    #   End result: 394
    #   Finished 'main' in 19 milliseconds
    # using test_data 111111-211111:
    #   End result: 898
    #   Finished 'main' in 210 milliseconds
    # using input data:
    #   End result: 763
    #   Finished 'main' in 1 second

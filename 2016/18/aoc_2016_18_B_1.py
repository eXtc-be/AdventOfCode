# aoc_2016_18_B_1.py - Day 18: Like a Rogue - part 2
# In a total of 400_000 rows (including the starting row), how many safe tiles are there?
# https://adventofcode.com/2016/day/18


from aoc_2016_18_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    find_next_row,
)

from tools import time_it

# other imports

from pprint import pprint


TOTAL_ROWS = 400_000


# other functions


@time_it
def main(first_row: str, total_rows: int = TOTAL_ROWS) -> None:
    rows = [first_row]
    row = first_row

    for _ in range(total_rows-1):
        row = find_next_row(row)
        rows.append(row)
    # pprint(rows)

    print(f'End result: {sum(row.count(".") for row in rows)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # using input data:
    #   End result: 19986699
    #   Finished 'main' in 12 seconds

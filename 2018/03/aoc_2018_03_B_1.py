# aoc_2018_03_B_1.py - Day 3: No Matter How You Slice It - part 2
# If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
# https://adventofcode.com/2018/day/3


from aoc_2018_03_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_claims,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    claims = get_claims(data_lines)
    # pprint(claims)

    total_width = max(claim.x + claim.w for claim in claims)
    total_height = max(claim.y + claim.h for claim in claims)

    grid = [[0 for _ in range(total_width)] for _ in range(total_height)]
    # pprint(grid)

    for claim in claims:
        for y in range(claim.y, claim.y + claim.h):
            for x in range(claim.x, claim.x + claim.w):
                grid[y][x] += 1
    # pprint(grid)

    claim = None
    for claim in claims:
        if all(grid[y][x] == 1 for y in range(claim.y, claim.y + claim.h) for x in range(claim.x, claim.x + claim.w)):
            break

    print(f'End result: {claim.id}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 650
    #   Finished 'main' in 79 milliseconds

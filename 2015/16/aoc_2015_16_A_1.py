# aoc_2015_16_A_1.py - Day 16: Aunt Sue - part 1
# What is the number of the Sue that got you the gift?
# https://adventofcode.com/2015/day/16


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_16'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_aunts(data_lines: list[str]) -> list[dict[str, int]]:
    aunts = []

    for line in data_lines:
        aunt = {}

        num = int(line[:line.find(':')].split()[-1])
        properties = line[line.find(':')+2:].split(', ')
        for prop in properties:
            property, amount = prop.split(': ')
            aunt[property] = int(amount)

        aunt['num'] = num

        aunts.append(aunt)

    return aunts


def get_mfcsam(data_lines: list[str]) -> dict[str, int]:
    mfcsam = {}
    for line in data_lines:
        property, amount = line.split(': ')
        mfcsam[property] = int(amount)

    return mfcsam


def filter_aunts(aunt: dict[str, int], property: str, value: int) -> bool:
    return aunt[property] == value if property in aunt else True


MFCSAM = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
""".strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    mfcsam = get_mfcsam(MFCSAM)
    # pprint(mfcsam)

    aunts = get_aunts(data_lines)
    # pprint(aunts)

    filtered = aunts  # start value
    for property, value in mfcsam.items():
        filtered = [aunt for aunt in filtered if filter_aunts(aunt, property, value)]

    # pprint(filtered)

    print(f'End result: {filtered[0]["num"]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 373
    #   Finished 'main' in 1 millisecond

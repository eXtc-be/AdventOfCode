# aoc_2015_05_A_1.py - Day 5: Doesn't He Have Intern-Elves For This? - part 1
# How many strings are nice?
# https://adventofcode.com/2015/day/5


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_05'

VOWELS = 'aeiou'
V_THRESHOLD = 3
D_THRESHOLD = 1
EXCLUDED = 'ab cd pq xy'.split()
E_THRESHOLD = 0


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def check_vowels(string: str, vowels: str = VOWELS, num: int = V_THRESHOLD) -> bool:
    return sum(1 for char in string if char in vowels) >= num


def check_double(string: str, num: int = D_THRESHOLD) -> bool:
    return sum(1 for ch1, ch2 in zip(string, string[1:]) if ch1.lower() == ch2.lower()) >= num


def check_excluded(string: str, excluded: str = EXCLUDED) -> bool:
    return sum(1 for ch1, ch2 in zip(string, string[1:]) if (ch1+ch2) in excluded) <= E_THRESHOLD


def is_nice(string: str) -> bool:
    return (
            check_vowels(string) and
            check_double(string) and
            check_excluded(string)
    )


test_data = '''
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nice = [line for line in data_lines if is_nice(line)]
    # print(nice)

    print(f'End result: {len(nice)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 255
    #   Finished 'main' in 6 milliseconds

    # # test check_vowels
    # for line in 'aei xazegov aeiouaeiouaeiou'.split():
    #     print(line, check_vowels(line))

    # # test check_double
    # for line in 'xx abcdde aabbccdd'.split():
    #     print(line, check_double(line))

    # # test check_excluded
    # for line in data_lines:
    #     print(line, check_excluded(line))

# aoc_2017_16_A_1.py - Day 16: Permutation Promenade - part 1
# In what order are the programs standing after their dance?
# https://adventofcode.com/2017/day/16


from tools import time_it

from string import ascii_lowercase

from pprint import pprint


DATA_PATH = './input_2017_16'

CHARS = tuple(c for c in ascii_lowercase[:16])
CHARS_TEST = tuple(c for c in ascii_lowercase[:5])


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_instructions(data: str) -> list[str]:
    return [inst for inst in data.split(',')]


def _spin(programs: tuple[str, ...], num: int) -> tuple[str, ...]:
    return programs[-num:] + programs[:-num]


def _exchange(programs: tuple[str, ...], i: int, j: int) -> tuple[str, ...]:
    # make sure indices are in order
    ii = min(i, j)
    jj = max(i, j)

    return programs[:ii] + programs[jj:jj+1] + programs[ii+1:jj] + programs[ii:ii+1] + programs[jj+1:]


def _partner(programs: tuple[str, ...], a: str, b: str) -> tuple[str, ...]:
    return _exchange(programs, programs.index(a), programs.index(b))


def execute_instructions(programs: tuple[str, ...], instructions: list[str]) -> tuple[str, ...]:
    for instruction in instructions:
        match instruction[0]:
            case 's':
                num = int(instruction[1:])
                programs = _spin(programs, num)
            case 'x':
                i, j = instruction[1:].split('/')
                programs = _exchange(programs, int(i), int(j))
            case 'p':
                a, b = instruction[1:].split('/')
                programs = _partner(programs, a, b)
            case '_':
                raise ValueError(f'Invalid instruction: {instruction}')

    return programs


test_data = '''
s1,x3/4,pe/b
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], programs: tuple[str, ...] = CHARS) -> None:
    instructions = get_instructions(data_lines[0])
    # print(instructions)

    programs = execute_instructions(programs, instructions)

    print(f'End result: {"".join(programs)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, CHARS_TEST)
    # using test_data:
    #   End result: baedc
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: kpbodeajhlicngmf
    #   Finished 'main' in 13 milliseconds

    # # test _spin
    # print(''.join(_spin(CHARS_TEST, 3)))  # cdeab
    # print(''.join(_spin(CHARS_TEST, 5)))  # abcde
    # print(''.join(_spin(CHARS_TEST, 0)))  # abcde
    #
    # # test _spin
    # print(''.join(_exchange(CHARS_TEST, 1, 3)))  # adcbe
    # print(''.join(_exchange(CHARS_TEST, 3, 1)))  # adcbe
    # print(''.join(_exchange(CHARS_TEST, 0, 1)))  # bacde
    # print(''.join(_exchange(CHARS_TEST, 3, 4)))  # abced
    #
    # # test _spin
    # print(''.join(_partner(CHARS_TEST, 'b', 'd')))  # adcbe
    # print(''.join(_partner(CHARS_TEST, 'd', 'b')))  # adcbe
    # print(''.join(_partner(CHARS_TEST, 'a', 'e')))  # ebcda

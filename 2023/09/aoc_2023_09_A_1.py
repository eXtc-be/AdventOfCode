# aoc_2023_09_A_1.py - Day 9: Mirage Maintenance - part 1
# Analyze your OASIS report and extrapolate the next value for each history.
# What is the sum of these extrapolated values?
# https://adventofcode.com/2023/day/9


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_09'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_sequences(data_lines: list[str]) -> list[list[int]]:
    return [[int(number) for number in line.split()] for line in data_lines]


def predict_next_number_in_sequence(sequence: list[int]) -> int:
    differences = [num2-num1 for num1, num2 in zip(sequence, sequence[1:])]
    if all(difference == 0 for difference in differences):
        return sequence[-1]
    else:
        return sequence[-1] + predict_next_number_in_sequence(differences)


def predict_next_number_in_all_sequences(sequences: list[list[int]]) -> list[int]:
    return [predict_next_number_in_sequence(sequence) for sequence in sequences]


test_data = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    sequences = get_sequences(data_lines)
    # print(sequences)

    # for sequence in sequences:
    #     print(predict_next_number_in_sequence(sequence))

    predictions = predict_next_number_in_all_sequences(sequences)
    # print(predictions)

    print(f'End result: {sum(predictions)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 114
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1641934234
    #   Finished 'main' in 5 milliseconds

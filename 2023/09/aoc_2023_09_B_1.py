# aoc_2023_09_B_1.py - Day 9: Mirage Maintenance - part 2
# Analyze your OASIS report again, this time extrapolating the previous value for each history.
# What is the sum of these extrapolated values?
# https://adventofcode.com/2023/day/9


from aoc_2023_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_sequences,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def predict_previous_number_in_sequence(sequence: list[int]) -> int:
    differences = [num2-num1 for num1, num2 in zip(sequence, sequence[1:])]
    if all(difference == 0 for difference in differences):
        return sequence[-1]
    else:
        return sequence[0] - predict_previous_number_in_sequence(differences)


def predict_previous_number_in_all_sequences(sequences: list[list[int]]) -> list[int]:
    return [predict_previous_number_in_sequence(sequence) for sequence in sequences]


@time_it
def main(data_lines: list[str]) -> None:
    sequences = get_sequences(data_lines)
    # print(sequences)

    # for sequence in sequences:
    #     print(predict_previous_number_in_sequence(sequence))

    predictions = predict_previous_number_in_all_sequences(sequences)
    # print(predictions)

    print(f'End result: {sum(predictions)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 975
    #   Finished 'main' in 5 milliseconds

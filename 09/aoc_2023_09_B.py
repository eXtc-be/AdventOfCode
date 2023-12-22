# aoc_2023_09_B.py - Day 9: Mirage Maintenance - part 2
# predict the previous number in a sequence using the differences between them
# https://adventofcode.com/2023/day/9


from aoc_2023_09_A import (
    DATA_PATH,
    load_data,
    test_data,
    get_sequences,
)


def predict_previous_number_in_sequence(sequence):
    differences = [num2-num1 for num1, num2 in zip(list(sequence), list(sequence)[1:])]
    if all(difference == 0 for difference in differences):
        return sequence[-1]
    else:
        return sequence[0] - predict_previous_number_in_sequence(differences)


def predict_previous_number_in_all_sequences(sequences):
    return [predict_previous_number_in_sequence(sequence) for sequence in sequences]


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    sequences = get_sequences(data_lines)
    # print(sequences)

    # for sequence in sequences:
    #     print(predict_previous_number_in_sequence(sequence))

    predictions = predict_previous_number_in_all_sequences(sequences)
    print(predictions)

    print(f'End result: {sum(predictions)}')

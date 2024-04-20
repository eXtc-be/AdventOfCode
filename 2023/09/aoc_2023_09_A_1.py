# aoc_2023_09_A_1.py - Day 9: Mirage Maintenance - part 1
# predict the next number in a sequence using the differences between them
# https://adventofcode.com/2023/day/9


# imports


DATA_PATH = './input_2023_09'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def get_sequences(data_lines):
    return [[int(number) for number in line.split()] for line in data_lines]


def predict_next_number_in_sequence(sequence):
    differences = [num2-num1 for num1, num2 in zip(sequence, sequence[1:])]
    if all(difference == 0 for difference in differences):
        return sequence[-1]
    else:
        return sequence[-1] + predict_next_number_in_sequence(differences)


def predict_next_number_in_all_sequences(sequences):
    return [predict_next_number_in_sequence(sequence) for sequence in sequences]


test_data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".splitlines()


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    sequences = get_sequences(data_lines)
    # print(sequences)

    # for sequence in sequences:
    #     print(predict_next_number_in_sequence(sequence))

    predictions = predict_next_number_in_all_sequences(sequences)
    print(predictions)

    print(f'End result: {sum(predictions)}')

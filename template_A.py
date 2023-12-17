# <filename> - Day <day>: <title> - part 1
# <description>
# https://adventofcode.com/2023/day/<day>


# imports


data_path = './input'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


# functions


test_data = """<testdata>""".splitlines()


if __name__ == "__main__":
    # data_lines = load_data(data_path)
    data_lines = test_data
    print(data_lines)

    # your code

    # print(f'End result: {sum(<last_array>)}')

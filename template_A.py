# <filename> - Day <day>: <title> - part 1
# <description>
# <url>


# imports


DATA_PATH = './input_<year>_<0_day>'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


# functions


test_data = """<testdata>""".splitlines()


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    # your code

    # print(f'End result: {sum(<last_array>)}')

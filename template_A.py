# <filename> - Day <day>: <title> - part 1
# <description>
# <url>


from tools import time_it

# other imports


DATA_PATH = './input_<year>_<0_day>'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = """
<testdata>
<testdata>
<testdata>
""".strip().splitlines()


@time_it
def main(data_lines: list[str]):
    # your code

    print(f'End result: {0}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    main(data_lines)

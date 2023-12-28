# <filename> - Day <day>: <title> - part 2
# <description>
# <url>


from <file_A> import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    # your code

    print(f'End result: {0}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    main(data_lines)

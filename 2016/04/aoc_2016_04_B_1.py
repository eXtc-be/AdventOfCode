# aoc_2016_04_B_1.py - Day 4: Security Through Obscurity - part 2
# What is the sector ID of the room where North Pole objects are stored?
# https://adventofcode.com/2016/day/4


from aoc_2016_04_A_1 import (
    DATA_PATH,
    load_data,
    Room,
    test_data_1,
    test_data_2,
    get_rooms,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


test_data = '''
qzmt-zixmtkozy-ivhz-343[zimth]
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    rooms = get_rooms(data_lines)
    # pprint(rooms)

    real_rooms = [room for room in rooms if room.validate()]
    # pprint(real_rooms)

    for room in real_rooms:
        room_name = room.decrypt()
        # print(room_name)
        if room_name == 'northpole object storage':
            print(f'End result: {room.sector}')
            break


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # data_lines = test_data_1
    # data_lines = test_data_2
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 548
    #   Finished 'main' in 34 milliseconds

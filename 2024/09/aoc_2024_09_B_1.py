# aoc_2024_09_B_1.py - Day 9: Disk Fragmenter - part 2
# Start over, now compacting the amphipod's hard drive using this new method
# instead. What is the resulting filesystem checksum?
# https://adventofcode.com/2024/day/9


from aoc_2024_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    decode_map,
    calc_checksum,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions

def compact_data(data: list[str]) -> list[str]:
    result = [c for c in data]

    src_end = len(result)
    prev_id = result[-1]

    while True:
        # find a contiguous block of data with the same id (a whole file)
        block_id = result[src_end-1]

        src_start = src_end - 1
        while result[src_start-1] == block_id:
            src_start -= 1
        block_length = src_end - src_start

        # if the block_id is larger than the one we did in the previous round,
        # we're dealing with a block we already moved and the rules say we must attempt to move
        # a file exactly once. we wouldn't be able to move it any further left anyway, because the
        # program didn't find a large enough block of free space left of its current position the first time
        if block_id > prev_id:
            src_end = src_start
            continue
        elif block_id == 0:
            break

        if block_id % 100 == 0:
            print(block_id)

        # find a block of empty space that is big enough to fit the file
        dst_start = src_start
        for pos in range(src_start):
            if result[pos:pos+block_length] == ['.'] * block_length:
                dst_start = pos
                break

        # swap src and dst (only if a large enough block of free space has been found)
        if dst_start < src_start:
            result[dst_start:dst_start+block_length], result[src_start:src_start+block_length] = result[src_start:src_start+block_length], result[dst_start:dst_start+block_length]

        # move src_end to the end of the next data block
        src_end = src_start
        while result[src_end-1] == '.':
            src_end -= 1

        prev_id = block_id

    return result


@time_it
def main(data_lines: list[str]) -> None:
    # print(data_lines[0])

    data = decode_map([c for c in data_lines[0]])
    # print(''.join(str(el) for el in data))

    compacted = compact_data(data)
    # print(''.join(str(el) for el in compacted))

    print(f'End result: {calc_checksum(compacted)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 2858
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 6408966547049
    #   Finished 'main' in 1 minute and 41 seconds before optimizing
    #   Finished 'main' in 1 minute and 6 seconds after optimizing (skip if block_id > prev_id)

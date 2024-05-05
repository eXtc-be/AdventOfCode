# aoc_2023_13_B_1.py - Day 13: Point of Incidence - part 2
# Find the new line of reflection in each of the patterns in your notes after cleaning 1 smudge.
# What number do you get after summarizing all of your notes?
# https://adventofcode.com/2023/day/13


from aoc_2023_13_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_patterns,
    # _get_reflection,
    _is_reflection,
)

from tools import time_it

# other imports

from pprint import pprint


FLIP = {
   '#': '.',
   '.': '#',
}


def _flip_cell(pattern: list[list[str]], r: int, c: int) -> list[list[str]]:
    """returns a copy of the original pattern with the cell at row=r and column=c flipped (. <-> #)"""
    return [
        [FLIP[cell] if (rr, cc) == (r, c) else cell for cc, cell in enumerate(row)]
        for rr, row in enumerate(pattern)
    ]


def _get_reflection(pattern: list[list[str]], old_reflection=None, factor=1) -> int:
    """
    finds the row around which a pattern can be mirrored
    only returns when the reflection found is not equal to old_reflection or if none was found
    """
    # factor = 1
    if old_reflection is None:
        old_reflection = -1
    # else:
    #     factor = 100 if old_reflection >= 100 else 1

    for cursor in range(len(pattern) - 1):
        if _is_reflection(pattern, cursor) and (cursor + 1) * factor != old_reflection:
            return cursor + 1  # 0-based vs 1-based

    return 0  # if no reflection was found, return 0 so math further down doesn't break


def _find_new_reflection(pattern: list[list[str]]) -> int | None:
    old_reflection = _get_reflection(pattern) * 100  # try horizontal reflection first
    if not old_reflection:  # try vertical if horizontal failed
        old_reflection = _get_reflection(list(zip(*pattern)))
    # print(old_reflection)
    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            new_pattern = _flip_cell(pattern, r, c)
            # try horizontal reflection first
            new_reflection = _get_reflection(new_pattern, old_reflection, 100) * 100
            if not new_reflection:  # try vertical if horizontal failed
                new_reflection = _get_reflection(list(zip(*new_pattern)), old_reflection)
            if new_reflection and new_reflection != old_reflection:
                # print(new_reflection)
                return new_reflection
    return None


def summarize(patterns: list[list[list[str]]]) -> list[int]:
    reflections = []

    for i, pattern in enumerate(patterns, 1):
        if reflection := _find_new_reflection(pattern):
            reflections.append(reflection)
        else:
            print(f'no reflection found for pattern {i}/{len(patterns)}')

        # print()

    return reflections


test_data = """
#..#..#....##....
.##.#..####..#...
.##.##.####..#...
#..#..#....##....
#..#..####.##....
####..##..###..##
.##.#.#...####.##
#..######.##...##
####.####..##..##
.##..####.#.#.#.#
#..#..#######.#.#
#..##...#.#.#.#..
.....#.##.....##.
""".strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    patterns = get_patterns(data_lines)
    # pprint(patterns)

    summary = summarize(patterns)
    # print(summary)

    print(f'End result: {sum(summary)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 400
    #   Finished 'main' in 2 milliseconds
    # using input data:
    #   End result: 33106
    #   Finished 'main' in 337 milliseconds

    # patterns = get_patterns(data_lines)

    # test _flip_smudge
    # pattern = [['.', '.', '.', ], ['.', '#', '.', ], ['.', '.', '.', ], ]
    # pprint(pattern)
    # for r in range(len(pattern)):
    #     for c in range(len(pattern[r])):
    #         pprint(_flip_smudge(pattern, r, c))

    # print(_get_reflection(list(zip(*patterns[0]))))
    # print(_get_reflection(_flip_smudge(patterns[0], 1, 5), 2, 100))

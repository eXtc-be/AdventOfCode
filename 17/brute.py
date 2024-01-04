# Python program using brute force
# to find the shortest path between 2 points in a weighed graph


from aoc_2023_17_A_1 import (
    create_grid,
    _good_streak,
    draw_grid,
)

from tools import time_it


def get_all_paths(path, start: tuple[int, int], end: tuple[int, int]) -> None:
    global grid, combos

    if start == end:
        path.append(start)
        # print(', '.join(str(grid[node[0]][node[1]]) for node in path))
        combos.append([node for node in path])
        path.pop()

    # not necessary as we do the same boundary checks below
    # if 0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[start[0]]):
    #     return

    path.append(start)

    if start[1] + 1 < len(grid[start[0]]):
    # if start[1] + 1 < len(grid[start[0]]) and _good_streak(path):
        get_all_paths(path, (start[0], start[1] + 1), end)

    if start[0] + 1 < len(grid):
    # if start[0] + 1 < len(grid) and _good_streak(path):
        get_all_paths(path, (start[0] + 1, start[1]), end)

    path.pop()


# test_data = '''
# 12
# 34
# '''.strip().splitlines()

# test_data = '''
# 1234
# 5678
# 9012
# '''.strip().splitlines()

test_data = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''.strip().splitlines()


@time_it
def main():
    get_all_paths(path, (0, 0), (len(grid) - 1, len(grid[len(grid) - 1]) - 1))
    combos.sort(key=lambda combo: sum(grid[node[0]][node[1]] for node in combo[1:]))
    print(
        '\n'.join(
            ', '.join(
                f'{node} [{grid[node[0]][node[1]]}]'
                for node in combo
            ) + ' -> ' + str(sum(grid[node[0]][node[1]] for node in combo[1:]))
            for combo in combos[:10]
        )
    )
    # print('\n'.join(', '.join(str(grid[node[0]][node[1]]) for node in combo) + ' -> ' + str(sum(grid[node[0]][node[1]] for node in combo)) for combo in combos[:50]))
    for combo in combos[:10]:
        draw_grid(grid, path=combo)


if __name__ == "__main__":
    data_lines = test_data
    grid = create_grid(data_lines)
    path = []
    combos = []
    main()

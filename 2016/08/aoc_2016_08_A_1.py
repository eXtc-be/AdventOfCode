# aoc_2016_08_A_1.py - Day 8: Two-Factor Authentication - part 1
# After you swipe your card, if the screen did work, how many pixels should be lit?
# aoc_2016_08_A_1.py - Day 8: Two-Factor Authentication - part 2
# After you swipe your card, what code is the screen trying to display?
# https://adventofcode.com/2016/day/8


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


@dataclass
class Instruction:
    def execute(self, screen: list[list[str]]):  # virtual method
        raise NotImplementedError


@dataclass
class Rect(Instruction):
    cols: int
    rows: int

    def execute(self, screen: list[list[str]]):
        if not 0 <= self.rows <= len(screen):
            raise ValueError(f'not a valid value for rows: {self.rows}')
        if not 0 <= self.cols <= len(screen[0]):
            raise ValueError(f'not a valid value for columns: {self.cols}')

        for row in range(self.rows):
            for col in range(self.cols):
                screen[row][col] = ON


@dataclass
class Rotate(Instruction):
    n: int


@dataclass
class RotateColumn(Rotate):
    x: int

    def execute(self, screen: list[list[str]]):  # virtual method
        if not 0 <= self.x <= len(screen[0]):
            raise ValueError(f'not a valid value for x: {self.x}')

        for _ in range(self.n):
            last = screen[-1][self.x]  # remember value in last row
            for row in range(len(screen)-1, 0, -1):
                screen[row][self.x] = screen[row-1][self.x]
            screen[0][self.x] = last  # put remembered value in first row



@dataclass
class RotateRow(Rotate):
    y: int

    def execute(self, screen: list[list[str]]):  # virtual method
        if not 0 <= self.y <= len(screen):
            raise ValueError(f'not a valid value for y: {self.y}')

        for _ in range(self.n):
            last = screen[self.y][-1]  # remember value in last column
            for col in range(len(screen[0])-1, 0, -1):
                screen[self.y][col] = screen[self.y][col-1]
            screen[self.y][0] = last  # put remembered value in first column


DATA_PATH = './input_2016_08'

OFF = '.'
ON = '#'

ACTUAL_SCREEN = [[OFF] * 50 for _ in range(6)]  # "[[OFF] * 50] * 6" creates 6 shallow copies of "[OFF] * 50"
TEST_SCREEN = [[OFF] * 7 for _ in range(3)]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def print_screen(screen: list[list[str]]) -> None:
    print('\n'.join(''.join(c for c in line) for line in screen))
    print('-' * 100)


def get_instructions(data_lines: list[str]) -> list[Instruction]:
    instructions = []

    for line in data_lines:
        verb, *args = line.split()

        match verb:
            case 'rect':
                if 'x' not in args[0]:
                    raise ValueError(f'not a valid command: {line}')
                instructions.append(Rect(*(int(arg) for arg in args[0].split('x'))))
            case 'rotate':
                if args[2] != 'by':
                    raise ValueError(f'not a valid command: {line}')
                match args[0]:
                    case 'column':
                        if 'x' not in args[1] or '=' not in args[1]:
                            raise ValueError(f'not a valid command: {line}')
                        instructions.append(RotateColumn(int(args[3]), int(args[1].split('=')[1])))
                    case 'row':
                        if 'y' not in args[1] or '=' not in args[1]:
                            raise ValueError(f'not a valid command: {line}')
                        instructions.append(RotateRow(int(args[3]), int(args[1].split('=')[1])))
                    case _:
                        raise ValueError(f'not a valid command: {line}')
            case _:
                raise ValueError(f'not a valid command: {line}')

    return instructions


# test_data = '''
# rect 1x1
# rotate column x=0 by 1
# rotate column x=0 by 1
# rotate column x=0 by 1
# rotate column x=0 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# rotate row y=1 by 1
# '''.strip().splitlines()

# test_data = '''
# rect 7x2
# rect 2x3
# rect 7x3
# '''.strip().splitlines()

test_data = '''
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], screen: list[list[str]]) -> None:
    # print_screen(screen)

    instructions = get_instructions(data_lines)
    # print(instructions)

    for instruction in instructions:
        # print(instruction)
        instruction.execute(screen)
        # print_screen(screen)

    print_screen(screen)

    print(f'End result: {sum(sum(c==ON for c in line) for line in screen)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, ACTUAL_SCREEN)
    # using test_data:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 116 - UPOJFLBCEZ
    #   Finished 'main' in 3 milliseconds

    # print_screen(SCREEN)

    # test all the classes
    # instruction = Instruction()
    # print(instruction)
    # rect = Rect(3, 2)
    # print(rect)
    # # rect.execute()
    # rot_c = RotateColumn(1, 2)
    # print(rot_c)
    # rot_r = RotateRow(3, 2)
    # print(rot_r)

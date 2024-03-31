# aoc_2018_15_A_extern_1.py - Day 15: Beverage Bandits - part 1
# What is the outcome of the combat described in your puzzle input?
# https://adventofcode.com/2018/day/15
# based on the solution by reddit user daggerdragon (extern_2.py)
# (https://old.reddit.com/r/adventofcode/comments/a6chwa/2018_day_15_solutions/ebtwcqr/)
# This version also didn't find the correct answer, but it got a correct answer for some other inputs I found

import sys
sys.path.extend(['..', '../..'])

from tools import time_it

from aoc_2018_15_A_1 import (
    DATA_PATH,
    load_data,
    test_data_A, test_data_B, test_data_C, test_data_D, test_data_E, test_data_F,
    clear,
)

from pprint import pprint

from typing import NamedTuple
from dataclasses import dataclass
import enum
import collections
import os


BOLD = '\033[1m'
ENDC = '\033[0m'


class Point(NamedTuple('Point', [('r', int), ('c', int)])):
    def __add__(self, other):
        return type(self)(self.r + other.r, self.c + other.c)

    @property
    def neighbours(self):
        return [self + d for d in [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]]


class Type(enum.Enum):
    EMPTY = '.'
    WALL = '#'
    ELF = 'E'
    GOBLIN = 'G'
    DEAD = 'X'


TEAMS = (Type.ELF, Type.GOBLIN)


@dataclass
class Unit:
    type: Type
    hit_points: int = 200
    attack_power: int = 3
    alive: bool = True
    selected: bool = False

    def __str__(self) -> str:
        return (f'{BOLD if self.selected else ""}'
                f'{self.type.value if self.type not in TEAMS or self.alive else Type.DEAD.value}'
                f'{ENDC}')


class ElfDied(Exception):
    pass


class Grid(dict):
    def __init__(self, lines: list[str], elf_attack_power: int = 3):
        super().__init__()

        self.rows = len(lines)
        self.cols = max(len(line) for line in lines)
        self.rounds = 0

        for r, line in enumerate(lines):
            for c, el in enumerate(line):
                self[Point(r, c)] = Unit(
                        type={
                            Type.EMPTY.value: Type.EMPTY,
                            Type.WALL.value: Type.WALL,
                            Type.ELF.value: Type.ELF,
                            Type.GOBLIN.value: Type.GOBLIN
                        }[el],
                        attack_power={
                            Type.EMPTY.value: 0,
                            Type.WALL.value: 0,
                            Type.ELF.value: elf_attack_power,
                            Type.GOBLIN.value: 3
                        }[el],
                        hit_points={
                            Type.EMPTY.value: 0,
                            Type.WALL.value: 0,
                            Type.ELF.value: 200,
                            Type.GOBLIN.value: 200
                        }[el],
                        alive={
                            Type.EMPTY.value: False,
                            Type.WALL.value: False,
                            Type.ELF.value: True,
                            Type.GOBLIN.value: True
                        }[el],
                        # alive={
                        #     Type.EMPTY.value: True,
                        #     Type.WALL.value: True,
                        #     Type.ELF.value: True,
                        #     Type.GOBLIN.value: True
                        # }[el],
                    )

    # def __str__(self) -> str:
    #     return '\n'.join(
    #         ''.join([str(v) for k, v in self.items() if k.r == r])
    #         for r in range(self.rows)
    #     ) + '\n' + '\n'.join(
    #         f'{v.type.value} {v.hit_points} {k.r},{k.c}'
    #         for r in range(self.rows)
    #         for k, v in self.items() if k.r == r and v.type in TEAMS
    #     ) + '\n' + str(self.rounds) + '\n'

    def __str__(self) -> str:
        return '\n'.join(
            ''.join([str(v) for k, v in self.items() if k.r == r]) +
            ' ' +
            ','.join(f'{v.type.value}{v.hit_points}' for k, v in self.items() if k.r == r and v.type in TEAMS)
            for r in range(self.rows)
        )

    def play(
            self,
            no_elf_losses=False,
            verbose: bool = False,
            confirm_next_round: bool = False,
            confirm_next_step: bool = False
    ) -> tuple[Type, int, int]:
        winner_type = None
        while True:
            if verbose:
                clear()
                print(f'Round {self.rounds}')
                print(self)
                if confirm_next_round and not confirm_next_step:
                    input('Press Enter to continue...')
            if winner_type := self.round(no_elf_losses, confirm_next_round and confirm_next_step):
                break
            self.rounds += 1

        if verbose:
            clear()
            print(f'Round {self.rounds}')
            print(self)

        return winner_type, self.rounds, sum(unit.hit_points for unit in self.values() if unit.type is winner_type and unit.alive)

    def _cleanup(self) -> None:
        # reset selected and remove dead units
        for position in [pos for pos in self.keys() if self[pos].type in TEAMS]:
            self[position].selected = False
            if not self[position].alive:
                self[position] = Unit(Type.EMPTY, 0, True)

    def round(self, no_elf_losses: bool = False, confirm_next_step: bool = False) -> Type | None:
        for position in sorted(pos for pos in self.keys() if self[pos].type in TEAMS):
            if self[position].selected:  # unit already did a turn, but moved into a position that isn't treated yet
                continue
            self[position].selected = True
            if self[position].alive:
                if self.move(position, no_elf_losses, confirm_next_step):
                    self._cleanup()
                    return self[position].type

        self._cleanup()
        return None

    def move(self, unit_position: Point, no_elf_losses: bool = False, confirm_next_step: bool = False) -> bool:
        enemy_positions = [
            pos for pos in self.keys()
            if self[pos].alive and self[pos].type in TEAMS and self[pos].type != self[unit_position].type
        ]

        if not enemy_positions:
            return True  # no more enemies left means battle is over

        adjacent_positions = set(
            point for target_position in enemy_positions for point in target_position.neighbours
            if not self[point].alive or self[point].type == Type.EMPTY or point == unit_position
        )

        if unit_position not in adjacent_positions:
            if new_position := self.find_move(unit_position, adjacent_positions):
                self[new_position], self[unit_position] = self[unit_position], self[new_position]
                unit_position = new_position

        opponent_positions = [enemy_pos for enemy_pos in enemy_positions if enemy_pos in unit_position.neighbours]

        if opponent_positions:
            target_position = min(
                opponent_positions,
                key=lambda opponent_position: (self[opponent_position].hit_points, opponent_position)
            )

            self[target_position].hit_points -= self[unit_position].attack_power

            if self[target_position].hit_points <= 0:
                self[target_position].alive = False
                if no_elf_losses and self[target_position].type == Type.ELF:
                    raise ElfDied()

        if confirm_next_step:
            input('Press Enter to continue...')
            clear()
            # print(f'Round {self.rounds}')
            print(self)

        return False  # battle not over yet

    def find_move(self, unit_position, adjacent_positions):
        visiting = collections.deque([(unit_position, 0)])
        meta = {unit_position: (0, None)}
        seen = set()
        free = {
            unit_position for unit_position in self.keys()
            if self[unit_position].type == Type.EMPTY or
               self[unit_position].type in TEAMS and not self[unit_position].alive  # dead units
        }

        while visiting:
            pos, dist = visiting.popleft()
            for neighbour in pos.neighbours:
                if neighbour not in free or neighbour in seen:
                    continue
                if neighbour not in meta or meta[neighbour] > (dist + 1, pos):
                    meta[neighbour] = (dist + 1, pos)
                if not any(neighbour == visit[0] for visit in visiting):
                    visiting.append((neighbour, dist + 1))
            seen.add(pos)

        try:
            min_dist, closest = min(
                (dist, pos)
                for pos, (dist, parent) in meta.items()
                if pos in adjacent_positions
            )
        except ValueError:
            return

        while meta[closest][0] > 1:
            closest = meta[closest][1]

        return closest


@time_it
def main(
        data_lines: list[str],
        verbose: bool = False,
        confirm_next_round: bool = False,
        confirm_next_step: bool = False,
        elf_start_attack_power: int = 4
) -> None:
    grid = Grid(data_lines)
    # print(grid)

    winner_type, rounds, hp_left = grid.play(False, verbose, confirm_next_round, confirm_next_step)

    # print(grid)

    clear()
    print(f'{"Elves" if winner_type == Type.ELF else "Goblins"} win '
          f'after {rounds} full rounds with {hp_left} hit points left. '
          f'Score: {rounds} * {hp_left} = {rounds * hp_left}')


if __name__ == "__main__":
    main(load_data(DATA_PATH), False)  # 81 * 2751 = 222831
    # main(load_data('input_2018_15_2'), False)  # 82 * 2459 = 201638
    # main(load_data('input_2018_15_3'), False)  # 103 * 2416 = 248848
    # main(load_data('input_2018_15_4'), False)  # 67 * 2922 = 195774
    # main(load_data('input_2018_15_5'), False)  # 76 * 2720 = 206720

    # main(test_data_B, verbose=True, confirm_next_round=False, confirm_next_step=False)

    # main(test_data_A, verbose=False, confirm_next_round=False)
    # main(test_data_B, verbose=False, confirm_next_round=False)
    # main(test_data_C, verbose=False, confirm_next_round=False)
    # main(test_data_D, verbose=False, confirm_next_round=False)
    # main(test_data_E, verbose=False, confirm_next_round=False)
    # main(test_data_F, verbose=False, confirm_next_round=False)

    # using test_data_A:
    #   End result: Goblins win after 47 full rounds with 590 hit points left. Score: 47 * 590 = 27730
    #   Finished 'main' in 14 milliseconds
    # using test_data_B:
    #   End result: Elves win after 37 full rounds with 982 hit points left. Score: 37 * 982 = 36334
    #   Finished 'main' in 16 milliseconds
    # using test_data_C:
    #   End result: Elves win after 46 full rounds with 859 hit points left. Score: 46 * 859 = 39514
    #   Finished 'main' in 18 milliseconds
    # using test_data_D:
    #   End result: Goblins win after 35 full rounds with 793 hit points left. Score: 35 * 793 = 27755
    #   Finished 'main' in 11 milliseconds
    # using test_data_E:
    #   End result: Goblins win after 54 full rounds with 536 hit points left. Score: 54 * 536 = 28944
    #   Finished 'main' in 15 milliseconds
    # using test_data_F:
    #   End result: Goblins win after 20 full rounds with 937 hit points left. Score: 20 * 937 = 18740
    #   Finished 'main' in 13 milliseconds
    # using input data:
    #   End result: Goblins win after 80 full rounds with 2754 hit points left. Score: 80 * 2754 = 220320 ???
    #   Finished 'main' in 3.4 seconds

from typing import NamedTuple
from dataclasses import dataclass
import enum
import itertools
import collections
import os


class Pt(NamedTuple('Pt', [('x', int), ('y', int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    @property
    def nb4(self):
        return [self + d for d in [Pt(0, 1), Pt(1, 0), Pt(0, -1), Pt(-1, 0)]]


class Team(enum.Enum):
    ELF = 'E'
    GOBLIN = 'G'

DEAD = 'X'

TEAMS = (Team.ELF, Team.GOBLIN)
BOLD = '\033[1m'
ENDC = '\033[0m'


@dataclass
class Unit:
    team: Team
    position: Pt
    hp: int = 200
    alive: bool = True
    power: int = 3
    selected: bool = False

    def __str__(self) -> str:
        return (f'{BOLD if self.selected and not LOGGING else ""}'
                f'{self.team.value if self.team not in TEAMS or self.alive else DEAD}'
                f'{ENDC if not LOGGING else ""}')


class ElfDied(Exception):
    pass


class Grid(dict):
    def __init__(self, lines, power=3):
        super().__init__()

        self.units = []
        self.rows = len(lines)

        teams = [v.value for v in Team]

        for i, line in enumerate(lines):
            for j, el in enumerate(line.strip()):
                self[Pt(i, j)] = el == '#'

                if el in teams:
                    self.units.append(Unit(
                        team={Team.ELF.value: Team.ELF, Team.GOBLIN.value: Team.GOBLIN}[el],
                        position=Pt(i, j),
                        power={Team.ELF.value: power, Team.GOBLIN.value: 3}[el]
                    ))

    def __str__(self) -> str:
        rows = []
        teams = [v for v in Team]
        for r in range(self.rows):
            row = ''
            stats = []
            for c, el in enumerate([v for k, v in self.items() if k.x == r]):
                if el:
                    row += '#'
                else:
                    units = [u for u in self.units if u.position == Pt(r, c)]
                    if units and units[0].team in teams:
                        row += str(units[0])
                        stats.append(str(units[0]) + str(units[0].hp))
                    else:
                        row += '.'
            rows.append(row + ' ' + ','.join(stats))
        return '\n'.join(rows)

    def play(self, elf_death=False):
        self.rounds = 0

        while True:
            if VERBOSE or LOGGING:
                clear()
                print(f'Round {self.rounds}')
                print(self)
                if CONFIRM_ROUND and not CONFIRM_STEP and not LOGGING:
                    input('Press Enter to continue...')

            if self.round(elf_death=elf_death):
                break
            self.rounds += 1
        return self.rounds, sum(unit.hp for unit in self.units if unit.alive)

    def round(self, elf_death=False):
        for unit in sorted(self.units, key=lambda unit: unit.position):
            unit.selected = True
            if unit.alive:
                if self.move(unit, elf_death=elf_death):
                    return True

        self.units = [unit for unit in self.units if unit.alive]  # remove dead units

        for unit in self.units:  # reset selected status
            unit.selected = False

    def move(self, unit, elf_death=False):
        targets = [target for target in self.units if unit.team != target.team and target.alive]
        occupied = set(u2.position for u2 in self.units if u2.alive and unit != u2)

        if not targets:
            return True

        in_range = set(pt for target in targets for pt in target.position.nb4 if not self[pt] and pt not in occupied)

        if not unit.position in in_range:
            move = self.find_move(unit.position, in_range)

            if move:
                unit.position = move

        opponents = [target for target in targets if target.position in unit.position.nb4]

        if opponents:
            target = min(opponents, key=lambda unit: (unit.hp, unit.position))

            target.hp -= unit.power

            if target.hp <= 0:
                target.alive = False
                if elf_death and target.team == Team.ELF:
                    raise ElfDied()

        if CONFIRM_STEP and not LOGGING:
            input('Press Enter to continue...')
            clear()
            print(f'Round {self.rounds:3}')
            print(self)

    def find_move(self, position, targets):
        visiting = collections.deque([(position, 0)])
        meta = {position: (0, None)}
        seen = set()
        occupied = {unit.position for unit in self.units if unit.alive}

        while visiting:
            pos, dist = visiting.popleft()
            for nb in pos.nb4:
                if self[nb] or nb in occupied:
                    continue
                if nb not in meta or meta[nb] > (dist + 1, pos):
                    meta[nb] = (dist + 1, pos)
                if nb in seen:
                    continue
                if not any(nb == visit[0] for visit in visiting):
                    visiting.append((nb, dist + 1))
            seen.add(pos)

        try:
            min_dist, closest = min((dist, pos) for pos, (dist, parent) in meta.items() if pos in targets)
        except ValueError:
            return

        while meta[closest][0] > 1:
            closest = meta[closest][1]

        return closest


VERBOSE = False
CONFIRM_ROUND = False
CONFIRM_STEP = False
LOGGING = False


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear') if not os.environ.get('CHARM') and not LOGGING else print('-' * 100)


if __name__ == "__main__":
    # lines = '''
    # #######
    # #.G...#
    # #...EG#
    # #.#.#G#
    # #..G#E#
    # #.....#
    # #######
    # '''.strip().splitlines()
    lines = open('input_2018_15').read().splitlines()  # 81 * 2751 = 222831
    # lines = open('input_2018_15_2').read().splitlines()  # 82 * 2459 = 201638
    # lines = open('input_2018_15_3').read().splitlines()  # 103 * 2416 = 248848
    # lines = open('input_2018_15_4').read().splitlines()  # 67 * 2922 = 195774
    # lines = open('input_2018_15_5').read().splitlines()  # 76 * 2720 = 206720

    grid = Grid(lines)
    # print(grid)

    rounds, hp = grid.play()

    clear()
    print(f'part 1: {rounds} * {hp} = {rounds * hp}')

    # for power in itertools.count(4):
    #     try:
    #         outcome = Grid(lines, power).play(elf_death=True)
    #     except ElfDied:
    #         continue
    #     else:
    #         print('part 2:', outcome)
    #         break

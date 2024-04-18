# aoc_2018_24_A_1.py - Day 24: Immune System Simulator 20XX - part 1
# As it stands now, how many units would the winning army have?
# https://adventofcode.com/2018/day/24


from tools import time_it, evalPlural

from dataclasses import dataclass, field
from enum import Enum, auto
import re

from pprint import pprint


DATA_PATH = './input_2018_24'

UNITS_HP = re.compile(r'^(?P<units>\d+) units each with (?P<hp>\d+) hit points.*$')
DMG_INIT = re.compile(r'^.*with an attack that does (?P<d_num>\d+) (?P<d_typ>[a-z]+) damage at initiative (?P<init>\d+)$')


class Damage(Enum):
    slashing = auto()
    bludgeoning = auto()
    radiation = auto()
    fire = auto()
    cold = auto()


DAMAGE = {
    'slashing': Damage.slashing,
    'bludgeoning': Damage.bludgeoning,
    'radiation': Damage.radiation,
    'fire': Damage.fire,
    'cold': Damage.cold,
}


@dataclass
class Attack:
    type: Damage
    amount: int


@dataclass
class Group:
    id: int
    team: str
    units: int
    hit_points: int
    attack: Attack
    initiative: int
    immunities: list[Damage] = field(default_factory=list)
    weaknesses: list[Damage] = field(default_factory=list)
    selected: bool = False

    @property
    def power(self) -> int:
        return self.attack.amount * self.units

    def damage_dealt_to(self, other):
        """returns the damage that would be dealt by attacker on defender"""
        if self.attack.type in other.immunities:
            return 0
        elif self.attack.type in other.weaknesses:
            return self.power * 2
        else:
            return self.power

    def __hash__(self) -> int:
        return hash(self.team + str(self.id))

    def __str__(self) -> str:
        return (f'{self.team} '
                f'{self.units:5,} * {self.attack.amount:5,} = {self.power:10,} '
                f' (I{self.initiative:02})')


@dataclass
class Army:
    team: str
    groups: list[Group] = field(default_factory=list)


@dataclass
class Battle:
    armies: list[Army] = field(default_factory=list)

    @property
    def groups(self) -> list[Group]:
        """returns a list of all the groups in all the armies"""
        return [group for army in self.armies for group in army.groups]

    def _group_index(self, group: Group) -> int:
        """returns the index of the group in its army"""
        return [army for army in self.armies if army.team == group.team][0].groups.index(group) + 1

    def _stats(self) -> None:
        """prints out information about the armies and its groups"""
        for army in self.armies:
            print(f'{army.team.capitalize()}:')
            if any(group.units > 0 for group in army.groups):
                for group in army.groups:
                    if group.units > 0:
                        print(f'\tGroup {self._group_index(group)} contains {"%d unit%s" % evalPlural(group.units)}')
            else:
                print('\tNo groups remain.')
        print()

    @staticmethod
    def _calc_damage(attacker: Group, defender: Group) -> int:
        """returns the damage that would be dealt by attacker on defender"""
        if attacker.attack.type in defender.immunities:
            return 0
        elif attacker.attack.type in defender.weaknesses:
            return attacker.power * 2
        else:
            return attacker.power

    def _do_turn(self, verbose: bool = False) -> int:
        """do one round of battle - returns the number of units killed"""
        fights = {}
        units_killed = 0

        if verbose:
            self._stats()
        # self._stats()
        # print('-' * 100)

        # target selection phase
        # attackers may pick a target in order of their power and initiative, highest to lowest
        for attacker in sorted(
                [group for group in self.groups if group.units > 0],
                key=lambda x: (x.power, x.initiative),
                reverse=True
        ):
            # choosing a target in order of damage dealt, power and initiative, highest to lowest
            defenders = sorted(
                [
                    defender for defender in self.groups
                    # select groups from opposing team with units left,
                    # that can do damage, and not yet selected for battle
                    if defender.team != attacker.team and
                       defender.units > 0
                       and attacker.damage_dealt_to(defender) > 0
                       and not defender.selected
                ],
                key=lambda x: (self._calc_damage(attacker, x), x.power, x.initiative),
                reverse=True
            )

            if defenders:
                if verbose:
                    for defender in defenders:
                        print(f'{attacker.team.capitalize()} group {self._group_index(attacker)} would deal '
                              f'{defender.team.capitalize()} group {self._group_index(defender)} '
                              f'{attacker.damage_dealt_to(defender)} damage')
                    print()

                defender = defenders[0]  # pick the first target in the list
                fights[attacker] = defender
                defender.selected = True
            else:
                if verbose:
                    print(f'There are no groups left for {attacker.team.capitalize()} group {self._group_index(attacker)} to attack.')
                    print()

        # attack phase
        # attackers attack in order of initiative, highest to lowest
        for attacker in sorted(
                [group for group in self.groups if group.units > 0],
                key=lambda x: x.initiative,
                reverse=True
        ):
            if attacker.units > 0:  # check for units here instead of at start of loop in case units were lost in battle
                if attacker in fights:
                    defender = fights[attacker]
                    damage = attacker.damage_dealt_to(defender)  # recalculate damage with current units

                    if verbose:
                        print(f'{attacker.team.capitalize()} group {self._group_index(attacker)} attacks '
                              f'{defender.team.capitalize()} group {self._group_index(defender)}, '
                              f'dealing {damage} damage, '
                              f'killing {"%d unit%s" % evalPlural(min(defender.units, damage // defender.hit_points))}')

                    defender.units -= damage // defender.hit_points  # only kill whole units
                    units_killed += damage // defender.hit_points

        # # remove all groups with zero or fewer units left
        # for army in self.armies:
        #     army.groups = [group for group in army.groups if group.units > 0]

        # reset defending status for all groups
        for group in self.groups:
            group.selected = False

        return units_killed

    def do_battle(self, verbose: bool = False, confirm: bool = False) -> tuple[str, int]:
        loser = None
        turn = 0

        while not loser:
            turn += 1

            if verbose:
                print(f'Turn: {turn}')
                print('-' * 100)
            # print(f'Turn: {turn}')
            # print('-' * 100)

            units_killed = self._do_turn(verbose=verbose)

            if units_killed == 0:  # stalemate
                if verbose:
                    print(f'Battle reached a stalemate.')
                    print('-' * 100)
                return '', sum([group.units for group in self.groups if group.units > 0])

            for army in self.armies:
                if all(group.units <= 0 for group in army.groups):
                    loser = army.team
                    break

            if verbose:
                print('-' * 100)

            if confirm:
                input('Press enter to continue')
                print('-' * 100)

        if verbose:
            print(f'Battle completed in {turn} turns. {loser.capitalize()} team lost.')
            print('-' * 100)
            self._stats()

        return loser, sum([group.units for group in self.groups if group.team != loser and group.units > 0])


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_units(data_lines: list[str], boost: int = 0) -> tuple[Army, Army]:
    immune, infection = Army('immune'), Army('infection')
    current = None
    counter = 0
    booster = 0

    for line in data_lines:
        if line == '':
            continue
        elif line == 'Immune System:':
            current = immune
            booster = boost
        elif line == 'Infection:':
            current = infection
            booster = 0
        else:
            # initialize/declare variables
            units, hp, d_num, d_typ, init, immunities, weaknesses = 0, 0, 0, '', 0, [], []

            # interpret unit stats - number of units, hit points
            if match := UNITS_HP.match(line):
                units = int(match.group('units'))
                hp = int(match.group('hp'))

            # interpret unit stats - attack strength and type, initiative
            if match := DMG_INIT.match(line):
                d_num = int(match.group('d_num')) + booster
                d_typ = DAMAGE[match.group('d_typ')]
                init = int(match.group('init'))

            # interpret unit stats - immunities, weaknesses
            if '(' in line and ')' in line:
                traits = line[line.index('(')+1:line.index(')')].split('; ')
                for trait in traits:
                    if trait.startswith('immune to '):
                        immunities = [DAMAGE[el] for el in trait[10:].split(', ')]
                    if trait.startswith('weak to '):
                        weaknesses = [DAMAGE[el] for el in trait[8:].split(', ')]

            # add group to current army
            current.groups.append(Group(counter, current.team, units, hp, Attack(d_typ, d_num), init, immunities, weaknesses))

            counter += 1

    return immune, infection


test_data = '''
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], verbose: bool = False, confirm: bool = False) -> None:
    immune, infection = get_units(data_lines)
    # pprint(immune)
    # pprint(infection)

    battle = Battle([immune, infection])
    # battle._do_turn(verbose)
    loser, units_left = battle.do_battle(verbose=verbose, confirm=confirm)

    print(f'End result: {units_left}')


if __name__ == "__main__":
    main(load_data(DATA_PATH), verbose=False)
    # main(test_data, verbose=True, confirm=False)

    # using test_data:
    #   End result: 5216
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 9878
    #   Finished 'main' in 49 milliseconds

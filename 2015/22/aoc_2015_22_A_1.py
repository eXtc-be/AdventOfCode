# aoc_2015_22_A_1.py - Day 22: Wizard Simulator 20XX - part 1
# What is the least amount of mana you can spend and still win the fight?
# https://adventofcode.com/2015/day/22


import sys
sys.path.insert(0, '../..')

from tools import time_it

from dataclasses import dataclass, field
from itertools import cycle, product

from pprint import pprint


DATA_PATH = './input_2015_22'

SPELLS = {
    'Magic Missile': {'cost': 53, 'turns': 1, 'damage': 4, 'armor': 0, 'heal': 0, 'mana': 0},
    'Drain': {'cost': 73, 'turns': 1, 'damage': 2, 'armor': 0, 'heal': 2, 'mana': 0},
    'Shield': {'cost': 113, 'turns': 6, 'damage': 0, 'armor': 7, 'heal': 0, 'mana': 0},
    'Poison': {'cost': 173, 'turns': 6, 'damage': 3, 'armor': 0, 'heal': 0, 'mana': 0},
    'Recharge': {'cost': 229, 'turns': 5, 'damage': 0, 'armor': 0, 'heal': 0, 'mana': 101},
 }

MAX_TRIES = 10_000_000

MAX_SPELLS = 8

HARD_MODE = False


@dataclass
class BasePlayer:
    name: str
    hitpoints: int
    damage: int
    mana: int = 0

    def __post_init__(self):
        self.timers = {spell: 0 for spell in SPELLS}

    @property
    def armor(self):
        return SPELLS['Shield']['armor'] if self.timers['Shield'] else 0

    @property
    def stats(self):
        return f'- {self.name} has {self.hitpoints} health'

    def process_spells(self, opponent: 'BasePlayer', verbose: bool = False) -> bool:
        result = False

        for spell in self.timers:
            if self.timers[spell] > 0:
                self.timers[spell] -= 1

                if SPELLS[spell]['armor']:
                    # self.armor = SPELLS[spell]['armor']
                    if verbose:
                        print(f'> {spell}\'s timer is now {self.timers[spell]}')

                if SPELLS[spell]['mana']:
                    self.mana += SPELLS[spell]['mana']
                    if verbose:
                        print(f'> {spell} provides {SPELLS[spell]["mana"]} mana; its timer is now {self.timers[spell]}')

                if SPELLS[spell]['damage']:
                    result = opponent.defend(SPELLS[spell]['damage'])  # returns True if opponent is killed
                    if result:
                        if verbose:
                            print(f'> {spell} deals {SPELLS[spell]["damage"]} damage.')
                        break  # no need to continue to process spells, unless we really want to kill him
                    elif verbose and SPELLS[spell]['damage']:
                        print(f'> {spell} deals {SPELLS[spell]["damage"]} damage; its timer is now {self.timers[spell]}')
                if self.timers[spell] == 0:
                    if verbose:
                        print(f'> {spell} wears off.')

        return result

    def take_turn(
            self,
            spells: list[str],
            opponent: 'BasePlayer',
            hard_mode: bool = HARD_MODE,
            verbose: bool = False
    ) -> int:
        # return -1 if self loses, 1 if opponent loses, 0 otherwise

        if hard_mode:
            if self.__class__.__name__ == 'Player':
                self.hitpoints -= 1
                if verbose:
                    print(f'> {self.name} is bleeding, losing 1 health')
                if self.hitpoints <= 0:
                    if verbose:
                        print(f'\n*** {self.name} is killed, {opponent.name} wins ***\n')
                    return -1

        if self.process_spells(opponent, verbose):  # returns True if opponent is killed
            if verbose:
                print(f'\n*** {opponent.name} is killed, {self.name} wins ***\n')
            return 1

        if opponent.process_spells(self, verbose):  # returns True if self is killed
            if verbose:
                print(f'\n*** {self.name} is killed, {opponent.name} wins ***\n')
            return -1

        # returns 1 if opponent is killed, -1 if attacker is killed, 0 if none is killed
        if (result := self.attack(opponent, spells, verbose)) == 1:
            if verbose:
                print(f'\n*** {opponent.name} is killed, {self.name} wins ***\n')
        elif result == -1:
            if verbose:
                print(f'\n*** {self.name} loses, {opponent.name} wins ***\n')

        return result

    def attack(self, opponent: 'BasePlayer', spells: list[str], verbose: bool = False) -> bool:
        pass  # implemented in child classes

    def defend(self, damage=0) -> bool:
        self.hitpoints -= max(damage - self.armor, 1)  # damage dealt - own armor, at least 1
        return self.hitpoints <= 0


@ dataclass
class Player(BasePlayer):

    @property
    def stats(self):
        return f'{super().stats}, {self.armor} armor, {self.mana} mana'

    def attack(self, opponent: 'BasePlayer', spells: list[str], verbose: bool = False) -> int:
        opponent_dead = False

        spell = ''
        rejected = []
        while spells:  # find the next valid spell
            spell = spells.pop(0)  # get next spell from the start of the list
            # reject spell if we don't have enough mana, or if the spell is still active from previous turn
            if SPELLS[spell]['cost'] > self.mana or self.timers[spell] > 0:
                rejected.append(spell)  # add spell to rejected list
            else:
                break

        if spell and SPELLS[spell]['cost'] <= self.mana and self.timers[spell] == 0:  # we got a valid spell
            # spells.extend(rejected)  # re-add rejected spells to the end of the list

            self.mana -= SPELLS[spell]['cost']

            damage_string = ''
            if SPELLS[spell]['turns'] == 1:  # instant effect
                opponent_dead = opponent.defend(SPELLS[spell]['damage'])   # returns True if opponent is killed
                damage_string = f', dealing {SPELLS[spell]["damage"]} damage'
            else:  # setup timer for spell
                self.timers[spell] = SPELLS[spell]['turns']

            armor_string = ''
            if SPELLS[spell]['armor']:
                armor_string = f', increasing armor by {SPELLS[spell]["armor"]}'

            healing_string = ''
            if SPELLS[spell]['heal']:
                healing_string = f', healing {SPELLS[spell]["heal"]} hit points'
                self.hitpoints += SPELLS[spell]['heal']

            if verbose:
                print(f'# {self.name} casts {spell}{damage_string}{armor_string}{healing_string} #')
        else:
            # we exhausted all valid spells
            if verbose:
                print(f'{self.name} has no spells left to cast.')
            #  if you cannot afford to cast *any* spell, you lose
            return -1

        return 1 if opponent_dead else 0


@ dataclass
class Boss(BasePlayer):
    def attack(self, opponent: 'BasePlayer', spells: list[str], verbose: bool = False) -> int:
        damage_string = f'{self.damage}'
        if opponent.armor:
            damage_string = f'{self.damage} - {opponent.armor} = {self.damage - opponent.armor}'
            if self.damage - opponent.armor < 1:
                damage_string += ' => 1'

        if verbose:
            print(f'# {self.name} attacks for {damage_string} damage #')

        return 1 if opponent.defend(self.damage) else 0  # returns 1 if opponent is killed, else 0


@ dataclass
class Game:
    boss: Boss
    player: Player

    # def play(self, spells: list[str], max_turns, verbose: bool = False) -> tuple[Boss | Player | None, int]:
    def play(
            self,
            spells: list[str],
            hard_mode: bool = HARD_MODE,
            verbose: bool = False
    ) -> tuple[Boss | Player | None, int]:

        if verbose:
            print(f'Trying {spells}')
            print('=' * 100)

        attack = cycle([self.player, self.boss])
        defend = cycle([self.boss, self.player])

        turn = 0
        while True:
            turn += 1

            attacker = next(attack)
            defender = next(defend)

            if verbose:
                print(f'Turn {turn}: {attacker.name}')
                print(self.player.stats)
                print(self.boss.stats)
                print('-' * 100)

            # returns -1 if attacker loses, 1 if defender loses, 0 otherwise
            result = attacker.take_turn(spells, defender, hard_mode=hard_mode, verbose=verbose)

            if attacker.hitpoints <= 0:
                return defender, turn  # defender wins
            if defender.hitpoints <= 0:
                return attacker, turn  # attacker wins
            if result == -1:  # player has no spells left to cast
                return defender, turn  # attacker (player) loses

            # if turn >= max_turns:
            #     if verbose:
            #         print('Maximum turns reached.')
            #     return None, turn

            if not spells and all(timer == 0 for timer in self.player.timers.values()):
                if verbose:
                    print('\nCould not determine a winner.\n')
                return None, turn

            if verbose:
                print('+' * 100)


@dataclass
class State:
    spells: list[str] = field(default_factory=list)

    @property
    def mana_spent(self):
        return sum(SPELLS[spell]['cost'] for spell in self.spells)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_boss(data_lines: list[str], name: str) -> Boss:
    return Boss(
        name,
        int(data_lines[0].split(': ')[-1]),  # hitpoints
        int(data_lines[1].split(': ')[-1]),  # damage
    )


def get_player(data_lines: list[str], name: str) -> Player:
    return Player(
        name,
        int(data_lines[0].split(': ')[-1]),  # hitpoints
        0,                                   # damage
        int(data_lines[1].split(': ')[-1]),  # mana
    )


test_player = '''
Hit Points: 10
Mana: 250
'''.strip().splitlines()

actual_player = '''
Hit Points: 50
Mana: 500
'''.strip().splitlines()

test_boss1 = '''
Hit Points: 13
Damage: 8
'''.strip().splitlines()

test_boss2 = '''
Hit Points: 14
Damage: 8
'''.strip().splitlines()

spells1 = '''
Poison
Magic Missile
'''.strip().splitlines()

spells2 = '''
Recharge
Shield
Drain
Poison
Magic Missile
'''.strip().splitlines()

spells3 = '''
Recharge
Shield
Drain
Poison
Magic Missile
'''.strip().splitlines()


@time_it
def main(boss_data: list[str], player_data: list[str], verbose: int = 0) -> None:
    # initial list of states: every state starts with one of the SPELLS
    states = sorted([State([spell]) for spell in SPELLS], key=lambda s: s.mana_spent)

    # declare variables to be used outside the loop
    state = None
    boss = None
    player = None
    winner = None

    # initialize try counter
    tries = 0

    # determine width of tries string
    tries_width = len(f'{MAX_TRIES:,}')

    while states:
        tries += 1

        state = states.pop(0)  # get first (lowest cost) state from list
        player = get_player(player_data, 'Player')  # create a new player for this game
        boss = get_boss(boss_data, 'Boss')  # create a new boss for this game
        game = Game(boss, player)

        if verbose > 0 and tries % 1000 == 0:
            print(f'{tries:{tries_width},} / {MAX_TRIES:{tries_width},} {state.spells}', end=' -> ')

        winner, turns = game.play([spell for spell in state.spells], hard_mode=HARD_MODE, verbose=verbose > 1)

        if winner == player:
            print(f'{player.name} won in {turns} turns')
            break
        # elif winner is None:  # None -> not enough spells
        else:
            if verbose > 0 and tries % 1000 == 0:
                print(f'{boss.name} won in {turns} turns') if winner == boss else print(f'undecided in {turns} turns')

            # add spells to current state, except the last one used
            if len(state.spells) < MAX_SPELLS:
                states.extend(State(state.spells + [spell]) for spell in SPELLS)
                # states.extend(State(state.spells + [spell]) for spell in SPELLS if spell != state.spells[-1])
                states = sorted(states, key=lambda s: s.mana_spent)  # sort states by mana spent
            # states.extend(State(state.spells + [spell]) for spell in SPELLS if spell != state.spells[-1])
            # states = filter(lambda s: len(s.spells) <= MAX_SPELLS, states)  # remove states with too much spells
            # states = sorted(states, key=lambda s: s.mana_spent)  # sort states by mana spent

        if verbose > 1:
            print('=' * 100)

        if tries >= MAX_TRIES:
            break

    if verbose:
        print('=' * 100)

    if winner == player:
        print(f'\nEnd result: {state.mana_spent} - {", ".join(state.spells)}')
    else:
        print('\nDidn\'t find a solution.')


if __name__ == '__main__':
    player_data = actual_player
    # player_data = test_player
    boss_data = load_data(DATA_PATH)
    # boss_data = test_boss1
    # boss_data = test_boss2
    # spells = spells1
    # spells = spells2
    # spells = spells3
    # print(data_lines)

    main(boss_data, player_data, 1)
    # using test_data boss1:
    #   End result: 226 - Poison, Magic Missile
    #   Finished 'main' in 3 milliseconds
    # using test_data boss2:
    #   End result: 641 - Recharge, Shield, Drain, Poison, Magic Missile
    #   Finished 'main' in 1 second
    # using input data MAX_SPELLS = 5:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 1.06 seconds
    # using input data MAX_SPELLS = 6:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 23 seconds
    # using input data MAX_SPELLS = 7:
    #   End result: Didn't find a solution.
    #   Finished 'main' in 10 minutes and 7 seconds
    # using input data MAX_SPELLS = 8:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data MAX_SPELLS = 9:
    #   End result: 953 - Magic Missile, Poison, Recharge, Magic Missile, Shield, Poison, Magic Missile, Magic Missile, Magic Missile
    #   Finished 'main' in 23 hours, 33 minutes and 11 seconds

    # # test class Boss, Player
    # player = Player('Player', 100, 0, 250)
    # print(player.stats)
    # boss = Boss('Boss', 100, 8)
    # print(boss.stats)

    # # test class Game
    # player = get_player(player_data, 'Player')
    # boss = get_boss(boss_data, 'Boss')
    # # print(player.stats)
    # # print(boss.stats)
    # game = Game(boss, player)
    # winner = game.play(spells, verbose=True)
    # print('=' * 100)
    # print(f'Winner: {winner}')

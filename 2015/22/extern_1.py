#!/usr/bin/python


from tools import time_it


HARD_MODE = True

class State(object):
    def __init__(self):
        self.hp = 50  # input data
        # self.hp = 10  # test data
        self.defense = 0
        self.boss_hp = 55  # input data
        # self.boss_hp = 13  # test data 1
        # self.boss_hp = 14  # test data 2

        self.effects = []

        self.mana = 500  # input data
        # self.mana = 250  # test data

        self.mana_spent = 0

        self.prev = None
        self.action = 'initial'

    def duplicate(self):
        other = State()

        other.hp = self.hp
        other.defense = 0  # effects will rebuild it
        other.boss_hp = self.boss_hp

        other.effects = self.effects[:]

        other.mana = self.mana

        other.mana_spent = self.mana_spent

        other.prev = self

        other.action = 'copy'

        return other

    def do_effects(self):
        new_effects = []
        for time, effect, name in self.effects:
            if time > 1:
                new_effects.append((time-1, effect, name))
            effect(self)

        self.effects = new_effects

    def boss_attack(self):
        other = self.duplicate()
        other.action = 'boss attack'

        other.do_effects()
        if other.boss_hp <= 0:
            return other

        other.hp -= max((8 - other.defense), 1)

        return other

    def magic_missile(self):
        other = self.duplicate()
        other.action = 'magic missile'

        if HARD_MODE:
            other.hp -= 1
            if other.hp <= 0:
                return None

        other.do_effects()
        if other.boss_hp <= 0:
            return other

        other.boss_hp -= 4

        other.mana -= 53

        other.mana_spent += 53

        if other.mana < 0:
            return None

        return other

    def drain(self):
        other = self.duplicate()
        other.action = 'drain'

        if HARD_MODE:
            other.hp -= 1
            if other.hp <= 0:
                return None

        other.do_effects()
        if other.boss_hp <= 0:
            return other

        other.hp += 2

        other.boss_hp -= 2

        other.mana -= 73

        other.mana_spent += 73

        if other.mana < 0:
            return None

        return other

    def shield(self):
        def effect(self):
            self.defense += 7

        other = self.duplicate()
        other.action = 'shield'

        if HARD_MODE:
            other.hp -= 1
            if other.hp <= 0:
                return None

        other.do_effects()
        if other.boss_hp <= 0:
            return other

        if 'shield' in [eff for (_, _, eff) in other.effects]:
            return None  # previous shield spell still active

        other.effects.append((6, effect, 'shield'))

        other.mana -= 113

        other.mana_spent += 113

        if other.mana < 0:
            return None

        return other

    def poison(self):
        def effect(self):
            self.boss_hp -= 3

        other = self.duplicate()
        other.action = 'poison'

        if HARD_MODE:
            other.hp -= 1
            if other.hp <= 0:
                return None

        other.do_effects()
        if other.boss_hp <= 0:
            return other

        if 'poison' in [eff for (_, _, eff) in other.effects]:
            return None  # previous poison spell still active

        other.effects.append((6, effect, 'poison'))

        other.mana -= 173

        other.mana_spent += 173

        if other.mana < 0:
            return None

        return other

    def recharge(self):
        def effect(self):
            self.mana += 101

        other = self.duplicate()
        other.action = 'recharge'

        if HARD_MODE:
            other.hp -= 1
            if other.hp <= 0:
                return None

        other.do_effects()
        if other.boss_hp <= 0:
            return other

        if 'recharge' in [eff for (_, _, eff) in other.effects]:
            return None  # previous recharge spell still active

        other.effects.append((5, effect, 'recharge'))

        other.mana -= 229

        other.mana_spent += 229

        if other.mana < 0:
            return None

        return other


@time_it
def main():
    min_successful = State()
    min_successful.mana_spent = 1_000_000

    states = [State()]

    run_effects = [
        lambda s: s.magic_missile(),
        lambda s: s.drain(),
        lambda s: s.shield(),
        lambda s: s.poison(),
        lambda s: s.recharge()
    ]

    while states:
        new_states = []

        print(f'{len(states)} state(s) left to process')
        print(f'mana spent: {min(s.mana_spent for s in states)} - {max(s.mana_spent for s in states)}')

        # player's turn
        for state in states:
            for eff in run_effects:
                tmp = eff(state)
                if tmp is not None:
                    if tmp.boss_hp <= 0:
                        if tmp.mana_spent < min_successful.mana_spent:
                            min_successful = tmp
                            print('new lowest mana spent found:', tmp.mana_spent)
                    elif tmp.mana_spent > min_successful.mana_spent:
                        continue
                    else:
                        new_states.append(tmp)

        states = new_states
        new_states = []

        # boss's turn
        for state in states:
            tmp = state.boss_attack()
            if tmp is not None:
                if tmp.boss_hp <= 0:
                    if tmp.mana_spent < min_successful.mana_spent:
                        min_successful = tmp
                        print('new lowest mana spent found:', tmp.mana_spent)
                        continue
                if tmp.hp <= 0:
                    continue  # you lose

                new_states.append(tmp)

        states = new_states

        print('-' * 100)

    print('answer:', min_successful.mana_spent)
    print('-' * 100)

    tmp = min_successful
    states = []

    # unwind nested states
    while tmp is not None:
        states.append(tmp)
        tmp = tmp.prev
    states.reverse()

    l = len(f'{len(states):,}')

    print('Steps:')
    for i, tmp in enumerate(states):
        print(f'{i:{l},} {tmp.action:15}\t{tmp.mana}\t{tmp.mana_spent}\t{tmp.boss_hp}\t{tmp.hp}')


def test2():
    tmp = State()
    tmp = tmp.poison()
    tmp = tmp.poison()
    print(tmp.effects)


def test():
    tmp = State()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('poison')
    tmp = tmp.poison()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('boss attack')
    tmp = tmp.boss_attack()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('magic missile')
    tmp = tmp.magic_missile()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('boss attack')
    tmp = tmp.boss_attack()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('magic missile')
    tmp = tmp.magic_missile()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('boss attack')
    tmp = tmp.boss_attack()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('magic missile')
    tmp = tmp.magic_missile()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')
    print('boss attack')
    tmp = tmp.boss_attack()
    print(f'player: {tmp.hp} - boss: {tmp.boss_hp}')


if __name__ == '__main__':
    main()
    # test2()
    # test()


"""
result: 1289

Steps:
 0 initial        	500	0	55	50
 1 poison         	327	173	55	49
 2 boss attack    	327	173	52	41
 3 drain          	254	246	47	42
 4 boss attack    	254	246	44	34
 5 recharge       	25	475	41	33
 6 boss attack    	126	475	38	25
 7 poison         	54	648	35	24
 8 boss attack    	155	648	32	16
 9 shield         	143	761	29	15
10 boss attack    	244	761	26	14
11 recharge       	15	990	23	13
12 boss attack    	116	990	20	12
13 poison         	44	1163	17	11
14 boss attack    	145	1163	14	10
15 drain          	173	1236	9	11
16 boss attack    	274	1236	6	3
17 magic missile  	221	1289	-1	2

Finished 'main' in 10 seconds
"""

# vim: set et sw=4 ts=4:

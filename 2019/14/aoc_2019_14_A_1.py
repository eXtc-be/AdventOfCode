# aoc_2019_14_A_1.py - Day 14: Space Stoichiometry - part 1
# Given the list of reactions in your puzzle input,
# what is the minimum amount of ORE required to produce exactly 1 FUEL?
# https://adventofcode.com/2019/day/14
# After trying different strategies (all flawed) I turned to the internet
# and found something that worked (see extern_1a.py and extern_1b.py)


from tools import time_it

from dataclasses import dataclass

from pprint import pprint


DATA_PATH = './input_2019_14'

# other constants


@dataclass
class Chemical:
    name: str
    amount: int


@dataclass
class Reaction:
    output: Chemical
    inputs: list[Chemical]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def parse_chemical(string: str) -> Chemical:
    return Chemical(string.split()[1], int(string.split()[0]))


def get_reactions(data_lines: list[str]) -> list[Reaction]:
    reactions = []

    for line in data_lines:
        input_specs, output_spec = line.split(' => ')
        reactions.append(Reaction(
            parse_chemical(output_spec),
            [parse_chemical(input_spec) for input_spec in input_specs.split(', ')]
        ))

    return reactions


def find_reaction(reactions: list[Reaction], goal: str) -> Reaction | None:
    for reaction in reactions:
        if reaction.output.name == goal:
            return reaction

    return None


def create_chemical(reactions: list[Reaction], goal: Chemical = Chemical('FUEL', 1)) -> dict[str, int]:
    elements = {reaction.output.name: 0 for reaction in reactions}
    elements['ORE'] = 0
    elements[goal.name] = goal.amount

    endings = [
        reaction.output.name
        for reaction in reactions
        if len(reaction.inputs) == 1 and reaction.inputs[0].name == 'ORE'
    ]
    endings.append('ORE')

    while True:
        for name in elements:
            if name in endings:
                continue
            if elements[name] > 0:
                reaction = find_reaction(reactions, name)
                if reaction.output.amount <= elements[name]:
                    elements[name] -= reaction.output.amount
                    for chemical in reaction.inputs:
                        elements[chemical.name] += chemical.amount

        if all(elements[name] <= 0 for name in elements if name not in endings):
            break

    for name in endings:
        if name == 'ORE':
            continue
        reaction = find_reaction(reactions, name)
        while elements[name] > 0:
            elements[name] -= reaction.output.amount
            for chemical in reaction.inputs:
                elements[chemical.name] += chemical.amount

    return elements


test_data = [
'''
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
'''.strip().splitlines(),
'''
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
'''.strip().splitlines(),
'''
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
'''.strip().splitlines(),
'''
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
'''.strip().splitlines(),
'''
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
'''.strip().splitlines(),
]


@time_it
def main(data_lines: list[str]) -> None:
    reactions = get_reactions(data_lines)
    # pprint(reactions)

    result = create_chemical(reactions)
    # print(result)

    print(f'End result: {result["ORE"]}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])

    # using test_data 0:
    #   End result: 31
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 165
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: ???
    #   Did not finish 'main' (infinite loop)
    # using test_data 3:
    #   End result: ???
    #   Did not finish 'main' (infinite loop)
    # using test_data 4:
    #   End result: ???
    #   Did not finish 'main' (infinite loop)
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

# aoc_2018_16_B_1.py - Day 16: Chronal Classification - part 2
# What value is contained in register 0 after executing the test program?
# https://adventofcode.com/2018/day/16


from aoc_2018_16_A_1 import (
    DATA_PATH,
    INSTRUCTION_SET,
    Sample,
    Computer,
    Register,
    Instruction,
    load_data,
    test_data,
    process_input,
)

from tools import time_it

from collections import defaultdict

from pprint import pprint


# other constants


def find_instruction_names(samples: list[Sample]) -> dict[int, str]:
    candidates = defaultdict(set)

    # find all candidate names for each opcode
    for sample in samples:
        for instruction_name in INSTRUCTION_SET:
            sample.instruction.name = instruction_name
            computer = Computer(
                [Register(i, r) for i, r in enumerate(sample.before)],
                [sample.instruction]
            )
            computer.run()
            if [reg.value for reg in computer.registers] == sample.after:
                candidates[sample.instruction.opcode].add(instruction_name)

    results = {}

    # build opcode: name dict by removing single items from longer lists
    while not all(len(candidate) == 0 for candidate in candidates.values()):
        for opcode, name_list in candidates.items():
            if len(name_list) == 1:
                results[opcode] = name_list.pop()
                for names in [candidate for candidate in candidates.values() if len(candidate) > 1]:
                    names.discard(results[opcode])

    return results


@time_it
def main(data_lines: list[str]) -> None:
    samples, program = process_input(data_lines)
    # pprint(samples)
    # print(set(sample.instruction.opcode for sample in samples))
    # pprint(program)
    # print(set(instruction.opcode for instruction in program))

    opcodes_to_names = find_instruction_names(samples)
    # pprint(results)

    computer = Computer(
        [Register(i) for i in range(4)],  # initialize 4 registers
        [Instruction(
            instruction.opcode,
            instruction.input_1,
            instruction.input_2,
            instruction.output,
            opcodes_to_names[instruction.opcode]
        ) for instruction in program]
    )
    # pprint(computer.program)

    computer.run()

    print(f'End result: {computer.registers[0].value}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using input data:
    #   End result: 540
    #   Finished 'main' in 1 second

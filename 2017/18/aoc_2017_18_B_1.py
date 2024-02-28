# aoc_2017_18_B_1.py - Day 18: Duet - part 2
# Once both of your programs have terminated (regardless of what caused them to do so),
# how many times did program 1 send a value?
# https://adventofcode.com/2017/day/18


from aoc_2017_18_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    Register,
    Instruction,
    Computer,
    set,
    add,
    mul,
    mod,
    jgz,
    _get_value,
)

from tools import time_it

from dataclasses import dataclass, field
from typing import Callable

from pprint import pprint


# other constants


@dataclass
class Computer_v2(Computer):
    send_queue: list[int] = field(default_factory=list, init=False)
    counter: int = field(default=0, init=False)
    receive: Callable = field(default=None, init=False)

    # inherit read_program

    # override run_program
    def run_program(self) -> None:
        while True:
            if not 0 <= self.program_counter < len(self.instructions):
                break  # quit if program jumps outside bounds

            current_instruction = self.instructions[self.program_counter]

            if current_instruction.function not in INSTRUCTION_SET:
                break  # quit if unknown instruction found

            current_function_name = current_instruction.function
            if current_function_name == 'brk':
                break

            current_function = INSTRUCTION_SET[current_function_name]

            current_arg1 = None
            if isinstance(current_instruction.arg1, int):
                current_arg1 = current_instruction.arg1
            elif isinstance(current_instruction.arg1, str):  # register
                for register in self.registers:
                    if register.name == current_instruction.arg1:
                        current_arg1 = register
                        break  # from inner for loop
                else:  # register not found -> quit program
                    break  # from outer while loop

            current_arg2 = None
            if isinstance(current_instruction.arg2, int):
                current_arg2 = current_instruction.arg2
            elif isinstance(current_instruction.arg2, str):  # register
                for register in self.registers:
                    if register.name == current_instruction.arg2:
                        current_arg2 = register
                        break  # from inner for loop
                else:  # register not found -> quit program
                    break  # from outer while loop

            result = None

            if current_function_name == 'snd':
                value = current_function(current_arg1, current_arg2)
                print(f'computer {self.id} sends {value}')
                self.send_queue.append(value)
                self.counter += 1
            elif current_function_name == 'rcv':
                if self.receive:
                    value = self.receive()
                    if value is None:
                        break
                    else:
                        result = current_function(current_arg1, value)
                        print(f'computer {self.id} receives {value}')
            else:
                result = current_function(current_arg1, current_arg2)

            if current_function_name == 'jgz':
                self.program_counter += result
            else:
                self.program_counter += 1

    def send(self):
        if self.send_queue:
            return self.send_queue.pop(0)

    def set_register(self, r: str, v: int):
        for register in self.registers:
            if register.name == r:
                register.value = v
                break


def snd(src: Register | int, dst=None) -> int:
    return _get_value(src)


def rcv(dst: Register, value: int) -> None:
    dst.value = value


INSTRUCTION_SET = {
    'snd': snd,
    'set': set,
    'add': add,
    'mul': mul,
    'mod': mod,
    'rcv': rcv,
    'jgz': jgz,
    'brk': None,
}


test_data2 = '''
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    computer_0 = Computer_v2(0)
    computer_0.read_program(data_lines)
    computer_0.set_register('p', 0)
    # pprint(computer_0)

    computer_1 = Computer_v2(1)
    computer_1.read_program(data_lines)
    computer_1.set_register('p', 1)
    # pprint(computer_1)

    computer_0.receive = computer_1.send
    computer_1.receive = computer_0.send

    while True:
        computer_0.run_program()
        if not computer_0.send_queue:
            break
        computer_1.run_program()
        if not computer_1.send_queue:
            break

    print(f'End result: {computer_1.counter}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data2
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 8001
    #   Finished 'main' in 1 second

    # print(INSTRUCTION_SET['snd'](1))
    # print(INSTRUCTION_SET['rcv'](1))
    # print(INSTRUCTION_SET['jgz'](1,7))

# intcode.py - an implementation of the IntCode computer used in several 2019 AoC puzzles


from dataclasses import dataclass, field
from enum import Enum, auto


class Mode(Enum):
    positional = 0
    immediate = 1


@dataclass
class Argument:
    mode: Mode
    value: int


@dataclass
class Computer:
    memory: list[int]
    inputs: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.ip = 0
        self._ip_len = len(f'{len(self.memory)}')
        self.outputs = []

    @property
    def input(self):
        return next(iter(self.inputs))

    def _get_arg(self, arg: Argument) -> int:
        if arg.mode == Mode.immediate:
            return arg.value
        elif arg.mode == Mode.positional:
            return self.memory[arg.value]
        else:  # unknown mode - should never happen
            raise ValueError(f'unknown mode: {arg.mode.name}')

    def add(self, args: list[Argument]) -> int:
        assert args[-1].mode == Mode.positional
        self.memory[args[-1].value] = self._get_arg(args[0]) + self._get_arg(args[1])
        return self.ip + len(args) + 1

    def mul(self, args: list[Argument]) -> int:
        assert args[-1].mode == Mode.positional
        self.memory[args[-1].value] = self._get_arg(args[0]) * self._get_arg(args[1])
        return self.ip + len(args) + 1

    def inp(self, args: list[Argument]) -> int:
        assert args[-1].mode == Mode.positional
        self.memory[args[-1].value] = self.input  # get the (next) input value
        return self.ip + len(args) + 1

    def out(self, args: list[Argument]) -> int:
        self.outputs.append(self._get_arg(args[0]))
        print(f'OUTPUT: {self.outputs[-1]}')
        return self.ip + len(args) + 1

    def jit(self, args: list[Argument]) -> int:
        if self._get_arg(args[0]) != 0:
            return self._get_arg(args[1])
        else:
            return self.ip + len(args) + 1

    def jif(self, args: list[Argument]) -> int:
        if self._get_arg(args[0]) == 0:
            return self._get_arg(args[1])
        else:
            return self.ip + len(args) + 1

    def les(self, args: list[Argument]) -> int:
        assert args[-1].mode == Mode.positional
        self.memory[args[-1].value] = int(self._get_arg(args[0]) < self._get_arg(args[1]))
        return self.ip + len(args) + 1

    def equ(self, args: list[Argument]) -> int:
        assert args[-1].mode == Mode.positional
        self.memory[args[-1].value] = int(self._get_arg(args[0]) == self._get_arg(args[1]))
        return self.ip + len(args) + 1

    def hlt(self, args: list[Argument]) -> int:
        return -1

    INSTRUCTION_SET = {
        1: {'function': add, 'args': 3},
        2: {'function': mul, 'args': 3},
        3: {'function': inp, 'args': 1},
        4: {'function': out, 'args': 1},
        5: {'function': jit, 'args': 2},
        6: {'function': jif, 'args': 2},
        7: {'function': les, 'args': 3},
        8: {'function': equ, 'args': 3},
        99: {'function': hlt, 'args': 0},
    }

    def run(self) -> int | None:
        while self.ip >= 0:
            # read next instruction from memory and convert it to zero padded string
            instruction = f'{self.memory[self.ip]:05}'
            opcode = int(instruction[-2:])  # extract opcode
            # modes = [int(val) for val in reversed(instruction[:3])]  # extract modes

            # get instruction details
            instruction_dict = self.INSTRUCTION_SET[opcode]
            function = instruction_dict['function']
            num_args = instruction_dict['args']
            args = [
                Argument(Mode(mode), val)
                for val, mode in zip(
                    self.memory[self.ip + 1:self.ip + 1 + num_args],
                    [int(val) for val in reversed(instruction[:3])]
                )
            ]

            # execute instruction
            self.ip = function(self, args)

        return self.outputs[-1] if self.outputs else None


if __name__ == "__main__":
    # # mem[3] = mem[0] + mem[0]; halt
    # test = Computer([1, 0, 0, 3, 99])
    # # mem[3] = 1 + 0; halt
    # test = Computer([1101, 1, 0, 3, 99])
    # # mem[3] = mem[9] + mem[10]; mem[0] = mem[3] * mem[11]; halt
    # test = Computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    # mem[0] = input[0]; mem[0] = mem[0] * mem[8]; halt
    test = Computer([3, 0, 2, 0, 8, 0, 4, 0, 99], [5])

    test.run()

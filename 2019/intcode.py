# intcode.py - an implementation of the IntCode computer used in several 2019 AoC puzzles


from dataclasses import dataclass, field
from enum import Enum, auto


class Mode(Enum):
    positional = 0
    immediate = 1
    relative = 2


ADDRESS_WIDTH = 4
NUMBER_WIDTH = 16


class State(Enum):
    running = auto()
    paused = auto()
    halted = auto()


@dataclass
class Argument:
    mode: Mode
    value: int


@dataclass
class Computer:
    memory: list[int]
    inputs: list[int] = field(default_factory=list)
    verbose: bool = True

    def __post_init__(self):
        self.ip = 0
        self.outputs = []
        self.state = State.paused
        self.rel_base = 0

    def _expand_memory(self, amount: int) -> None:
        self.memory.extend([0 for _ in range(amount)])

    def _check_index(self, index) -> None:
        if isinstance(index, slice):
            if index.stop > len(self.memory) - 1:
                self._expand_memory(index.stop - len(self.memory) + 1)
        else:
            if index > len(self.memory) - 1:
                self._expand_memory(index - len(self.memory) + 1)

    def __getitem__(self, index) -> int | list[int]:
        self._check_index(index)
        return self.memory[index]

    def __setitem__(self, index, value):
        self._check_index(index)
        self.memory[index] = value

    def _get_arg(self, arg: Argument) -> int:
        if arg.mode == Mode.immediate:
            return arg.value
        elif arg.mode == Mode.positional:
            return self[arg.value]
        elif arg.mode == Mode.relative:
            return self[self.rel_base + arg.value]
        else:  # unknown mode - should never happen
            raise ValueError(f'unsupported mode: {arg.mode.name}')

    def _set_dst(self, arg: Argument, value: int) -> None:
        if arg.mode == Mode.positional:
            self[arg.value] = value
        elif arg.mode == Mode.relative:
            self[self.rel_base + arg.value] = value
        else:  # unknown mode - should never happen
            raise ValueError(f'unsupported mode: {arg.mode.name}')

    def add(self, args: list[Argument]) -> int:
        assert args[-1].mode != Mode.immediate
        self._set_dst(args[-1], self._get_arg(args[0]) + self._get_arg(args[1]))
        return self.ip + len(args) + 1

    def mul(self, args: list[Argument]) -> int:
        assert args[-1].mode != Mode.immediate
        self._set_dst(args[-1], self._get_arg(args[0]) * self._get_arg(args[1]))
        return self.ip + len(args) + 1

    def inp(self, args: list[Argument]) -> int:
        assert args[-1].mode != Mode.immediate
        if self.inputs:
            self._set_dst(args[-1], self.inputs.pop(0))
            return self.ip + len(args) + 1
        else:
            self.state = State.paused
            return self.ip

    def out(self, args: list[Argument]) -> int:
        self.outputs.append(self._get_arg(args[0]))
        if self.verbose:
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
        assert args[-1].mode != Mode.immediate
        self._set_dst(args[-1], int(self._get_arg(args[0]) < self._get_arg(args[1])))
        return self.ip + len(args) + 1

    def equ(self, args: list[Argument]) -> int:
        assert args[-1].mode != Mode.immediate
        self._set_dst(args[-1], int(self._get_arg(args[0]) == self._get_arg(args[1])))
        return self.ip + len(args) + 1

    def rbo(self, args: list[Argument]) -> int:
        self.rel_base += self._get_arg(args[0])
        return self.ip + len(args) + 1

    def hlt(self, args: list[Argument]) -> int:
        self.state = State.halted
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
        9: {'function': rbo, 'args': 1},
        99: {'function': hlt, 'args': 0},
    }

    def run(self, inputs: list[int] = None) -> int | None:
        if inputs:
            self.inputs.extend(inputs)

        self.state = State.running

        while self.state == State.running:
            # read next instruction from memory and convert it to zero padded string
            instruction = f'{self[self.ip]:05}'
            opcode = int(instruction[-2:])  # extract opcode

            # get instruction details
            instruction_dict = self.INSTRUCTION_SET[opcode]
            function = instruction_dict['function']
            num_args = instruction_dict['args']
            args = [
                Argument(Mode(mode), val)
                for val, mode in zip(
                    self[self.ip + 1:self.ip + 1 + num_args],
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

    # # mem[0] = input[0]; mem[0] = mem[0] * mem[8]; output[0]; halt
    # test = Computer([3, 0, 2, 0, 8, 0, 4, 0, 99], [5])

    # mem[0] = input[0]; mem[20] = mem[20] * mem[8]; output[20]; halt :: len(mem) < 20
    test = Computer([3, 0, 2, 0, 8, 20, 4, 20, 99], [5])

    test.dump()

    # test.run()

# aoc_2016_10_A_1.py - Day 10: Balance Bots - part 1
# Based on your instructions, what is the number of the bot that is responsible
#   for comparing value-61 microchips with value-17 microchips?
# https://adventofcode.com/2016/day/10


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2016_10'

# other constants


@dataclass
class Input:
    value: int


@dataclass
class Output:
    id: int
    value: int = None


@dataclass
class Bot:
    id: int
    values: list[int] = field(default_factory=list)

    @property
    def lo(self) -> int | None:
        if len(self.values) < 2:
            return None
        else:
            return min(self.values)

    @property
    def hi(self) -> int | None:
        if len(self.values) < 2:
            return None
        else:
            return max(self.values)


@dataclass
class Instruction:
    source: Input | Bot | None = None  # source for specific-valued microchip (Input) or bot id (Bot)
    dest: Bot | None = None  # destination for specific-valued microchip (Input)
    dest_lo: Bot | Output | None = None  # destination for bot low value
    dest_hi: Bot | Output | None = None  # destination for bot high value
    processed: bool = False  # keep track of which instructions are already processed


@dataclass
class Factory:
    instructions: list[Instruction] = field(default_factory=list)
    inputs: list[Input] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)
    bots: list[Bot] = field(default_factory=list)

    def _get_bot(self, id: int) -> Bot:
        my_bot = None
        # check if bot already exists
        for bot in self.bots:
            if bot.id == id:
                my_bot = bot
                break
        else:  # else create it and append it to list
            my_bot = Bot(id)
            self.bots.append(my_bot)
        return my_bot

    def _get_output(self, id: int) -> Output:
        my_output = None
        # check if output already exists
        for output in self.outputs:
            if output.id == id:
                my_output = output
                break
        else:  # else create it and append it to list
            my_output = Output(id)
            self.outputs.append(my_output)
        return my_output

    def get_instructions(self, data_lines: list[str]) -> None:
        for line in data_lines:
            parts = line.split()
            match parts[0]:  # determine the source of the operation
                case 'value':  # specific-valued microchip
                    # sanity check inputs
                    if not parts[1].isdigit():  # value
                        raise ValueError(f'Invalid input: {line}')
                    if not parts[5].isdigit():  # bot id
                        raise ValueError(f'Invalid input: {line}')

                    # create source and destination objects
                    # inputs are unique, so no need to check if it already exists
                    source = Input(int(parts[1]))
                    self.inputs.append(source)

                    # for specific-valued microchip sources, the destination is always a bot
                    dest = self._get_bot(int(parts[5]))

                    # create instruction object
                    self.instructions.append(Instruction(source=source, dest=dest))
                case 'bot':
                    # sanity check inputs
                    if not parts[1].isdigit():  # source bot id
                        raise ValueError(f'Invalid input: {line}')
                    if not parts[6].isdigit():  # low destination bot id
                        raise ValueError(f'Invalid input: {line}')
                    if not parts[11].isdigit():  # high destination bot id
                        raise ValueError(f'Invalid input: {line}')

                    # create source and destination objects
                    # check if bot already exists
                    source = self._get_bot(int(parts[1]))

                    match parts[5]:  # determine the low destination of the operation
                        case 'bot':
                            dest_lo = self._get_bot(int(parts[6]))
                        case 'output':
                            dest_lo = self._get_output(int(parts[6]))
                        case _:
                            raise ValueError(f'Invalid input: {line}')
                    match parts[10]:  # determine the low destination of the operation
                        case 'bot':
                            dest_hi = self._get_bot(int(parts[11]))
                        case 'output':
                            dest_hi = self._get_output(int(parts[11]))
                        case _:
                            raise ValueError(f'Invalid input: {line}')

                    # create instruction object
                    self.instructions.append(Instruction(source=source, dest_lo=dest_lo, dest_hi=dest_hi))
                case _:
                    raise ValueError(f'Invalid input: {line}')

    def execute_instructions(self):
        while any(output.value is None for output in self.outputs):
        # while any(not instruction.processed for instruction in self.instructions):
            for instruction in [instr for instr in self.instructions if not instr.processed]:
                if isinstance(instruction.source, Input):
                    # for specific-valued microchip sources, the destination is always a bot
                    if len(instruction.dest.values) < 2:
                        instruction.dest.values.append(instruction.source.value)
                        instruction.processed = True
                elif isinstance(instruction.source, Bot):
                    # process bot's low value
                    if instruction.source.lo is not None:
                        if isinstance(instruction.dest_lo, Output):
                            if instruction.dest_lo.value is None:
                                instruction.dest_lo.value = instruction.source.lo
                                instruction.processed = True
                        else:
                            if len(instruction.dest_lo.values) < 2:
                                instruction.dest_lo.values.append(instruction.source.lo)
                                instruction.processed = True
                    # process bot's high value
                    if instruction.source.hi is not None:
                        if isinstance(instruction.dest_hi, Output):
                            if instruction.dest_hi.value is None:
                                instruction.dest_hi.value = instruction.source.hi
                                instruction.processed = True
                        else:
                            if len(instruction.dest_hi.values) < 2:
                                instruction.dest_hi.values.append(instruction.source.hi)
                                instruction.processed = True
                else:
                    raise ValueError(f'Invalid instruction: {instruction}')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], goal: tuple[int, int]) -> None:
    factory = Factory()
    # pprint(factory)

    factory.get_instructions(data_lines)
    # pprint(factory)

    factory.execute_instructions()
    # pprint(factory)

    for bot in factory.bots:
        if (bot.lo, bot.hi) == goal:
            print(f'End result: {bot.id}')
            break
    else:
        print(f'No solution found.')




if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    # main(data_lines, (2, 5))  # test
    main(data_lines, (17, 61))  # for real
    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 98
    #   Finished 'main' in 4 milliseconds

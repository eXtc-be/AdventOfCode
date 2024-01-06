# aoc_2023_18_B_1.py - Day 18: Lavaduct Lagoon - part 2
# The Elves are concerned the lagoon won't be large enough;
# if they follow their dig plan, how many cubic meters of lava could it hold?
# https://adventofcode.com/2023/day/18


from aoc_2023_18_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    DIR_TO_WALL,
    Color,
    Coord,
    Direction,
    Instruction,
    get_instructions,
)

from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


INT_TO_DIR = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}


@dataclass
class Vertex:
    position: Coord
    depth: int = 0
    pipe: str = '.'


@dataclass
class Edge:
    vertices: tuple[Vertex, Vertex] = field(default_factory=list)
    depth: int = 0
    pipe: str = '.'


@dataclass
class HugeGrid:
    vertices: list[Vertex] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def follow_instructions(self, instructions: list[Instruction]) -> None:  # changes the grid in place
        current_vertex = Vertex(Coord(0, 0), 1, '░')
        self.vertices.append(current_vertex)
        previous_move = ''
        for instruction in instructions:
            move = instruction.direction.name
            delta = instruction.direction.delta
            value = instruction.value

            # update current_vertex's pipe character
            if previous_move:
                current_vertex.pipe = DIR_TO_WALL[previous_move+move]

            # create next vertex
            next_vertex = Vertex(current_vertex.position + delta * value, 1, '░')
            self.vertices.append(next_vertex)

            # add vertex
            self.edges.append(Edge((current_vertex, next_vertex), 1, DIR_TO_WALL[move]))

            previous_move = move
            current_vertex = next_vertex

        # change first/last corner
        current_vertex.pipe = DIR_TO_WALL[previous_move+instructions[0].direction.name]
        self.vertices[0].pipe = DIR_TO_WALL[previous_move+instructions[0].direction.name]

    def __str__(self) -> str:
        """
        returns a string representation of the grid
        it does this by creating an array that will hold the complete grid,
        so don't do this with huge grids, lest you want to wait alot and
        possibly/likely get a memory overflow error
        """

        # we can't use negative coordinates,
        # so we need add an offset to every vertex's coordinates if necessary
        row_min = min(vertex.position.row for vertex in self.vertices)
        col_min = min(vertex.position.col for vertex in self.vertices)

        if row_min < 0:
            for vertex in self.vertices:
                vertex.position.row -= row_min

        if col_min < 0:
            for vertex in self.vertices:
                vertex.position.col -= col_min

        # calculate the number of rows and columns we need
        num_rows = max(vertex.position.row for vertex in self.vertices) + 1
        num_cols = max(vertex.position.col for vertex in self.vertices) + 1

        # create an array
        array = [['.' for _ in range(num_cols)] for _ in range(num_rows)]

        # populate the array
        for vertex in self.vertices:
            array[vertex.position.row][vertex.position.col] = vertex.pipe

        for edge in self.edges:
            if edge.pipe == '│':
                start = min(edge.vertices[0].position.row, edge.vertices[1].position.row) + 1
                end = max(edge.vertices[0].position.row, edge.vertices[1].position.row)
                for row in range(start, end):
                    array[row][edge.vertices[0].position.col] = edge.pipe
            else:
                start = min(edge.vertices[0].position.col, edge.vertices[1].position.col) + 1
                end = max(edge.vertices[0].position.col, edge.vertices[1].position.col)
                for col in range(start, end):
                    array[edge.vertices[0].position.row][col] = edge.pipe

        # return the array as a string
        return '\n'.join(''.join(str(cell) for cell in row) for row in array)


def _convert_instruction(instruction: Instruction) -> Instruction:
    return Instruction(
        Direction(INT_TO_DIR[int(instruction.color.hex[6], 16)]),
        int(instruction.color.hex[1:6], 16),
        Color()
    )


def convert_instructions(instructions: list[Instruction]) -> list[Instruction]:
    return [_convert_instruction(instruction) for instruction in instructions]


@time_it
def main(data_lines: list[str]) -> None:
    grid = HugeGrid()

    instructions = get_instructions(data_lines)
    # pprint(instructions)

    grid.follow_instructions(instructions)
    # pprint(grid)
    print(grid)

    # new_instructions = convert_instructions(instructions)
    # # pprint(new_instructions)
    #
    # grid.follow_instructions(new_instructions)
    # pprint(grid)

    # print(f'End result: {0}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

    # # test class HugeGrid
    # grid = HugeGrid()
    # print(grid)
    # grid = HugeGrid([
    #     Vertex(Coord(0, 0), 1, '.'),
    #     Vertex(Coord(10, 0), 1, '.'),
    #     Vertex(Coord(0, 10), 1, '.'),
    #     Vertex(Coord(25, 30), 1, '.'),
    # ])
    # print(grid)

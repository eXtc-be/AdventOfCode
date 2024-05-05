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

WALL_TO_VERT: dict[str, str] = {
    '┐': 'D',
    '┌': 'D',
    '┘': 'U',
    '└': 'U',
}


@dataclass
class Vertex:
    position: Coord
    depth: int = 0
    wall: str = '.'


@dataclass
class Edge:
    vertices: tuple[Vertex, Vertex] = field(default_factory=list)
    depth: int = 0
    wall: str = '.'


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

            # update current_vertex's wall character
            if previous_move:
                current_vertex.wall = DIR_TO_WALL[previous_move + move]

            # create next vertex
            next_vertex = Vertex(current_vertex.position + delta * value, 1, '░')
            self.vertices.append(next_vertex)

            # add edge
            # make sure the vertex with the lowest row number is stored first for vertical movements
            if move in 'UD':
                if current_vertex.position.row < next_vertex.position.row:
                    self.edges.append(Edge((current_vertex, next_vertex), 1, DIR_TO_WALL[move]))
                else:
                    self.edges.append(Edge((next_vertex, current_vertex), 1, DIR_TO_WALL[move]))
            # make sure the vertex with the lowest column number is stored first for horizontal movements
            if move in 'LR':
                if current_vertex.position.col < next_vertex.position.col:
                    self.edges.append(Edge((current_vertex, next_vertex), 1, DIR_TO_WALL[move]))
                else:
                    self.edges.append(Edge((next_vertex, current_vertex), 1, DIR_TO_WALL[move]))

            previous_move = move
            current_vertex = next_vertex

        # change first/last corner
        current_vertex.wall = DIR_TO_WALL[previous_move + instructions[0].direction.name]
        self.vertices[0].wall = DIR_TO_WALL[previous_move + instructions[0].direction.name]

        self._normalize_grid()

    def _normalize_grid(self) -> None:  # changes the grid in place
        """if any of the vertices' coordinates are negative,
        add an offset to every vertex so all the coordinates are positive again"""
        row_min = min(vertex.position.row for vertex in self.vertices)
        col_min = min(vertex.position.col for vertex in self.vertices)

        if row_min < 0:
            for vertex in self.vertices:
                vertex.position.row -= row_min

        if col_min < 0:
            for vertex in self.vertices:
                vertex.position.col -= col_min

    def _get_walls(self, rr: int) -> list:
        """returns all walls for a given row"""
        # get all vertical lines crossing the current row
        verticals = [
            edge
            for edge in self.edges
            if edge.wall == '│' and
               edge.vertices[0].position.row < rr < edge.vertices[1].position.row
        ]

        horizontals = [
            edge
            for edge in self.edges
            if edge.vertices[0].position.row == rr and
               edge.wall == '─'
        ]

        return verticals + horizontals

    def trench(self) -> int:
        """returns the number of cells in the trench"""
        total = 0

        for rr in range(max(vertex.position.row for vertex in self.vertices) + 1):
            walls = self._get_walls(rr)
            for wall in walls:
                if wall.wall == '│':
                    total += 1
                else:
                    total += wall.vertices[1].position.col - wall.vertices[0].position.col + 1

        return total

    def _get_edges(self, rr: int) -> list[int]:
        """returns all edges for a given row"""
        edges = []

        # get all vertical lines crossing the current row
        verticals = [
            edge
            for edge in self.edges
            if edge.wall == '│' and
               edge.vertices[0].position.row < rr < edge.vertices[1].position.row
        ]

        # get all horizontal lines in the current row
        horizontals = [
            edge
            for edge in self.edges
            if edge.wall == '─' and
               edge.vertices[0].position.row == rr
        ]

        # generate the list of columns where outside becomes inside and vice versa
        inside = False
        for edge in sorted(verticals + horizontals, key=lambda edge: edge.vertices[0].position.col):
            if edge.wall == '│':
                edges.append(edge.vertices[0].position.col)
                inside = not inside
            else:
                if WALL_TO_VERT[edge.vertices[0].wall] == WALL_TO_VERT[edge.vertices[1].wall]:  # ┌─┐ or └─┘
                    if inside:
                        edges.append(edge.vertices[0].position.col)
                        edges.append(edge.vertices[1].position.col)
                else:  # └─┐ or ┌─┘
                    if inside:
                        edges.append(edge.vertices[0].position.col)
                    else:
                        edges.append(edge.vertices[1].position.col)
                    inside = not inside

        return edges

    def dugout(self) -> int:
        """returns the number of cells in the grid enclosed by the trench"""
        total = 0
        # cells in the first and last rows and columns can only be part of the loop or outside the loop,
        # so we don't bother to check those rows and columns to determine the number of cells to dig out
        for rr in range(max(vertex.position.row for vertex in self.vertices) + 1)[1:-1]:
            edges = self._get_edges(rr)
            for left, right in zip(edges[::2], edges[1::2]):
                total += right - left - 1

        return total

    @property
    def size(self) -> tuple[int, int]:
        # calculate the number of rows and columns
        num_rows = max(vertex.position.row for vertex in self.vertices) + 1
        num_cols = max(vertex.position.col for vertex in self.vertices) + 1
        return num_rows, num_cols

    def __str__(self) -> str:
        """
        returns a string representation of the grid
        it does this by creating an array that will hold the complete grid,
        so DON'T USE THIS WITH LARGE GRIDS, lest you want to wait alot and
        possibly/likely get a memory overflow error
        """

        # calculate the number of rows and columns needed
        # num_rows = max(vertex.position.row for vertex in self.vertices) + 1
        # num_cols = max(vertex.position.col for vertex in self.vertices) + 1
        num_rows, num_cols = self.size

        # create the array with the calculated dimensions
        array = [['.' for _ in range(num_cols)] for _ in range(num_rows)]

        # populate the array: corners
        for vertex in self.vertices:
            array[vertex.position.row][vertex.position.col] = vertex.wall

        # populate the array: edges
        for edge in self.edges:
            if edge.wall == '│':
                # vertices in vertical edges are sorted by row number
                for row in range(edge.vertices[0].position.row + 1, edge.vertices[1].position.row):
                    array[row][edge.vertices[0].position.col] = edge.wall
            else:
                # vertices in horizontal edges are sorted by column number
                for col in range(edge.vertices[0].position.col + 1, edge.vertices[1].position.col):
                    array[edge.vertices[0].position.row][col] = edge.wall

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

    # grid.follow_instructions(instructions)
    # # pprint(grid)
    # print(grid)
    # print(f'Grid size: {grid.size[0]} x {grid.size[1]}')

    new_instructions = convert_instructions(instructions)
    # pprint(new_instructions)

    grid.follow_instructions(new_instructions)
    # pprint(grid)
    print(f'Grid size: {grid.size[0]} x {grid.size[1]}')

    trench = grid.trench()
    # print(trench)

    dugout = grid.dugout()
    # print(dugout)

    print(f'End result: {trench + dugout}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   Final grid size: 1,186,329 x 1,186,329
    #   End result: 952408144115
    #   Finished 'main' in 7.6 seconds
    # using input data:
    #   Final grid size: 12,231,325 x 16,768,543
    #   End result: 68548301037382
    #   Finished 'main' in 40 minutes and 29 seconds

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

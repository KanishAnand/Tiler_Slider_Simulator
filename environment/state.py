import numpy as np

from enum import Enum


class GridState:

    class Move(Enum):
        UP = -1, 0
        DOWN = 1, 0
        LEFT = 0, -1
        RIGHT = 0, 1

        @classmethod
        def from_char(cls, direction):
            if direction == 'U':
                return cls.UP
            elif direction == 'D':
                return cls.DOWN
            elif direction == 'L':
                return cls.LEFT
            elif direction == 'R':
                return cls.RIGHT

    def __init__(self, n, m, grid, tiles, targets):
        self.n, self.m = n, m
        self.grid = grid
        self.tiles = tiles
        self.targets = targets

    @classmethod
    def load(cls, input_file, moves_file):
        # Get the Grid
        file = open(input_file, 'r')
        n, m = list(map(int, file.readline().strip().split()))
        grid = np.array(
            [[cell == "." for cell in file.readline().strip()] for _ in range(n)])
        k = int(file.readline().strip())
        tiles, targets = [], []
        for _ in range(k):
            line = list(map(int, file.readline().strip().split()))
            tiles.append((line[0], line[1]))
            targets.append((line[2], line[3]))
        state = GridState(n, m, grid, tiles, targets)
        file.close()

        # read moves
        file = open(moves_file, 'r')
        moves = list(map(cls.Move.from_char, file.readline().strip('\n')))
        file.close()
        return state, moves

    def move(self, move: Move):
        delta_r, delta_c = move.value
        flag = 0
        for idx, tile in enumerate(self.tiles):
            next_r, next_c = tile[0] + delta_r, tile[1] + delta_c
            if 0 <= next_r < self.n and 0 <= next_c < self.m and \
                    self.grid[next_r, next_c] and (next_r, next_c) not in self.tiles:
                flag = 1
                tile = tile[0] + delta_r, tile[1] + delta_c
            self.tiles[idx] = tile
        return flag

    def __str__(self):
        labels = np.full(shape=self.grid.shape, fill_value='.')
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if not self.grid[x, y]:
                    labels[x, y] = '#'
        for x, y in self.tiles:
            labels[x, y] = 'a'
        for x, y in self.targets:
            labels[x, y] = 'A' if labels[x, y] != '.' else '1'
        return "\n".join(list(map(lambda line: "".join(line), labels)))

import sys
import typing

import pygame

from environment import config
from environment.state import GridState


class GridRender(GridState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.init()
        window_width: int = self.m * config.BLOCK_SIZE
        window_height: int = self.n * config.BLOCK_SIZE
        window_title: str = config.WINDOW_TITLE
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(window_title)

    def render(self):
        for y in range(self.m):
            for x in range(self.n):
                rect = pygame.Rect(
                    y * config.BLOCK_SIZE, x * config.BLOCK_SIZE, config.BLOCK_SIZE, config.BLOCK_SIZE)
                circle_color = config.COLORS["SPACE"]
                # assigning colour based on grid value
                if (x, y) in self.tiles and (x, y) in self.targets:
                    color = config.COLORS["COMBINED"][self.tiles.index((x, y))]
                elif (x, y) in self.tiles:
                    color = config.COLORS["TILE"][self.tiles.index((x, y))]
                    circle_color = config.COLORS["SPACE"]
                elif (x, y) in self.targets:
                    color = config.COLORS["SPACE"]
                    circle_color = config.COLORS["TARGET"][self.targets.index(
                        (x, y))]
                elif self.grid[x, y]:
                    color = config.COLORS["SPACE"]
                else:
                    color = config.COLORS["OBSTACLE"]

                pygame.draw.rect(self.screen, color, rect, 0, border_radius=0)

                if ((x, y) in self.tiles) ^ ((x, y) in self.targets):
                    pygame.draw.circle(self.screen, circle_color, (
                        y*config.BLOCK_SIZE + config.BLOCK_SIZE/2, x*config.BLOCK_SIZE + config.BLOCK_SIZE/2),
                        radius=config.RADIUS)

        # draw lines
        for x in range(self.m):
            pygame.draw.line(self.screen, config.COLORS['LINE'], (
                x*config.BLOCK_SIZE, 0), (x*config.BLOCK_SIZE, self.n*config.BLOCK_SIZE), config.LINE_WIDTH)

        for y in range(self.n):
            pygame.draw.line(self.screen, config.COLORS['LINE'], (
                0, y*config.BLOCK_SIZE), (self.m*config.BLOCK_SIZE, y*config.BLOCK_SIZE), config.LINE_WIDTH)

    def update(self, time):
        self.screen.fill(config.COLORS["SCREEN"])
        self.render()
        pygame.display.update()
        pygame.time.wait(time)

    @staticmethod
    def respond():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()

    @classmethod
    def load(cls, input_file, moves_file):
        state: GridState
        moves: typing.List[typing.Tuple[int, int]]
        state, moves = super().load(input_file, moves_file)

        state: GridRender = GridRender(
            state.n, state.m, state.grid, state.tiles, state.targets)
        state.render()
        state.update(config.WAIT_TIME)

        for move in moves:
            for _ in range(max(state.n, state.m) + 1):
                flag = state.move(move)
                if flag == 0:
                    # no tiles position changed
                    pygame.time.wait(config.WAIT_TIME)
                    break
                state.update(config.ANIMATION_TIME)
            state.respond()

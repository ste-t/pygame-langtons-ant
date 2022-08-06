#!/bin/env python
import sys
from contextlib import suppress
import numpy as np
import pygame
import pygame.gfxdraw

color0 = 0x282d3f
color1 = 0xd3423e

pygame.display.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.K_ESCAPE])

max_fps = 0  # 0 means no limit
clock = pygame.time.Clock()

window_size = 1080, 720
screen = pygame.display.set_mode(window_size)
square_size = 10  # Should be a divisor of the vertical and horizontal window size

cols, rows = int(window_size[0] /
                 square_size), int(window_size[1] / square_size)

grid = np.zeros((rows, cols), dtype=np.uint8)
print(f"\n{grid}\n")
print(
    f"Window size: {window_size[0]}x{window_size[1]}\n"
    f"Square size: {square_size}\n"
    f"Grid size: {grid.shape[1]}x{grid.shape[0]}")


class Ant:
    ANT_UP = 0
    ANT_RIGHT = 1
    ANT_DOWN = 2
    ANT_LEFT = 3

    def __init__(self, position, direction: int):
        # Make sure it is a list[int] and not a list[float]
        self.position = list(map(int, position))
        self.direction = direction

    def turn_right(self):
        self.direction += 1
        self.direction %= 4

    def turn_left(self):
        self.direction -= 1
        self.direction %= 4

    def switch_color(self):
        # print("Switching color")
        grid[self.position[1], self.position[0]
             ] = not grid[self.position[1], self.position[0]]

    def move(self):
        if self.direction == self.ANT_UP:
            self.position[1] -= 1
        elif self.direction == self.ANT_RIGHT:
            self.position[0] += 1
        elif self.direction == self.ANT_DOWN:
            self.position[1] += 1
        elif self.direction == self.ANT_LEFT:
            self.position[0] -= 1

        if self.position[0] > cols - 1:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = cols - 1

        if self.position[1] > rows - 1:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = rows - 1

    def step(self):
        # If is on 1
        if grid[self.position[1], self.position[0]]:
            # print("Right")
            self.turn_left()
        else:
            # print("Left")
            self.turn_right()
        self.switch_color()
        self.move()


def draw_cells():
    display_surf = pygame.Surface((grid.shape[1], grid.shape[0]))
    pygame.surfarray.blit_array(
        display_surf, np.transpose(grid * color1 + (1-grid)*color0))

    # TODO: figure out why this displays the wrong color
    #display_surf = pygame.surfarray.make_surface(np.transpose(grid * color1))

    pygame.transform.scale(display_surf, window_size, screen)


grid_lines = pygame.Surface(window_size, pygame.SRCALPHA)
if square_size > 1:
    for x in range(0, window_size[0], square_size):
        pygame.gfxdraw.vline(grid_lines, x, 0, window_size[1], (0, 0, 0))
    for y in range(0, window_size[1], square_size):
        pygame.gfxdraw.hline(grid_lines, 0, window_size[0], y, (0, 0, 0))


ant = Ant([cols / 2, rows / 2], 1)
# ant1 = Ant((cols / 2.5, rows / 2), 2)
# ant2 = Ant((cols / 1.8, rows / 2), 3)
# ant3 = Ant((cols / 3, rows / 2), 4)


def main():
    steps = 0
    while True:
        clock.tick(max_fps)

        # Exit on ESCAPE key press or if the user presses the X button on the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE:
                print(f"\n{steps} steps")
                sys.exit(0)

        ant.step()
        # ant1.step()
        # ant2.step()
        # ant3.step()

        steps += 1

        draw_cells()
        screen.blit(grid_lines, (0, 0))
        pygame.display.flip()

        with suppress(OverflowError):
            pygame.display.set_caption(
                f"Langton's ant ({int(clock.get_fps())}/{max_fps} fps)")

        """ Performance testing
        if steps == 11000:
            print(f"\n{steps} steps in {pygame.time.get_ticks()} ms")
            sys.exit()
        """


if __name__ == "__main__":
    main()

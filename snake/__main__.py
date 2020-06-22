import math
import random
from random import randrange
import tkinter as tk
from tkinter import messagebox

import pygame
import click

from .block import Block
from .snake import Snake
from snake import __version__
from .decorators import add_custom_help


class Game:
    def __init__(self, mode=0, width=500, height=500, rows=20):
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.width = width
        self.rows = rows
        self.win = pygame.display.set_mode((width, height))

    def adjust_speed(self):
        # setup sname speed so it don't move too fast
        pygame.time.delay(50)
        self.clock.tick(10)

    def drawGrid(self):
        """Draw the grid on the board."""
        size, x, y = self.width // self.rows, 0, 0
        # draw red boarder around the window to indicate danger
        if self.mode == 2:
            pygame.draw.line(self.win, (255, 0, 0), (0, 0), (0, self.width),
                             10)
            pygame.draw.line(self.win, (255, 0, 0), (self.width, 0),
                             (self.width, self.width), 12)
            pygame.draw.line(self.win, (255, 0, 0), (0, 0), (self.width, 0),
                             10)
            pygame.draw.line(self.win, (255, 0, 0), (0, self.width),
                             (self.width, self.width), 12)

        for i in range(self.rows):
            x, y = x + size, y + size
            # draw horizontal lines every "size"th pixels apart
            pygame.draw.line(self.win, (255, 255, 255), (x, 0),
                             (x, self.width))
            # draw vertical lines every "size"th pixel apart
            pygame.draw.line(self.win, (255, 255, 255), (0, y),
                             (self.width, y))

    def redrawWindow(self, snake, snack):
        self.win.fill((0, 0, 0))
        snake.draw(self.win)
        snack.draw(self.win)
        self.drawGrid()
        pygame.display.update()

    def message_box(self, subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass


@click.command()
@click.version_option(__version__, "-V", "--version", message="%(version)s")
@click.option(
    '--difficulty',
    '-d',
    default='0',
    help='Difficulty mode.',
    type=click.Choice(['0', '1', '2']),
)
@add_custom_help
def main(difficulty):
    """
Modes of play:\n
0: Move through walls.\n
1: Can't move though walls.\n
2. Can't touch walls.
"""
    mode = int(difficulty)
    game = Game(mode=mode)
    snake = Snake(game=game, mode=mode)
    snack = Block(snake=snake, rand=True)
    # game loop
    while True:
        game.adjust_speed()
        game.redrawWindow(snake, snack)
        snake.move()
        # if snake ate a snack, add a new block
        if snake.body[0].pos == snack.pos:
            snake.addBlock()
            snack = Block(snake=snake, rand=True)
        # if snake touches itslef, game over!
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(
                    map(lambda z: z.pos, snake.body[x + 1:])):
                game.message_box(
                    'You lost!', f'Your score: {len(snake.body)}\nPlay again.')
                snake.reset()
                break
        game.redrawWindow(snake, snack)


if __name__ == '__main__':
    main()

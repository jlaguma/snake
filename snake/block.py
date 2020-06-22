import random
from random import randrange

import pygame


class Block(object):
    rows = 20
    w = 500
    rand = False

    def __init__(self,
                 snake=None,
                 pos=(10, 10),
                 dx=1,
                 dy=0,
                 color=(255, 0, 0),
                 rand=False):
        self.snake = snake
        self.pos = pos
        self.dx = dx
        self.dy = dy
        self.color = color
        self.rand = rand
        self.rand_data = []
        if rand:
            self.pos = self.random_position()
            self.rand_data = self.generate_random_block()

    def move(self, dx, dy):
        self.dx, self.dy = dx, dy
        new_x, new_y = self.pos[0] + self.dx, self.pos[1] + self.dy
        # make sure we dong move off the board
        if new_x < 0:
            new_x = 0
        elif new_x >= self.rows:
            new_x = self.rows - 1
        if new_y < 0:
            new_y = 0
        elif new_y >= self.rows:
            new_y = self.rows - 1
        self.pos = (new_x, new_y)

    def random_position(self):
        """Choose a random block on the board."""
        while True:
            x, y = randrange(self.rows), randrange(self.rows)
            # make sure that snack does not pop up on top of snakes body
            if len(list(filter(lambda sb: sb.pos ==
                               (x, y), self.snake.body))) > 0:
                continue
            else:
                break
        return (x, y)

    def generate_random_block(self):
        """We build a kind of Identicon here."""
        # create random 10 x 10 block with each cell in shape of (1, (255,255,255))
        block1 = [[(randrange(2), (random.choice([0, 255]),
                                   random.choice([0, 255]),
                                   random.choice([0, 255])))
                   for _ in range(self.rows // 2)]
                  for _ in range(self.rows // 2)]
        # reverse the above list (horizontal mirror)
        block2 = [list(reversed(x)) for x in block1]
        # vertical mirror of block1
        block3 = [x for x in reversed(block1)]
        # vertical mirror of block2
        block4 = [x for x in reversed(block2)]
        # join all 4 lists into 1 list
        block = [x + y for x, y in list(zip(block1, block2))
                 ] + [x + y for x, y in list(zip(block3, block4))]
        return block

    def draw(self, surface, eyes=False):
        """Draw block on theboard."""
        i, j, dis = self.pos[0], self.pos[1], self.w // self.rows
        pygame.draw.rect(surface, self.color,
                         (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if self.rand:
            for r, row in enumerate(self.rand_data):
                for c, col in enumerate(row):
                    toggle, color = col[0], col[1]
                    if toggle == 1:
                        pygame.draw.circle(surface, color,
                                           (i * dis + r + 3, j * dis + c + 3),
                                           1)
        elif eyes:
            center, radius = dis // 2, 3
            mid1, mid2 = (i * dis + center - radius,
                          j * dis + 8), (i * dis + dis - radius * 2,
                                         j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), mid1, radius)
            pygame.draw.circle(surface, (0, 0, 0), mid2, radius)

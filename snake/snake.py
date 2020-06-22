import pygame

from .block import Block


class Snake(object):
    body = []
    turns = {}

    def __init__(self, game=None, mode=0):
        self.head = Block()
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1
        self.game = game
        self.mode = mode

    def move(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

            # at each key press, we save the coordinates of the head at that
            # point as well as the direction in which head was turned
            # do not allow reversing the direction, only forward, left or right
            keys = pygame.key.get_pressed()
            for key in keys:
                if self.mode == 0:
                    if keys[pygame.K_LEFT]:
                        if self.dx == 1 and self.dy == 0:
                            pass
                        else:
                            self.dx, self.dy = -1, 0
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                    elif keys[pygame.K_RIGHT]:
                        if self.dx == -1 and self.dy == 0:
                            pass
                        else:
                            self.dx, self.dy = 1, 0
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                    elif keys[pygame.K_UP]:
                        if self.dx == 0 and self.dy == 1:
                            pass
                        else:
                            self.dx, self.dy = 0, -1
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                    elif keys[pygame.K_DOWN]:
                        if self.dx == 0 and self.dy == -1:
                            pass
                        else:
                            self.dx, self.dy = 0, 1
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif self.mode == 1 or self.mode == 2:
                    if keys[pygame.K_LEFT]:
                        # prevent reversal of direction
                        if self.head.dx == 1 or self.head.pos[0] <= 0:
                            pass
                        else:
                            self.dx, self.dy = -1, 0
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                    elif keys[pygame.K_RIGHT]:
                        if self.head.dx == -1 or self.head.pos[
                                0] >= self.head.rows - 1:
                            pass
                        else:
                            self.dx, self.dy = 1, 0
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                    elif keys[pygame.K_UP]:
                        if self.head.dy == 1 or self.head.pos[1] <= 0:
                            pass
                        else:
                            self.dx, self.dy = 0, -1
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]
                    elif keys[pygame.K_DOWN]:
                        if self.head.dy == -1 or self.head.pos[
                                1] >= self.head.rows - 1:
                            pass
                        else:
                            self.dx, self.dy = 0, 1
                            self.turns[self.head.pos[:]] = [self.dx, self.dy]

        # iterate though entire snakes body
        for i, c in enumerate(self.body):
            # grab the position of a block
            p = c.pos[:]
            # if Block is at the coordinates saved inside turns dict
            # change the direction of that cube
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # if this is the last Block of the Snake's body,
                # we remove the saved "turn" from turns dict
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            # keep moving in the same direction as before, but detect walls
            else:
                if self.mode == 0:
                    # detect left wall collision
                    if c.dx == -1 and c.pos[0] <= 0:
                        c.pos = (c.rows - 1, c.pos[1])
                    # detect right wall collision
                    elif c.dx == 1 and c.pos[0] >= c.rows - 1:
                        c.pos = (0, c.pos[1])
                    # detect floor collision
                    elif c.dy == 1 and c.pos[1] >= c.rows - 1:
                        c.pos = (c.pos[0], 0)
                    # detect root collision
                    elif c.dy == -1 and c.pos[1] <= 0:
                        c.pos = (c.pos[0], c.rows - 1)
                    # keep moving in same direction as before
                    else:
                        c.move(c.dx, c.dy)
                elif self.mode == 1:
                    # detect left wall collision
                    if c.dx == -1 and c.pos[0] <= 0:
                        if c.pos[1] > c.rows // 2:
                            self.dx, self.dy = 0, -1
                        else:
                            self.dx, self.dy = 0, 1
                    # detect right wall collision
                    elif c.dx == 1 and c.pos[0] >= c.rows - 1:
                        if c.pos[1] > c.rows // 2:
                            self.dx, self.dy = 0, -1
                        else:
                            self.dx, self.dy = 0, 1
                    # detect floor collision
                    elif c.dy == 1 and c.pos[1] >= c.rows - 1:
                        if c.pos[0] > c.rows // 2:
                            self.dx, self.dy = -1, 0
                        else:
                            self.dx, self.dy = 1, 0
                    # detect roof collision
                    elif c.dy == -1 and c.pos[1] <= 0:
                        if c.pos[0] > c.rows // 2:
                            self.dx, self.dy = -1, 0
                        else:
                            self.dx, self.dy = 1, 0
                    else:
                        self.dx, self.dy = c.dx, c.dy
                    c.move(self.dx, self.dy)
                elif self.mode == 2:
                    # detect left wall collision
                    if c.dx == -1 and c.pos[0] <= 0:
                        self.game.message_box(
                            'You lost!',
                            f'Your score: {len(self.body)}\nPlay again.')
                        self.reset()
                        break
                    # detect right wall collision
                    elif c.dx == 1 and c.pos[0] >= c.rows - 1:
                        self.game.message_box(
                            'You lost!',
                            f'Your score: {len(self.body)}\nPlay again.')
                        self.reset()
                        break
                    # detect floor collision
                    elif c.dy == 1 and c.pos[1] >= c.rows - 1:
                        self.game.message_box(
                            'You lost!',
                            f'Your score: {len(self.body)}\nPlay again.')
                        self.reset()
                        break
                    # detect roof collision
                    elif c.dy == -1 and c.pos[1] <= 0:
                        self.game.message_box(
                            'You lost!',
                            f'Your score: {len(self.body)}\nPlay again.')
                        self.reset()
                        break
                    else:
                        self.dx, self.dy = c.dx, c.dy
                    c.move(self.dx, self.dy)

    def reset(self):
        self.head = Block()
        self.body = []
        self.turns = {}
        self.dx = 0
        self.dy = 1
        self.body.append(self.head)

    def addBlock(self):
        tail = self.body[-1]
        dx, dy = tail.dx, tail.dy
        if dx == 1 and dy == 0:
            self.body.append(Block(pos=(tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Block(pos=(tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Block(pos=(tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Block(pos=(tail.pos[0], tail.pos[1] + 1)))
        self.body[-1].dx = dx
        self.body[-1].dy = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

from SnakeBody import SnakeBody
from Board import Board
import pygame

# The snake is a list of SnakeBody parts.
class Snake(list):

    factor = 10

    def __init__(self, start_x, start_y, n):
        list.__init__(self, [SnakeBody(start_x, start_y + i * Snake.factor)
                             for i in range(n)])

    def move_head(self, dx, dy):
        self[0].x += dx
        self[0].y += dy

    def update(self, score):
        for i in range(len(self) - 1, 0, -1):
            self[i].x = self[i - 1].x
            self[i].y = self[i - 1].y

    def check_death(self, display_width, display_height):
        if not (9 < self[0].x < display_width+10 and 9 < self[0].y < display_height+1):
            return True
        return any(body_part.x == self[0].x and body_part.y == self[0].y for body_part in self[1:])

    def draw(self, game_display):
        for body_part in self:
            pygame.draw.rect(game_display, Board.teal,
                             (body_part.x, body_part.y, Snake.factor, Snake.factor))

import random


class Food:  # Class to represent the food over the board.

    def __init__(self, start, width_stop, height_stop, step, snake):
        self.food_x = 0
        self.food_y = 0
        self.draw(start, width_stop, height_stop, step)  # draw food by changing the x,y.
        for i in range(0, len(snake)):
            if self.food_x == snake[i].x and self.food_y == snake[i].y:  # if collision:
                self.draw(start, width_stop, height_stop, step)         # draw a new food.
                i = 0

    def check_collision(self,snake):
        for i in range(0, len(snake)):  # Iterate over the snake
            if self.food_x == snake[i].x and self.food_y == snake[i].y:  # if at least 1 part collides with the food.
                return True  # return that there is a collision.
        return False

    def draw(self, start, width_stop, height_stop, step):
        rand_x = random.randrange(start, width_stop - step)  # randomize a number between the start and stop
        if rand_x % 10 != 0:  # if not a multiply of 10
            rand_x = (rand_x - rand_x % 10)  # reduce it to be a multiply of 10
        self.food_x = rand_x

        rand_y = random.randrange(start, height_stop - step)  # randomize a number between the start and stop
        if rand_y % 10 != 0:  # if not a multiply of 10
            rand_y = (rand_y - rand_y % 10)  # reduce it to be a multiply of 10
        self.food_y = rand_y
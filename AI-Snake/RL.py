from Snake import Snake
from Board import Board
from SnakeBody import SnakeBody
from Food import Food
from collections import defaultdict
import pygame
import time
import numpy as np
import random


global clock
global window_width
global window_height
global display_width
global display_height
global game
global sleep

global score
global game_display
global snake
global food

global font
global text

global x_change
global y_change
global first_time
global eat
global mov
global maxScore 
global gen

def setTimeSleepUp():
    sleep+=0.01
    
def setTimeSleepDown():
    sleep-=0.01    

def sscore(_score,maxsc):
    text1 = font.render("Score: " + str(_score), False, Board.teal)
    game_display.GAME_display.blit(text1, (game_display.width - 150, 100))
    
    text2 = font.render("Max score: " + str(maxsc), False, Board.red)
    game_display.GAME_display.blit(text2, (game_display.width - 150, 130))
    
    text3 = font.render("Game number: " + str(gen), False, Board.blue_black)
    game_display.GAME_display.blit(text3, (game_display.width - 150, 70))
    
    text4 = font.render("Speed: " + str(sleep), False, Board.red)
    game_display.GAME_display.blit(text4, (game_display.width - 150, 160))


def update_data_set(data_set, mov, snake, food):
    # initDataSet('DataSets.csv')
    new_row = np.array([0] * 66)  # initiate a new row of 0
    new_row[((int(food.food_y / 10) - 1) * 8) + ((int(food.food_x / 10) - 1))] = 1  # computes the index of the food and puts 1.
    for i in range(0, (len(snake) - 1)):
        if i == 0:
            new_row[((int(snake[i].y / 10) - 1) * 8) + ((int(snake[i].x / 10) - 1))] = 3  # computes the index of the head and puts 3.
        else:
            new_row[((int(snake[i].y / 10) - 1) * 8) + ((int(snake[i].x / 10) - 1))] = 2  # computes the index of the food and puts 2.

    new_row[65] = mov  # The action we took.

    data_set = np.vstack([data_set, new_row])  # Stacks the row into the CSV file.
    return data_set

def what_is_cur_state(snake, food):
    head_pos = [(int(snake[0].y / 10) - 1),(int(snake[0].x / 10) - 1)]
    tail_pos = [(int(snake[len(snake)-1].y / 10) - 1),(int(snake[len(snake)-1].x / 10) - 1)]
    food_pos = [(int(food.food_y / 10) - 1), (int(food.food_x / 10) - 1)]
    tail_rel = ((head_pos[1]-tail_pos[1]),(head_pos[0]-tail_pos[0]))
    food_rel = ((head_pos[1]-food_pos[1]),(head_pos[0]-food_pos[0]))
    
    return (tail_rel,food_rel,len(snake))

def reset():
    global clock
    global window_width
    global window_height
    global display_width
    global display_height
    global game
    global score
    global game_display
    global snake
    global food
    #global _score
    global font
    global text
    global gen
    global x_change
    global y_change
    global first_time
    global eat
    global mov
    global maxScore 
    global sleep

    score = 60
    game_display = Board(window_width, window_height)
    snake = Snake(20, 20, 3)
    food = Food(10, display_width, display_height, 10, snake)
    
    font = pygame.font.SysFont('Time New Roman, Arial', 20)
    #text = font.render('Score: %d' % tuple([game_display.game_score]), False, Board.gold)

    x_change = 0
    y_change = 0
    first_time = True
    eat = True
    mov = 0
    
    return what_is_cur_state(snake,food)
    
def step(action):
    global clock
    global window_width
    global window_height
    global display_width
    global display_height
    global game
    global score
    global game_display
    global snake
    global food
    
    global font
    global text
    global gen
    global x_change
    global y_change
    global first_time
    global eat
    global mov
    global maxScore 
    
    reward = -0.25
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if clicked on the window's X.
            pygame.quit()
            game = False
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_UP:  # if it was the up arrow
#                setTimeSleepUp()
#            elif event.key == pygame.K_DOWN:  # if it was the down arrow
#                 setTimeSleepDown()
        
    #first_time = False
    if action==4:  # if it was the left arrow
        if x_change != 10:
            x_change = -10
            y_change = 0
            mov = 4
    elif action==6:  # if it was the right arrow
        if x_change != -10:
            x_change = 10
            y_change = 0
            mov = 6
    elif action==8:  # if it was the up arrow
        if y_change != 10:
            x_change = 0
            y_change = -10
            mov = 8
    elif action==2:  # if it was the down arrow
        if y_change != -10:
            x_change = 0
            y_change = 10
            mov = 2
    #if not first_time:  # if it's while we haven't clicked anything when the window pops.
        #data_sets = update_data_set(data_sets, mov, snake, food)
    snake.update(score)
    if score % 10 == 0 and eat:  # still need to figure out.--------------
        snake.append(SnakeBody(snake[len(snake) - 1].x, snake[len(snake) - 1].y))
        print(len(snake))
        eat = False
    snake.move_head(x_change, y_change)  # changes the head's x,y. making it "move"
    state = what_is_cur_state(snake,food)

    if (snake[0].x < food.food_x + 10 and snake[0].x >= food.food_x
            and snake[0].y < food.food_y + 10 and snake[0].y >= food.food_y):
        score += 10
        game_display.game_score += 1
        food = Food(10, display_width, display_height, 10, snake)
        eat = True
        reward = 1

    if snake.check_death(display_width, display_height):
        #if game_display.pop_exit_window():#):
        reward = -1
        state = what_is_cur_state(snake,food)
        done = (len(snake)==64)
        state = what_is_cur_state(snake,food)
        print ("death")
        return state, reward, done

    game_display.clean()
    game_display.borders(display_height, display_width)
    pygame.draw.rect(game_display.GAME_display, Board.red,
                     (food.food_x, food.food_y, Snake.factor, Snake.factor))
    snake.draw(game_display.GAME_display)
    #game_display.GAME_display.blit(text, (game_display.width - 50, 50))############################
    #max_score(len(snake)-4)
    if maxScore < len(snake)-4:
            maxScore = game_display.game_score
            
    sscore(len(snake)-4, maxScore)
    pygame.display.flip()
    time.sleep(0.120)
    clock.tick(60)
    
    done = (len(snake)==64)
    return state, reward, done




def main():
        
    global clock
    global window_width
    global window_height
    global display_width
    global display_height
    global game
    global maxScore 
    global gen
    global sleep
    clock = pygame.time.Clock()
    window_width = 300
    window_height = 300
    display_width = 80
    display_height = 80
    sleep = 0.005
    game = True
    
    action_space = [2,4,6,8]
    Q = defaultdict(dict)
    alpha = 0.618
    
    for episode in range(1,500000):
        done = False
        G, rwrd = 0,0
        maxScore=0
        gen = 1
        
        state = reset()
        while not done:
            if state in Q:
                action = (np.argmax(Q[state])+1)*2
            else:
                Q[state] = np.zeros([4])
                action = (np.argmax(Q[state])+1)*2
            nxt_state, rwrd, done = step(action)
            if state in Q:
                if action in Q[state]:
                    if nxt_state in Q:
                        Q[state][int(action/2)-1] += alpha * (rwrd + np.max(Q[nxt_state]) - Q[state][action])
                    else:
                        Q[state][int(action/2)-1] += ((alpha * rwrd) - Q[state][action])
                else:
                    if nxt_state in Q:
                        Q[state][int(action/2)-1] = alpha * (rwrd + np.max(Q[nxt_state]))
                    else:
                        Q[state][int(action/2)-1] = (alpha * rwrd)
            else:
                Q[state] = np.zeros([4])
                if nxt_state in Q:
                        Q[state][int(action/2)-1] = alpha * (rwrd + np.max(Q[nxt_state]))
                else:
                    Q[state][int(action/2)-1] = (alpha * rwrd)
            G += rwrd
            state = nxt_state
            if rwrd == -1:
                gen+=1
                state = reset()

    #data_sets = np.arange(66)

    #while True:  # while the program runs.
    
    
    

if __name__ == "__main__":
    main()

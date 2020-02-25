# Modules -------------------------------------------------------------------
import pygame
from pygame.locals import*
import numpy as np
import random
import matplotlib.pyplot as plt
from AIsnake import AIsnake 
# Configuration ------------------------------------------------------------
DISPLAY_GAME = False  # Set this variable to true to show the game
x_grid_size = 4
y_grid_size = 4
Number_games = 10 # Here set the number of games you want the network to train
# Constants -----------------------------------------------------------------
WIDTH = 500
HEIGHT = 500
tile_size = min(HEIGHT/y_grid_size, WIDTH/x_grid_size)
margin = 0.9 # from 0 (whole tile is margin) to 1 (no margin at all)
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3
reward = 0
episode = 0
total_reward = 0
time_step= 0
total_reward_list = []
time_step_list = []
#Colors-----------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 150, 0)
BLUE = (0, 0, 255)
BLACK= (0, 0, 0)
action = UP
# Classes--------------------------------------------------------------------
class Game:
    def __init__(self, apple_reward = 1, die_reward = -1):
        self.map=np.zeros((x_grid_size, y_grid_size))
        self.game_over = False
        self.apple_reward = apple_reward
        self.die_reward = die_reward

    def take_action(self, action, player, apple):
        player.change_velocity(action)
        player.moving1()
        player.K = True
        if len(player.snake)!=len(set(player.snake)):
            self.game_over = True
            reward = self.die_reward
        if player.x > x_grid_size or player.y> y_grid_size:
            self.game_over = True
            reward = self.die_reward
        if not (self.game_over):
            if (player.x, player.y) == (apple.x, apple.y):
                while (apple.x, apple.y) in player.snake:
                    apple.new_apple()
                reward = self.apple_reward
            else:
                player.moving2()
                reward = 0
        self.map = np.zeros((x_grid_size, y_grid_size))
        for (i,j) in player.snake:
            if (i,j) == player.snake[-1]:
                self.map[i,j] = 5
            else:
                self.map[i,j] = 1
        self.map[apple.x, apple.y] = -5
        return self.map, reward
class Player:
    def __init__(self):
        self.snake = [(2,1),(2,2)] #Initial position
        self.x, self.y = 2, 1 
        self.step = 1
        self.dx, self.dy = 1, 0
        self.speed = 5
        self.points = 0
        self.K= True
    def change_velocity(self, action):
        if self.dx == 0 and action == RIGHT and self.K == True:
            self.dx = 1
            self.dy = 0
            self.K = False
        if self.dx == 0 and action == LEFT and self.K == True:
            self.dx = -1
            self.dy = 0
            self.K = False
        if self.dy == 0 and action == UP and self.K == True:
            self.dx = 0
            self.dy = -1
            self.K = False
        if self.dy == 0 and action == DOWN and self.K == True:
            self.dx = 0
            self.dy = 1 
            self.K = False
    def moving1(self):
        self.x=(self.x+self.dx)%x_grid_size
        self.y=(self.y+self.dy)%y_grid_size
        self.snake.append((self.x, self.y))
    def moving2(self):
        self.snake.pop(0)
class Apple:
    def __init__(self):
           self.x = random.randint(0, x_grid_size-1)
           self.y = random.randint(0, y_grid_size-1)
    def new_apple(self):
        self.x = random.randint(0, x_grid_size-1)
        self.y = random.randint(0, y_grid_size-1)
# Functions

def text(texto, posx, posy, color=(255, 255, 255)):

    fuente = pygame.font.Font('images/DroidSans.ttf', 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#  -----------------------------------------------------------------------------
def main():
    #--------------------------- PyGame stuff ----------------------------------
    if DISPLAY_GAME:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My PySnake")
    #---------------------------------------------------------------------------

    #------------------------ Initialization ----------------------------------
    game = Game()
    player = Player()
    apple = Apple()
    agent = AIsnake()
    if DISPLAY_GAME:
        clock = pygame.time.Clock()
    #---------------------------------------------------------------------------
    while True:
        if DISPLAY_GAME:
            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit(0)
        #--------------------- Logic of the game -------------------------------
        old_state = game.map
        action = agent.get_next_action(old_state)
        new_state, reward2 = game.take_action(action, player, apple)
        agent.update(old_state, new_state, action, reward)
        global time_step
        global total_reward
        global total_reward_list
        global episode
        total_reward = total_reward + reward2
        time_step += 1
        total_reward_list.append(total_reward)
        time_step_list.append(time_step)
        #--------------------- Drawing the map in the display-------------------
        if DISPLAY_GAME:
            time = clock.tick(5)
            screen.fill(BLACK)
            # new_state, action = agent.get_next_action(old_state, player, apple)
            for i in range(0, x_grid_size):
                for j in range(0, y_grid_size):
                    if int(game.map[i,j])==1:
                        pygame.draw.rect(screen,GREEN_DARK,(i*tile_size,j*tile_size,
                        tile_size*margin,tile_size*margin))
                    if int(game.map[i,j])==-5:
                        pygame.draw.rect(screen,RED,(i*tile_size,j*tile_size,
                        tile_size*margin,tile_size*margin))
                    if int(game.map[i,j])==5:
                        pygame.draw.rect(screen,GREEN,(i*tile_size,j*tile_size,
                        tile_size*margin,tile_size*margin))
            # p_jug, p_jug_rect = text(str(player.points), WIDTH/4, 40)
            # screen.blit(p_jug, p_jug_rect)
            pygame.display.flip()
         #---------------------Restart for game over -------------------
        if game.game_over:
            game = Game()
            player = Player()
            apple = Apple()
            episode = episode + 1  
            print(episode)
            game.game_over = False
        if episode > Number_games:
            agent.save_model('model')
            plt.plot(time_step, total_reward,'ro')
            plt.show()
            break

# Main //////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    main()



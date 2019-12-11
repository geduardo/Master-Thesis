# Modules -------------------------------------------------------------------
import pygame
from enums2 import *
from pygame.locals import*
import numpy as np
import random
from AIsnake import AIsnake 
# Constants -----------------------------------------------------------------
x_grid_size = 4
y_grid_size = 4
WIDTH = 500
HEIGHT = 500
tile_size = min(HEIGHT/y_grid_size, WIDTH/x_grid_size)
margin = 0.9 # from 0 (whole tile is margin) to 1 (no margin at all)
#Colors-----------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 150, 0)
BLUE = (0, 0, 255)
BLACK= (0, 0, 0)
action = UP
reward = 0
# Classes--------------------------------------------------------------------
class Game:
    def __init__(self, apple_reward = 1, die_reward = -1):
        self.map=np.zeros((x_grid_size, y_grid_size))
        self.game_over = False
        self.apple_reward = apple_reward
        self.die_reward = die_reward
        self.n=0

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
                self.n=0
                reward = self.apple_reward
                player.speed = player.speed + 1
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
        if self.n>40 and not(reward == self.die_reward):
            reward=-1
        self.n=self.n+1
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My PySnake")
    #---------------------------------------------------------------------------

    #------------------------ Initialization ----------------------------------
    game = Game()
    player = Player()
    apple = Apple()
    agent = AIsnake()
    clock = pygame.time.Clock()
    #---------------------------------------------------------------------------
    while True:
        time = clock.tick(5)
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
        #--------------------- Logic of the game -------------------------------
        old_state = game.map
        action = agent.get_next_action(old_state)
        new_state, reward2 = game.take_action(action, player, apple)
        agent.update(old_state, new_state, action, reward)
        #--------------------- Drawing the map in the display-------------------
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
        print(agent.eps)
         #---------------------Restart for game over -------------------
        if game.game_over:
            game = Game()
            player = Player()
            apple = Apple()
            game.game_over = False

# Main //////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    main()



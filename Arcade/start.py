import arcade
import random
import timeit
# Set how many rows and columns we will have
ROW_COUNT = 8
COLUMN_COUNT = 8
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 50
# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5
# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
HALF_SQUARE_WIDTH = (WIDTH)/2
HALF_SQUARE_HEIGHT = (HEIGHT)/2
SCREEN_TITLE = "SNAKE"
# We create a class for the player
class Player:
    # Let's define the initial configuration of the player
    # We create a list that with the points of the snake
    snake = [(2,3)] #Initial position
    x, y = 2, 3 
    step = 1
    dx, dy = 1, 0
    speed = 5
    points = 0
    K= True
    def change_velocity_Right(self):
        if self.dx == 0:
            self.dx = 1
            self.dy = 0
    def change_velocity_Left(self):
        if self.dx == 0:
            self.dx = -1
            self.dy = 0
    def change_velocity_Down(self):
        if self.dy == 0:
            self.dx = 0
            self.dy = -1
    def change_velocity_Up(self):
        if self.dy == 0:
            self.dx = 0
            self.dy = 1 
    def moving1(self):
        self.x=(self.x+self.dx)%COLUMN_COUNT
        self.y=(self.y+self.dy)%ROW_COUNT
        self.snake.append((self.x, self.y))
    def moving2(self):
        self.snake.pop(0)
# We create a class for the apple
class Apple:
    x = 5
    y = 4
    def new_apple(self):
        self.x = random.randint(0, COLUMN_COUNT-1)
        self.y = random.randint(0, ROW_COUNT-1)

class MyGame(arcade.Window):
    #Let's initate the window of the game
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.player = Player()
        self.grid = []
        self.apple = Apple()
        self.game_over = False
        self.text_angle = 0
        self.time_elapsed = 0.0
        self.draw_time = 0
        self.shape_list = None
    
    def on_update(self,dt=0.0001):
        self.player.moving1()
        self.player.K = True 
        if len(self.player.snake) != len(set(self.player.snake)):
            self.game_over = True
        if not(self.game_over):
            self.shape_list = arcade.ShapeElementList()
            if (self.player.x, self.player.y)==(self.apple.x, self.apple.y):
                while (self.apple.x, self.apple.y) in self.player.snake:
                    self.apple.new_apple()
                self.player.speed=self.player.speed+0.2
                self.player.points=self.player.points+1
            else:
                self.player.moving2()
            point_list = []
            color_list = [] 
            for (i,j) in self.player.snake:
                x = (MARGIN + WIDTH) * i + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * j + MARGIN + HEIGHT // 2
                top_left = (x - HALF_SQUARE_WIDTH, y + HALF_SQUARE_HEIGHT)
                top_right = (x + HALF_SQUARE_WIDTH, y + HALF_SQUARE_HEIGHT)
                bottom_right = (x + HALF_SQUARE_WIDTH, y - HALF_SQUARE_HEIGHT)
                bottom_left = (x - HALF_SQUARE_WIDTH, y - HALF_SQUARE_HEIGHT)                
                point_list.append(top_left)
                point_list.append(top_right)
                point_list.append(bottom_right)
                point_list.append(bottom_left)
                for i in range(4):
                    color_list.append(arcade.color.GREEN)
            shape = arcade.create_rectangles_filled_with_colors(point_list, color_list)
            self.shape_list.append(shape)
            x = (MARGIN + WIDTH) * self.apple.x + MARGIN + WIDTH // 2 
            y= (MARGIN + HEIGHT) * self.apple.y + MARGIN + HEIGHT // 2
            shape=arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, arcade.color.RED)       
            self.shape_list.append(shape)
            arcade.pause(1/self.player.speed)
            
    def on_draw(self):
            arcade.start_render()
            # Start timing how long this takes
            draw_start_time = timeit.default_timer()
            # --- Draw all the rectangles
            self.shape_list.draw()
            output = f"Drawing time: {self.draw_time:.3f} seconds per frame."
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18)
            self.draw_time = timeit.default_timer() - draw_start_time
            if self.game_over:
                start_x = 100
                start_y = 100
                arcade.draw_text("GAME OVER", start_x, start_y, arcade.color.WHITE, 15)
                start_x = 100
                start_y = 150
                arcade.draw_text("POINTS= " + str(self.apple.points), start_x, start_y, arcade.color.WHITE ,15 )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT and self.player.K:
            self.player.change_velocity_Left()
            self.player.K = False
        elif key == arcade.key.RIGHT and self.player.K:
            self.player.change_velocity_Right()
            self.player.K = False
        elif key == arcade.key.UP and self.player.K:
            self.player.change_velocity_Up()
            self.player.K = False
        elif key == arcade.key.DOWN and self.player.K:
            self.player.change_velocity_Down()
            self.player.K = False


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
if __name__ == "__main__":
    main()
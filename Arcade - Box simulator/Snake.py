import arcade
import random
import timeit
#Size of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "BOX"
# Timestep for the calculations
dt=0.001
# Bound for stopping loops
eps=0.0001
# Gravity 
g=9.8
class Box:
    x = SCREEN_WIDTH/4
    y = SCREEN_HEIGHT/2
    velocity=0
    def __init__(self, size, mass, mu):
        self.mass=mass
        self.size=size
        self.mu=mu
    def update_position(self, dt):
        if (self.velocity>eps):
            self.velocity=self.velocity-g*self.mu*dt
        self.x=self.x+self.velocity*dt

class Bullet:
    r = 5
    y = (SCREEN_HEIGHT+20) / 2
    x = 0
    collided = False
    def __init__(self, velocity, mass):
        self.velocity=velocity
        self.mass = mass
    def update_position(self,dt):
        self.x=self.x+self.velocity*dt

def check_collision (bullet, box, eps):
    if (box.x-box.size/2-bullet.r-bullet.x<eps) and not(bullet.collided):
        box.mass=box.mass+bullet.mass
        box.velocity=(bullet.mass*bullet.velocity)/(box.mass+bullet.mass)
        bullet.collided = True
    elif(box.x-box.size/2-bullet.r-bullet.x<2*eps) and bullet.collided:
        bullet.x=box.x-box.size/2-bullet.r

class Values(arcade.Window):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Insert the values for the bullet on the terminal. Then click to continue.", SCREEN_WIDTH/2, SCREEN_WIDTH/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        mass_bullet = float(input('Introduce the mass of the bullet: '))
        velocity_bullet = float(input('Introduce the velocity of the bullet: '))

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        mygame = MyGame()
        self.window.show_view(mygame)

class MyGame(arcade.Window):
    #Let's initate the window of the game
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.box = Box(60,random.randint(0,1000),0.6)
        self.shape_list=[]
        self.bullet = Bullet(velocity_bullet, mass_bullet)
    def on_update(self,dt=0.01):
        # if self.box.velocity<eps and self.bullet.collided:
        #     # mass_bullet= int(input('Mass bullet: '))
        #     # velocity_bullet= int(input('Velocity bullet: ' ))
        check_collision(self.bullet,self.box,dt)
        self.box.update_position(dt)
        self.bullet.update_position(dt)
        self.shape_list = arcade.ShapeElementList()
        x = self.box.x
        y = self.box.y
        shape=arcade.create_rectangle_filled(x, y, self.box.size, self.box.size, arcade.color.WHITE)
        self.shape_list.append(shape)      
        x = self.bullet.x 
        y = self.bullet.y
        shape=arcade.create_ellipse_filled (x, y, self.bullet.r, self.bullet.r, arcade.color.YELLOW)     
        self.shape_list.append(shape)

    def on_draw(self):
            arcade.start_render()
            # Start timing how long this takes
            draw_start_time = timeit.default_timer()
            # --- Draw all the rectangles
            self.shape_list.draw()
            output = f"Drawing time: {self.draw_time:.3f} seconds per frame."
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18)
            self.draw_time = timeit.default_timer() - draw_start_time
def main():
    Values(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
if __name__ == "__main__":
    main()

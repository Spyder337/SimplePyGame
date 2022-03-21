import sys
import time
from random import randint

from pygame.locals import *

from game_object import *
from shapes import *

BoundsX = 0
BoundsY = 0
GameObjects = {}
RemovalList = []


#   Remember always need self.attrName to access class attributes
#   Class for handling window management and game loop logic
#   May partition the game loop to its own class
class Window:
    display_surf = None  # Main canvas for the window
    world_objects = None

    # Color       R    G    B    A
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 50)
    GREEN = (0, 255, 0, 150)
    BLUE = (0, 0, 255, 150)

    init_time = time.process_time()

    def __init__(self, name, height, width):
        pygame.init()
        self.display_surf = pygame.display.set_mode((width, height))
        self.display_surf.fill(self.WHITE)
        window.BoundsX = self.display_surf.get_width()
        window.BoundsY = self.display_surf.get_height()
        pygame.display.set_caption(name)
        self.init_scene()

    def init_scene(self):
        circle = Circle(self.BLUE, 100, (200, 200))
        poly = Polygon(self.GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)), (400, 400))
        rect = Rectangle(self.RED, (400, 400), (0, 0, 200, 200))
        sprite = Sprite((0, 0, 0), (400, 400), "sprites/fireball.png")
        self.create_game_obj("circle", circle, None)
        self.create_game_obj("polygon", poly, None)
        self.create_game_obj("rectangle", rect, None, invulnerable=True)
        self.create_game_obj("static_sprite", sprite, (0, 0), True, True, 10, True, True, 1.0)

    # Start the game loop
    # Loop => Input -> Physics -> Render
    def start(self):
        init_time = time.process_time()
        while True:
            self.display_surf.fill(self.WHITE)  # Reset the render canvas
            for event in pygame.event.get():  # Iterate over events
                if event.type == QUIT:  # Clicking X button
                    pygame.quit()
                    sys.exit()
            self.update()  # Handle updates to game objects
            pygame.display.update()  # Update the display

    def update(self):
        elapsed = time.process_time() - self.init_time
        for id in GameObjects:  # Iterate over objects
            GameObjects[id].update(self.display_surf)  # Update the object

            if not GameObjects[id].is_alive:
                window.RemovalList.append(id)

            else:
                if elapsed > 3:
                    self.init_time = time.process_time()
                    print(GameObjects[id].to_string())

        for id in window.RemovalList:
            if not GameObjects[id].is_alive:
                del GameObjects[id]

        window.RemovalList = []

    def add_shape(self, id, shape):
        self.shapes[id] = shape

    def create_game_obj(self, id, prim, vel=None, isSprite=False, isStatic=False, scale=1, invulnerable=False,
                        canDamage=False, damage=0.0):
        if vel is None:
            vel_x = randint(1, 3)
            vel_y = randint(1, 3)
            vel = (vel_x, vel_y)
        game_obj = GameObject(id, prim, self.display_surf, vel, isSprite, isStatic, scale, invulnerable, canDamage,
                              damage)  # Instantiate the game object
        GameObjects[id] = game_obj  # Add the object to the dict of objects

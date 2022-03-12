import pygame,sys
from pygame.locals import *

from shapes import *
from game_object import *

#   Remember always need self.attrName to access class attributes
#   Class for handling window management and game loop logic
#   May partition the game loop to its own class
class Window:
    display_surf = None
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 50)
    GREEN = (0, 255, 0, 150)
    BLUE = (0, 0, 255, 150)

    def __init__(self, name, height, width):
        pygame.init()
        self.display_surf = pygame.display.set_mode((width, height))
        self.display_surf.fill(self.WHITE)
        pygame.display.set_caption(name)
        self.init_scene()

    def init_scene(self):
        self.shapes = {}
        self.game_objs = {}
        circle = Circle(self.BLUE, 100, (200, 200))
        poly = Polygon(self.GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)), (400, 400))
        rect = Rectangle(self.RED, (400, 400), (0, 0, 200, 200))
        self.addShape("circ1", circle)
        self.addShape("poly1", poly)
        self.addShape("rect1", rect)
        self.createGameObj("circle", circle)
        self.createGameObj("polygon", poly)
        self.createGameObj("rectangle", rect)

    # Start the game loop
    # Loop => Input -> Physics -> Render
    def start(self):
        while True:
            self.display_surf.fill(self.WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            pygame.display.update()

    def update(self):
        for id in self.game_objs:
            if(not self.game_objs[id].do_update):
                continue
            self.game_objs[id].update(self.display_surf)

    def draw(self):
        for id in self.shapes:
            if(not self.shapes[id].do_update):
                continue
            print("Shape: " + id)
            print("Color: " + str(self.shapes[id].color))
            print("Pos: " + str(self.shapes[id].pos))
            print()
            self.shapes[id].draw(self.display_surf)

    def addShape(self, id, shape):
        self.shapes[id] = shape

    def createGameObj(self, id, prim):
        gameObj = GameObject(prim)
        self.game_objs[id] = gameObj

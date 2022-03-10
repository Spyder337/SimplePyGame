import pygame,sys
from pygame.locals import *

from shapes import *

#   Remember always need self.attrName to access class attributes
#   Class for handling window management and game loop logic
#   May partition the game loop to its own class
class Window:
    DISPLAYSURF = None
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 10)
    BLUE = (0, 0, 255, 255)

    def __init__(self, name, height, width):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.shapes = []
        self.addShape(Polygon(self.GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106))))

    # Start the game loop
    # Loop => Input -> Physics -> Render
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw()
            pygame.display.update()

    def draw(self):
        for shape in self.shapes:
            shape.draw(self.DISPLAYSURF)

    def addShape(self, shape):
        self.shapes.append(shape)

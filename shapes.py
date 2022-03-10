import pygame
import Primitives.primitive as primitive


class Primitive:

    def __init__(self, displaysurf, color):
        self.displaysurf = displaysurf
        self.color = color

    def draw(self):
        pass


class Polygon(Primitive):

    def __init__(self, displaysurf, color, points):
        self.points = points
        super(Polygon, self).__init__(displaysurf, color)

    def draw(self):
        pygame.draw.polygon(self.displaysurf, self.color, self.points)

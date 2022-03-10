import pygame

import Primitives.primitive as primitive


class Polygon(primitive.Primitive):

    def __init__(self, displaysurf, color, points):
        self.points = points
        super(Polygon, self).__init__(displaysurf, color)

    def draw(self):
        pygame.draw.polygon(self.displaysurf, self.color, self.points)

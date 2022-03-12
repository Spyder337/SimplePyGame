import pygame

#   Base class for primitives
class Primitive:

    def __init__(self, color, pos):
        self.shape_surf = None          #   The surface the primitive is drawn to
        self.color = color              #   The color of the primitive
        self.do_update = True           #   Should the primitive be redrawn
        self.pos = pos                  #   Location on screen

    #   Used for draw calls
    #   Does nothing
    def draw(self, display_surf):
        pass

    #   Used for moving the object
    def updatePos(self, newPos):
        self.do_update = True
        pass

class Polygon(Primitive):

    def __init__(self, color, points, pos):
        self.points = points
        super(Polygon, self).__init__(color, pos)
        lx, ly = zip(*self.points)                                                                                  #   Get list of x and y coords
        self.min_x, self.min_y, self.max_x, self.max_y = min(lx), min(ly), max(lx), max(ly)                         #   Find the bounds
        self.target_rect = pygame.Rect(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)    #   Create a rectangle with the bounds
        self.target_rect.center = self.pos                                                                          #   Place the new rectangle at the position
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)                                    #   Create the surface for the primitive

    def draw(self, display_surf):
        pygame.draw.polygon(self.shape_surf, self.color, [(x - self.min_x, y - self.min_y) for x, y in self.points])    #   Loop through coords and get new positions
        display_surf.blit(self.shape_surf, self.target_rect)                                                            #   Blend the primitive's surface and the display one
        self.do_update = False                                                                                          #   Do not redraw it by default

    def updatePos(self, newPos):
        self.pos = newPos
        self.target_rect.center = self.pos

class Circle(Primitive):

    def __init__(self, color, radius, pos):
        self.radius = radius
        super().__init__(color, pos)
        #   Generate a rectangle that contains the circle
        #   Used in generating the shape_surf
        self.target_rect = pygame.Rect(self.pos, (radius * 2, radius * 2))
        self.target_rect.center = self.pos
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)

    def draw(self, display_surf):
        pygame.draw.circle(self.shape_surf, self.color, (self.radius, self.radius), self.radius)
        display_surf.blit(self.shape_surf, self.target_rect)
        self.do_update = False

    def updatePos(self, newPos):
        self.pos = newPos
        self.target_rect.center = self.pos

class Rectangle(Primitive):

    def __init__(self, color, pos, rect):
        super().__init__(color, pos)
        self.target_rect = pygame.Rect(rect)
        self.target_rect.center = self.pos
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)

    def draw(self, display_surf):
        pygame.draw.rect(self.shape_surf, self.color, self.shape_surf.get_rect())
        display_surf.blit(self.shape_surf, self.target_rect)
        self.do_update = False
        
    def updatePos(self, newPos):
        self.pos = newPos
        self.target_rect.center = self.pos

import pygame

#   Base class for primitives
class Primitive:

    def __init__(self, color, pos):
        self.shape_surf = None
        self.color = color
        self.do_update = True
        self.pos = pos

    #   Used for draw calls
    #   Does nothing
    def draw(self, display_surf):
        pass

    def updatePos(self, newPos):
        pass


class Polygon(Primitive):

    def __init__(self, color, points, pos):
        self.points = points
        super(Polygon, self).__init__(color, pos)
        lx, ly = zip(*self.points)
        self.min_x, self.min_y, self.max_x, self.max_y = min(lx), min(ly), max(lx), max(ly)
        self.target_rect = pygame.Rect(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)
        self.target_rect.center = self.pos
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)
        self.shape_surf.set_alpha(color[3])

    def draw(self, display_surf):
        pygame.draw.polygon(self.shape_surf, self.color, [(x - self.min_x, y - self.min_y) for x, y in self.points])
        display_surf.blit(self.shape_surf, self.target_rect)
        self.do_update = False

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

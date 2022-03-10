import pygame


class Primitive:

    def __init__(self, color):
        self.shape_surf = None
        self.shape = None
        self.color = color

    def draw(self, display_surf):
        pass


class Polygon(Primitive):

    def __init__(self, color, points):
        self.points = points
        super(Polygon, self).__init__(color)
        lx, ly = zip(*self.points)
        self.min_x, self.min_y, self.max_x, self.max_y = min(lx), min(ly), max(lx), max(ly)
        self.target_rect = pygame.Rect(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)

    def draw(self, display_surf):
        pygame.draw.polygon(self.shape_surf, self.color, [(x - self.min_x, y - self.min_y) for x, y in self.points])
        display_surf.blit(self.shape_surf, self.target_rect)

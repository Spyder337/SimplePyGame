import pygame

#   Base class for primitives
class Primitive:

    shape_surf = None
    rect = None

    def __init__(self, color, pos):
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
        pos = newPos

    def scalePrimitive(self, display_surf, scale):
        print(str(self.shape_surf.get_rect().size))
        self.shape_surf = pygame.transform.rotozoom(self.shape_surf, 0, scale).convert_alpha()
        self.rect = self.shape_surf.get_rect()
        print(str(self.shape_surf.get_rect().size))
        self.rect.center = self.pos

class Sprite(Primitive):
    imagePath = ""

    def __init__(self, color, pos, imagePath):
        self.imagePath = imagePath
        self.shape_surf = pygame.image.load(self.imagePath).convert_alpha()
        self.shape_surf.set_colorkey((0, 0, 0, 255))
        self.rect = self.shape_surf.get_rect()
        super().__init__(color,  pos)

    def draw(self, display_surf):
        display_surf.blit(self.shape_surf, self.pos)

    def updatePos(self, newPos):
        super().updatePos(newPos)
        self.rect.center = self.pos

    

class Polygon(Primitive):

    def __init__(self, color, points, pos):
        self.points = points
        lx, ly = zip(*self.points)                                                                                  #   Get list of x and y coords
        self.min_x, self.min_y, self.max_x, self.max_y = min(lx), min(ly), max(lx), max(ly)                         #   Find the bounds
        self.target_rect = pygame.Rect(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)    #   Create a rectangle with the bounds
        self.target_rect.center = pos                                                                               #   Place the new rectangle at the position
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)                                    #   Create the surface for the primitive
        super(Polygon, self).__init__(color, pos)

    def draw(self, display_surf):
        pygame.draw.polygon(self.shape_surf, self.color, [(x - self.min_x, y - self.min_y) for x, y in self.points])    #   Loop through coords and get new positions
        display_surf.blit(self.shape_surf, self.target_rect)                                                            #   Blend the primitive's surface and the display one
                                                                                                                        #   Do not redraw it by default

    def updatePos(self, newPos):
        self.pos = newPos
        self.target_rect.center = self.pos

class Circle(Primitive):

    def __init__(self, color, radius, pos):
        self.radius = radius
        #   Generate a rectangle that contains the circle
        #   Used in generating the shape_surf
        self.target_rect = pygame.Rect(pos, (radius * 2, radius * 2))
        self.target_rect.center = pos
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)
        super().__init__(color, pos)

    def draw(self, display_surf):
        pygame.draw.circle(self.shape_surf, self.color, (self.radius, self.radius), self.radius)
        display_surf.blit(self.shape_surf, self.target_rect)

    def updatePos(self, newPos):
        self.pos = newPos
        self.target_rect.center = self.pos

class Rectangle(Primitive):

    def __init__(self, color, pos, rect):
        self.target_rect = pygame.Rect(rect)
        self.target_rect.center = pos
        self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)
        super().__init__(color, pos)

    def draw(self, display_surf):
        pygame.draw.rect(self.shape_surf, self.color, self.shape_surf.get_rect())
        display_surf.blit(self.shape_surf, self.target_rect)
        
    def updatePos(self, newPos):
        self.pos = newPos
        self.target_rect.center = self.pos

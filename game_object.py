import window


class GameObject:
    primitive = None        #   Item to be rendered
    velocity = (1, 1)       #   Speed
    is_alive = True         #   Should it be culled
    can_collide = True      #   Can collisions occur
    do_update = True        #   Did the position or color change
    

    def __init__(self, prim):
        self.primitive = prim
        pass

    def update(self, displaySurf):
        if(self.can_collide):           #   Check if a collision check needs to happen
            self.handle_collision()
        self.move()                     #   Handle movement
        self.render(displaySurf)        #   Render the primitive

    def handle_collision(self):
        size = self.primitive.target_rect.size      #   Size of the collision box
        rect =  self.primitive.target_rect
        top = rect.top
        bottom = rect.bottom
        left = rect.left
        right = rect.right
        boundX = window.BoundsX - 5                 #   Window boundaries
        boundY = window.BoundsY - 5
        if(top < 10 or bottom > boundY):
            y = self.velocity[1] * -1
        else:
            y = self.velocity[1]
        if(left < 10 or right > boundX):
            x = self.velocity[0] * -1
        else:
            x = self.velocity[0]
        self.change_velocity(x, y)

    def change_velocity(self, x, y):
        self.velocity = (x, y)

    def move(self):
        xPos = self.primitive.pos[0]            #   Get the x position
        yPos = self.primitive.pos[1]            #   Get the y position
        xPos += self.velocity[0]                #   Modify the location by velocity
        yPos += self.velocity[1]
        self.primitive.updatePos((xPos, yPos))  #   Update the render objects position

    def render(self, displaySurf):
        self.primitive.draw(displaySurf)

    def toString(self):
        print("Pos: " + str(self.primitive.pos))
        print("Velocity: " + str(self.velocity))

class Particle(GameObject):

    life_span = 100     #   Time alive in ms

    def __init__(self, prim):
        super().__init__(prim)
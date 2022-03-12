class GameObject:
    primitive = None        #   Item to be rendered
    velocity = (1, 1)       #   Speed
    is_alive = True         #   Should it be culled
    can_collide = False     #   Can collisions occur
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
        pass

    def change_velocity(self):
        pass

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
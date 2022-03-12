class GameObject:
    primitive = None
    velocity = (1, 1)
    is_alive = True
    can_collide = False
    do_update = True

    def __init__(self, prim):
        self.primitive = prim
        pass

    def update(self, displaySurf):
        if(self.can_collide):
            self.handle_collision()
        self.move()
        self.render(displaySurf)

    def handle_collision(self):
        pass

    def change_velocity(self):
        pass

    def move(self):
        xPos = self.primitive.pos[0]
        yPos = self.primitive.pos[1]
        xPos += self.velocity[0]
        yPos += self.velocity[1]
        self.primitive.updatePos((xPos, yPos))

    def render(self, displaySurf):
        self.primitive.draw(displaySurf)

    def toString(self):
        print("Pos: " + str(self.primitive.pos))
        print("Velocity: " + str(self.velocity))

class Particle(GameObject):

    life_span = 100     #   Time alive in ms

    def __init__(self, prim):
        super().__init__(prim)
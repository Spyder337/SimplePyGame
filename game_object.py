import random
import time

import window


def get_random_velocity(max_velocity):
    x = random.randint(0, max_velocity) * (-1 if random.random() < 0.5 else 1)
    y = random.randint(0, max_velocity) * (-1 if random.random() < 0.5 else 1)
    vel = (x, y)
    return vel


def get_random_scale(max_scale):
    scale = random.randint(0, max_scale)
    return scale


def get_random_damage(max_dmg):
    dmg = random.randint(0, max_dmg)
    return dmg


def get_random_lifespan(max_lifespan):
    lifespan = random.randint(0, max_lifespan)
    return lifespan


class GameObject:
    id = ""
    primitive = None  # Item to be rendered
    velocity = (1, 1)  # Speed
    is_alive = True  # Should it be culled
    can_collide = True  # Can collisions occur
    do_update = True  # Did the position or color change
    has_sprite = False
    is_static = False  # If the object can move
    can_damage = False  # If the object can deal damage
    invulnerable = False
    damage = 0.0
    health = 10.0  # Health if the object can deal damage
    rotation = 0
    rotation_direction = 0  # The direction rotations are applied
    gravity = False  # Should gravity be applied
    gravitationalForce = (0, 1)  # Gravitational forces
    display = None

    def __init__(self, id, prim, display_surf, velocity=(1, 1), has_sprite=False, is_static=False, scale=1.0,
                 invulnerable=False, can_damage=False, damage=0.0):
        self.id = id
        self.primitive = prim
        self.primitive.scale_primitive(display_surf, scale)
        self.velocity = velocity
        self.has_sprite = has_sprite
        self.is_static = is_static
        self.can_damage = can_damage
        self.has_collided = False
        self.invulnerable = invulnerable
        self.collisions = []
        self.damage = damage

    def update(self, display_surf):
        if not self.is_alive:
            return

        if not self.is_static:

            if self.can_collide:  # Check if a collision check needs to happen
                self.update_collisions()  # Check for any collisions
                self.handle_collision()  # Iterate through the collisions and handle them
            self.move()  # Handle movement

        self.render(display_surf)  # Render the primitive

    def update_collisions(self):
        for id in window.GameObjects:  # Iterate through game objects
            go = window.GameObjects[id]
            if go.can_collide:  # Check if the object has collisions enabled
                if self.primitive.rect.colliderect(go.primitive.rect):
                    self.collisions.append(go)  # If a collision occurs add it to a list of collisions
                    self.has_collided = True

    def handle_collision(self):
        if self.has_collided:  # If collision occured
            for col in self.collisions:
                self.on_collide(col)  # evaluate collision
        self.window_collision()
        self.has_collided = False
        self.collisions = []

    def on_collide(self, target_game_obj):
        if self.can_damage:  # Can the object damage what it collided with
            if not target_game_obj.invulnerable:  # Is the object collided with invulnerable
                target_game_obj.take_dmg(self.damage)  # Apply damage

        if target_game_obj.can_damage:  # Can the target deal damage
            if not self.invulnerable:
                self.take_dmg(target_game_obj.damage)

    def take_dmg(self, dmg_amount):
        self.health -= dmg_amount
        if self.health <= 0:
            self.is_alive = False

    def window_collision(self):
        size = self.primitive.target_rect.size  # Size of the collision box
        rect = self.primitive.target_rect
        top = rect.top
        bottom = rect.bottom
        left = rect.left
        right = rect.right
        boundX = window.BoundsX  # Window boundaries
        boundY = window.BoundsY

        if top <= 0 or bottom >= boundY:  # Modify direction if colliding with a side
            y = self.velocity[1] * -1
        else:
            y = self.velocity[1]

        if left <= 10 or right >= boundX:  # Modift direction if colliding with top or bottom
            x = self.velocity[0] * -1
        else:
            x = self.velocity[0]

        self.change_velocity(x, y)

    def change_velocity(self, x, y):
        self.velocity = (x, y)

    def move(self):
        x_pos = self.primitive.pos[0]  # Get the x position
        y_pos = self.primitive.pos[1]  # Get the y position
        x_pos += self.velocity[0]  # Modify the location by velocity
        y_pos += self.velocity[1]
        self.primitive.update_pos((x_pos, y_pos))  # Update the render objects position
        self.do_update = True

    def render(self, displaySurf):
        self.primitive.draw(displaySurf)

    def to_string(self):
        print("Id: " + self.id)
        print("\tPos: " + str(self.primitive.pos))
        print("\tVelocity: " + str(self.velocity))
        print("\tHealth: " + str(self.health) + '\n')


class Particle(GameObject):
    life_span = 100  # Time alive in ms
    respawns = 1  # Amount of times it should be respawned

    def __init__(self, id, prim, display_surf, velocity=(1, 1), has_sprite=False, is_static=False, scale=1.0,
                 invulnerable=False, can_damage=False, damage=0.0):
        super().__init__(id, prim, display_surf, velocity, has_sprite, is_static, scale, invulnerable, can_damage,
                         damage)
        self.startTime = time.process_time()

    def update(self, display_surf):
        self.move()
        self.render(display_surf)

    def move(self):
        if self.gravity:
            pass
        else:
            super().move()

    def render(self, display_surf):
        return super().render(display_surf)


def update_lifespan(particle):                      # Called by the controller
    curr_time = time.process_time()
    elapsed_time = curr_time - particle.startTime
    if elapsed_time > particle.life_span:
        particle.is_alive = False


class ParticleController(GameObject):
    particles = []

    def __init__(self, id, prim, display_surf, size, velocity=(1, 1), has_sprite=False, is_static=False, scale=1,
                 invulnerable=False, can_damage=False, damage=0):
        super().__init__(id, prim, display_surf, velocity, has_sprite, is_static, scale, invulnerable, can_damage,
                         damage)
        self.generate_particles(size)

    def generate_particles(self, amount):
        for i in range(amount):
            vel = get_random_velocity(10)
            scale = get_random_scale(3)
            p_id = self.id + str(i)
            p = Particle(p_id, self.primitive, self.display, vel, scale=scale, invulnerable=True)
            p.life_span = get_random_lifespan(500)
            self.particles.append(p)

    def move(self):  # Disabled currently
        pass

    def update(self, display_surf):
        removals = []
        for p in self.particles:
            if not p.is_alive:
                removals.append(p)
                continue
            update_lifespan(p)
            if not p.is_alive:
                removals.append(p)
                continue
            p.update()

        for p in removals:
            self.particles.remove(p)

        removals = []

    def render(self, display_surf):  # Disabled currently
        pass

import numpy

from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3

from entity import Entity
from engine_2d import last_string_from_node
from collider import Collider

# Needs to inherit from DirectObject to receive collision notifications
class PlayerChar2D(Entity, DirectObject):
    def __init__(self, incoming_engine_ref, pos, rot, scale):
        super().__init__(incoming_engine_ref, pos, rot, scale, "egg-models/angler_fish/angler_fish.gltf", True)
        
        self.SPEED = 1.2
        self.JUMP_FORCE = 0.2
        self.FRICTION = -0.12

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.move_direction = "right"
        self.move_direction_cache = "right"
        self.is_jumping = False
        self.is_on_floor = True

        self.collider = Collider(self.engine_ref, self, "player_char_2d", Vec3(0, 0, -10), Vec3(20, 40, 25))

        self.key_map = {
            "left": False,
            "right": False
        }


        # Attach point light
        """   plight = PointLight("plight_fish")
        # plight.setShadowCaster(True, 1280, 1280)
        plight.setColor((1, 1, 1, 1))
        plnp = self.actor.attachNewNode(plight)
        plnp.setPos(1, 1, 50)
        # plight.setAttenuation((1.4, 0, 0))
        self.engine_ref.render.setLight(plnp)  """

        # Temp stuff
        self.accept_input()
        #self.mesh.setRenderModeWireframe()


        # Collision Events
        self.accept("player_char_2d-into-pier", self.on_collision_enter)
        self.accept("player_char_2d-again-pier", self.on_collision_again)
        self.accept("player_char_2d-out-pier", self.on_collision_out)

    def accept_input(self):
        # Keyboard events
        self.engine_ref.accept("arrow_left", self.update_key_map, ["left", True])
        self.engine_ref.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.engine_ref.accept("arrow_right", self.update_key_map, ["right", True])
        self.engine_ref.accept("arrow_right-up", self.update_key_map, ["right", False])
        self.engine_ref.accept("arrow_up", self.jump)

    def update_key_map(self, control_name, state):
        # This function is called when the left or right keys are pressed or released. It updates the key_map dict.
        self.key_map[control_name] = state

    def turn(self):
        self.mesh.setH(self.mesh, 180)

    def jump(self):
        if self.is_on_floor:
            self.is_on_floor = False
            self.velocity.z = self.JUMP_FORCE

    def update(self):
        super().update()

        # Zero accel each frame otherwise it would scale
        self.acceleration = Vec3(0, 0, self.engine_ref.GRAVITY)

        # Movement input
        self.move_direction_cache = self.move_direction
        if self.key_map["right"]:  # if right is True
            self.acceleration.x = self.SPEED * self.engine_ref.dt_time
            self.move_direction = "right"
        if self.key_map["left"]:  # if left is True
            self.acceleration.x = -self.SPEED * self.engine_ref.dt_time
            self.move_direction = "left"

        if self.move_direction != self.move_direction_cache:
            self.turn()

        # Calculating the position vector based on the velocity and the acceleration vectors
        self.acceleration.x += self.velocity.x * self.FRICTION  # Only add Friction to horizontal movement
        self.velocity += self.acceleration
        self.pos += self.velocity + (self.acceleration * self.engine_ref.ACCEL_MODIFIER)

        # Setting the actor's position
        self.mesh.setPos(self.pos)

        #TODO: Polish cam z movement
        #self.engine_ref.cam.setX(numpy.clip(self.pos.x, -100, 40))
        #self.engine_ref.cam.setZ(numpy.clip(self.pos.z + 1.5, -40, 40))


    # ::::::::::::::::::::::::::::::::Collision::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    def on_collision_enter(self, entry):
        self.is_on_floor = True

    def on_collision_again(self, entry):
        if last_string_from_node(entry.getIntoNodePath()) == "pier":

            self.velocity.z = 0
            self.pos.z = entry.getIntoNodePath().getPos(self.engine_ref.render).z + 3.3
            self.mesh.setPos(self.pos)

            """             if self.velocity.z < 0:  # prevent snapping to the top of the platforms
                if not self.is_jumping:
                    # TODO: find a standardized way to figure the offset for each object.
                    #  The value that is being added is hardcoded.
                   
            else:
                self.is_jumping = False """

    def on_collision_out(self, entry):
        pass



from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionBox, CollisionNode, BitMask32, Vec3
from engine_2d import *

# Auxiliary stuff for movement input
key_map = {
    "left": False,
    "right": False,
}


def update_key_map(control_name, state):
    # This function is called when the left or right keys are pressed or released. It updates the key_map dict.
    key_map[control_name] = state


class FishPlayer(DirectObject):
    def __init__(self, incoming_engine_ref: Engine2D):
        
        self.SPEED = 4
        self.JUMP_FORCE = 1.2
        self.FRICTION = -0.12

        self.engine_ref = incoming_engine_ref
        self.actor = None
        self.position = Vec3(0, 0, 18)  # This is also the initial position of the actor
        self.scale = Vec3(0.1, 0.1, 0.1)

        # Movement variables
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.move_direction = "right"
        self.move_direction_cache = "right"
        self.is_jumping = False
        self.is_on_floor = True

        # Setting the actor
        self.actor = Actor("egg-models/angler_fish/angler_fish.gltf")
        self.actor.reparentTo(self.engine_ref.render)
        self.actor.setScale(self.scale)
        self.actor.setH(self.actor, -90)
        #self.actor.loop("mill")
        #self.actor.setPlayRate(5, "mill")

        # Setting up actor collision
        collider_node = CollisionNode("fish_player")
        collider_node.setFromCollideMask(BitMask32.bit(1))
        # TODO: find a standardized way to figure the collider size for each object.
        collider_node.addSolid(CollisionBox((0, 0, 0), 30, 30, 30))
        collider = self.actor.attachNewNode(collider_node)
        self.engine_ref.cTrav.addCollider(collider, self.engine_ref.colHandlerEvent)
        if self.engine_ref.DEBUG:
            collider.show()




        plight = PointLight("plight_fish")
        # plight.setShadowCaster(True, 1280, 1280)
        plight.setColor((1, 1, 1, 1))
        plnp = self.actor.attachNewNode(plight)
        plnp.setPos(1, 1, 50)
        # plight.setAttenuation((1.4, 0, 0))
        self.engine_ref.render.setLight(plnp) 

        # Collision Events
        self.accept("fish_player-into-pier", self.on_collision_enter)
        self.accept("fish_player-again-pier", self.on_collision_again)
        self.accept("fish_player-out-pier", self.on_collision_out)
     
        # Keyboard input events
        self.engine_ref.accept("arrow_left", update_key_map, ["left", True])
        self.engine_ref.accept("arrow_left-up", update_key_map, ["left", False])
        self.engine_ref.accept("arrow_right", update_key_map, ["right", True])
        self.engine_ref.accept("arrow_right-up", update_key_map, ["right", False])
        self.engine_ref.accept("arrow_up", self.jump)

    def turn(self):
        self.actor.setH(self.actor, 180)

    def jump(self):
        if self.is_on_floor:
            self.is_on_floor = False
            self.velocity.z = self.JUMP_FORCE

    def update(self):
        # Zero accel each frame otherwise it would scale
        self.acceleration = Vec3(0, 0, self.engine_ref.GRAVITY)

        # Movement input
        self.move_direction_cache = self.move_direction
        if key_map["right"]:  # if right is True
            self.acceleration.x = self.SPEED * self.engine_ref.dt_time
            self.move_direction = "right"
        if key_map["left"]:  # if left is True
            self.acceleration.x = -self.SPEED * self.engine_ref.dt_time
            self.move_direction = "left"

        if self.move_direction != self.move_direction_cache:
            self.turn()

        # Calculating the position vector based on the velocity and the acceleration vectors
        self.acceleration.x += self.velocity.x * self.FRICTION  # Only add Friction to horizontal movement
        self.velocity += self.acceleration
        self.position += self.velocity + (self.acceleration * self.engine_ref.ACCEL_MODIFIER)

        # Setting the actor's position
        self.actor.setPos(self.position)


    # ::::::::::::::::::::::::::::::::Collision::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    def on_collision_enter(self, entry):
        self.is_on_floor = True

    def on_collision_again(self, entry):
        if last_string_from_node(entry.getIntoNodePath()) == "pier":

            self.position.z = entry.getIntoNodePath().getPos(self.engine_ref.render).z + 18
            self.velocity.z = 0  # prevent fast falling from platforms
            self.actor.setPos(self.position)

            """             if self.velocity.z < 0:  # prevent snapping to the top of the platforms
                if not self.is_jumping:
                    # TODO: find a standardized way to figure the offset for each object.
                    #  The value that is being added is hardcoded.
                   
            else:
                self.is_jumping = False """

    def on_collision_out(self, entry):
        pass



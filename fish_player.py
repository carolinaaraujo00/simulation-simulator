from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, BitMask32, Vec3
import engine_2d

# Auxiliary stuff for movement input
key_map = {
    "left": False,
    "right": False,
}


def update_key_map(control_name, state):
    # This function is called when the left or right keys are pressed or released. It updates the key_map dict.
    key_map[control_name] = state


class FishActor:
    def __init__(self, incoming_engine_ref: engine_2d.Engine2D):

        self.SPEED = 4
        self.JUMP_FORCE = 1.2
        self.FRICTION = -0.12

        self.engine_ref = incoming_engine_ref
        self.actor = None
        self.position = Vec3(0, 0, 20)  # This is also the initial position of the actor
        self.scale = Vec3(5, 5, 5)

        # Movement variables
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.move_direction = "right"
        self.move_direction_cache = "right"
        self.is_jumping = False
        self.is_on_floor = True

        # Setting the actor
        self.actor = Actor("egg-models/FishEgg/FirstFish", {"anim1": "egg-models/FishEgg/FirstFishAnim"})
        # self.actor.find("**/Object_4").node().setIntoCollideMask(BitMask32.bit(2))
        self.actor.reparentTo(self.engine_ref.render)
        self.actor.setScale(self.scale)
        self.actor.loop("anim1")
        self.actor.setPlayRate(5, 'anim1')

        # Setting up actor collision
        collider_node = CollisionNode("box-coll")
        collider_node.setFromCollideMask(BitMask32.bit(1))
        # TODO: find a standardized way to figure the collider size for each object.
        collider_node.addSolid(CollisionBox((0, 0, 0), 0.5, 0.2, 0.4))
        collider = self.actor.attachNewNode(collider_node)
        self.engine_ref.cTrav.addCollider(collider, self.engine_ref.colHandlerQueue)
        if self.engine_ref.DEBUG:
            collider.show()

        # TODO: make global input manager
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
            self.is_jumping = True
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

        # TODO: make global collision manager. This "for" loop should be in the engine
        # Handle collisions
        for entry in self.engine_ref.colHandlerQueue.getEntries():

            # inp means: into node path
            inp = entry.getIntoNodePath().getPos(self.engine_ref.render)

            if self.velocity.z < 0:  # prevent snapping to the top of the platforms
                if not self.is_jumping:
                    # TODO: find a standardized way to figure the offset for each object.
                    #  The value that is being added is hardcoded.
                    self.position.z = inp.z + 2.3
                    self.velocity.z = 0  # prevent fast falling from platforms
                    self.is_on_floor = True
            else:
                self.is_jumping = False

        # Setting the actor's position
        self.actor.setPos(self.position)

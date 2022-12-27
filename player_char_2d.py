from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3

from entity import Entity
from engine_2d import last_string_from_node
from collider import Collider
from light_setup import *
from common import * 

# Needs to inherit from DirectObject to receive collision notifications
class PlayerChar2D(Entity, DirectObject):
    def __init__(self, incoming_engine_ref, pos, rot, scale, spcl_shading):
        super().__init__(incoming_engine_ref, pos, rot, scale, "egg-models/angler_fish/angler_fish.gltf", False, spcl_shading)
        
        self.SPEED = 0.7
        self.JUMP_FORCE = 10
        self.FRICTION = -0.12

        self.beggining_pos_x = self.pos.x
        self.beggining_pos_z = self.pos.z

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.move_direction = "right"
        self.move_direction_cache = "right"
        self.is_on_floor = True
        self.floor_offset = 0.5
        self.can_move = True

        self.collider = Collider(self.engine_ref, self, "player_char_2d", Vec3(0, 0, -30), Vec3(20, 40, 25))

        self.key_map = {
            "left": False,
            "right": False
        }

        # Attach point light

        print("fish position=", self.mesh.getPos())
        self.debug_cube = self.engine_ref.loader.loadModel(cube_model_path)
        self.debug_cube.setPos((0,15,48))
        # self.debug_cube.reparentTo(self.mesh)
        self.debug_cube.reparentTo(self.engine_ref.render)
        # self.debug_cube.setScale(100)
        print(self.debug_cube.getPos())
        # setup_point_light_in_model(self.engine_ref.render, self.mesh, (self.beggining_pos_x, -30, self.beggining_pos_z))
        setup_black_point_light(self.engine_ref.render, (-50, 0, 20)) 
        setup_point_light_in_model(self.engine_ref.render, self.mesh, (0,15,48))

        self.accept_input()

        # Collision Events
        self.accept("player_char_2d-into-pier", self.on_collision_enter)
        self.accept("player_char_2d-again-pier", self.on_collision_again)
        self.accept("player_char_2d-out-pier", self.on_collision_out)

    def disable_input(self):
        self.update_key_map("left", False)
        self.update_key_map("right", False)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.can_move = False

    def accept_input(self):
        # Keyboard events
        self.engine_ref.accept("arrow_left", self.update_key_map, ["left", True])
        self.engine_ref.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.engine_ref.accept("arrow_right", self.update_key_map, ["right", True])
        self.engine_ref.accept("arrow_right-up", self.update_key_map, ["right", False])
        self.engine_ref.accept("arrow_up", self.jump)

    def update_key_map(self, control_name, state):
        if self.can_move:
            self.key_map[control_name] = state

    def turn(self):
        self.mesh.setH(self.mesh, 180)

    def jump(self):
        if self.is_on_floor and self.can_move:
            self.is_on_floor = False
            self.velocity.z = self.JUMP_FORCE

    def set_pos_on_collision(self, entry):
        if self.velocity.z < 0:
            self.velocity.z = 0
            self.pos.z = entry.getIntoNodePath().getPos(self.engine_ref.render).z + self.floor_offset
            self.mesh.setPos(self.pos)

    def update(self):
        super().update()

        # Zero accel each frame otherwise it would scale
        self.acceleration = Vec3(0, 0, self.engine_ref.GRAVITY)

        # Movement input
        self.move_direction_cache = self.move_direction
        if self.key_map["right"]:  # if right is True
            self.acceleration.x = self.SPEED
            self.move_direction = "right"
        if self.key_map["left"]:  # if left is True
            self.acceleration.x = -self.SPEED
            self.move_direction = "left"

        if self.move_direction != self.move_direction_cache:
            self.turn()

        # Calculating the position vector based on the velocity and the acceleration vectors
        self.acceleration.x += self.velocity.x * self.FRICTION  # Only add Friction to horizontal movement
        self.velocity += self.acceleration
        self.pos += (self.velocity + (self.acceleration * self.engine_ref.ACCEL_MODIFIER))* self.engine_ref.dt_time
        # print("fish pos=", self.pos)

        # Setting the actor's position
        self.mesh.setPos(self.pos)

        # Setting cam based on player
        self.engine_ref.set_cam_pos(self.pos)

        if self.pos.z < self.engine_ref.cam_z_limits[0]:
            self.pos.x = self.beggining_pos_x
            self.pos.z = self.beggining_pos_z
            
            self.mesh.setPos(self.pos)


    # ::::::::::::::::::::::::::::::::Collision::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    def on_collision_enter(self, entry):
        if last_string_from_node(entry.getIntoNodePath()) == "pier":
            self.is_on_floor = True
            self.set_pos_on_collision(entry)
        
    def on_collision_again(self, entry):
        if last_string_from_node(entry.getIntoNodePath()) == "pier":
            self.is_on_floor = True
            self.set_pos_on_collision(entry)

    def on_collision_out(self, entry):
        if last_string_from_node(entry.getIntoNodePath()) == "pier":
            self.is_on_floor = False

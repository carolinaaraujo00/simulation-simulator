from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3

from common import * 
from level_one.entity import Entity
from level_one.collider import Collider
from level_one.engine_2d import last_string_from_node
from camera_setup import *

class ShadingOrb(Entity, DirectObject):
    def __init__(self, incoming_engine_ref, sound_player, main_camera, pos, rot, scale, spcl_shading, shading_stage):
        super().__init__(incoming_engine_ref, pos, rot, scale, orb_model_path, False, spcl_shading)
        
        self.sound_player = sound_player
        self.main_camera = main_camera

        self.shading_stage = shading_stage
        collider_name = "shading_orb" + str(self.shading_stage)
        self.collider = Collider(self.engine_ref, self, collider_name, Vec3(0, 0, 0.15), Vec3(0.1, 0.1, 0.1))

        self.mesh.loadAnims({"anim1": orb_anim_model_path})
        self.mesh.loop("anim1")

        self.accept("player_char_2d-into-shading_orb0", self.on_collision_enter)
        self.accept("player_char_2d-into-shading_orb1", self.on_collision_enter)
        self.accept("player_char_2d-into-shading_orb2", self.on_collision_enter)
        self.accept("player_char_2d-into-shading_orb3", self.on_collision_enter)
        self.accept("player_char_2d-into-shading_orb4", self.on_collision_enter)
        self.accept("player_char_2d-into-shading_orb5", self.on_collision_enter)

    def on_collision_enter(self, entry):
        if last_string_from_node(entry.getFromNodePath()) == "player_char_2d":
            if entry.getIntoNodePath() == self.collider.collider:
                # Plays sound effect of orb being catched
                # Creates camera breathing effect and changes camera to opposing projection
                self.sound_player.power_up()
                self.main_camera.change_camera_ortho()
                self.main_camera.fov_breathing_effect_start()
                self.engine_ref.change_shading(self.shading_stage)
                self.mesh.cleanup()


            












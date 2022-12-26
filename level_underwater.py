from panda3d.core import Vec3

from level import Level
from engine_2d import*
from player_char_2d import*
from entity import Entity
from platform_default import PlatformDefault
from shading_orb import ShadingOrb
from sound_player import *

class LevelUnderwater(Level):
    def __init__(self, incoming_engine_ref: Engine2D, pos, rot, scale):
        super().__init__(incoming_engine_ref, pos, rot, scale)

        # 2D level position
        self.y_pos = -15
        
        # Player
        self.player_char_2d = PlayerChar2D(self.engine_ref, Vec3(-97, self.y_pos, 3), Vec3(-90, 0, 0), Vec3(0.01, 0.01, 0.01), False)
        self.add_actor(self.player_char_2d)
        self.player = self.player_char_2d

        # Setup plats
        self.platforms = []

        plat_positions = [
            Vec3(-100, self.y_pos, 0), 
            Vec3(-96.5, self.y_pos, 0), 
            Vec3(-93, self.y_pos, 0), 
            Vec3(-87, self.y_pos, 0), 

            Vec3(-83.5, self.y_pos, -2), 
            Vec3(-76.5, self.y_pos, -4), 
            Vec3(-73, self.y_pos, -4),
            Vec3(-68, self.y_pos, -4), 

            Vec3(-64.5, self.y_pos, -13), 
            Vec3(-61, self.y_pos, -13), 
            Vec3(-57.5, self.y_pos, -13), 

            Vec3(-51.5, self.y_pos, -13), 
            Vec3(-47, self.y_pos, -11.5), 
            Vec3(-51.5, self.y_pos, -10),
            Vec3(-47, self.y_pos, -8.5), 
            Vec3(-51.5, self.y_pos, -7),
            Vec3(-47, self.y_pos, -5.5), 
            Vec3(-51.5, self.y_pos, -4),
            Vec3(-47, self.y_pos, -2.5), 

            Vec3(-41, self.y_pos, -2.5), 
            Vec3(-37.5, self.y_pos, -1),
            Vec3(-34, self.y_pos, 0.5),
            Vec3(-30.5, self.y_pos, 2),
            Vec3(-27, self.y_pos, 3.5),
            Vec3(-23.5, self.y_pos, 5),

            Vec3(-20, self.y_pos, 5),
            Vec3(-16.5, self.y_pos, 5),
            Vec3(-13, self.y_pos, 5),
            Vec3(-9.5, self.y_pos, 5),
            Vec3(-6, self.y_pos, 5),

            Vec3(-16.5, self.y_pos, 6.5),
            Vec3(-13, self.y_pos, 8),
            Vec3(-9.5, self.y_pos, 6.5),

            Vec3(0.5, self.y_pos, 5),

            Vec3(4, self.y_pos, 3.5),
            Vec3(7.5, self.y_pos, 2),
            Vec3(11, self.y_pos, 2),
            Vec3(14.5, self.y_pos, 2),
            Vec3(18, self.y_pos, 2),
            Vec3(21.5, self.y_pos, 2),
            Vec3(25, self.y_pos, 3.5),

            Vec3(4, self.y_pos, 6.5),
            Vec3(7.5, self.y_pos, 8),
            Vec3(11, self.y_pos, 8),
            Vec3(14.5, self.y_pos, 8),
            Vec3(18, self.y_pos, 8),
            Vec3(21.5, self.y_pos, 8),
            Vec3(25, self.y_pos, 6.5),

            Vec3(14.5, self.y_pos, 5),
            Vec3(18, self.y_pos, 5),
            Vec3(21.5, self.y_pos, 5),
            Vec3(28.5, self.y_pos, 5),

            Vec3(34, self.y_pos, 6.5), 
            Vec3(39.5, self.y_pos, 8), 
            Vec3(45, self.y_pos, 9.5),
            Vec3(48.5, self.y_pos, 9.5),
            Vec3(52, self.y_pos, 9.5)
        ]

        # Create plats
        for pos in plat_positions:
            self.platforms.append(PlatformDefault(self.engine_ref, pos, Vec3(0, 0, 0), Vec3(1, 1 ,1), False))
            self.add_actor(self.platforms[-1])

        # Orbs
        self.orbs = []

        orb_positions = [
            Vec3(-60, self.y_pos, -5.5),
            Vec3(-10.2, self.y_pos, 9.5),
            Vec3(17, self.y_pos, 5.8), 
            Vec3(55, self.y_pos, 9.8)
        ]

        # Add sounds
        self.sound_player = SoundPlayer(self.engine_ref)
        self.sound_player.init_level1_sounds()

        for index, pos in enumerate(orb_positions):
            self.orbs.append(ShadingOrb(self.engine_ref, self.sound_player, orb_positions[index], Vec3(45, 45, 45), Vec3(2, 2, 2), True, index + 2))
            self.add_actor(self.orbs[-1])

        # Background
        self.fossil = Entity(self.engine_ref, Vec3(0, 100, 0), Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5), "egg-models/underwater_environment/fossil.gltf", True, False)
        self.add_actor(self.fossil)
        self.background_albedo = Entity(self.engine_ref, Vec3(-80, 350, -30), Vec3(-90, 0, 0), Vec3(2, 2.2, 2), "egg-models/background_sea.gltf", True, False)
        self.add_actor(self.background_albedo)
        self.background_alpha = Entity(self.engine_ref, Vec3(0, 200, 50), Vec3(-90, 0, 0), Vec3(1.5, 1.5, 1.5), "egg-models/background_sea_shading.gltf", True, False)
        self.add_actor(self.background_alpha)

        self.toggle_background(False)

    def toggle_background(self, toggle):
        if toggle:
            self.fossil.toggle_visibility(True)
            self.background_albedo.toggle_visibility(True)
            self.background_alpha.toggle_visibility(True)
        else:
            self.fossil.toggle_visibility(False)
            self.background_albedo.toggle_visibility(False)
            self.background_alpha.toggle_visibility(False)

    def update(self):
        super().update()



from panda3d.core import Vec3

from level import Level
from engine_2d import*
from player_char_2d import*
from entity import Entity
from platform_default import PlatformDefault

class LevelUnderwater(Level):
    def __init__(self, incoming_engine_ref: Engine2D, pos, rot, scale):
        super().__init__(incoming_engine_ref, pos, rot, scale)

        
        # Player
        self.player_char_2d = PlayerChar2D(self.engine_ref, Vec3(-100, -15, 5), Vec3(-90, 0, 0), Vec3(0.01, 0.01, 0.01))
        self.actors.append(self.player_char_2d)


        # Setup plats
        posy = -15
        rot = Vec3(0, -90, -90)
        scale = Vec3(1, 1 ,1)

        self.platforms = []

        plat_positions = [
            Vec3(-100, posy, -3), 
            Vec3(-90, posy, -5), 
            Vec3(-80, posy, -7), 
            Vec3(-69, posy, -9), 
            Vec3(-58, posy, -11), 
            Vec3(-51, posy, -9), 
            Vec3(-44, posy, -7), 
            Vec3(-37, posy, -5), 
            Vec3(-30, posy, -3), 
            Vec3(-23, posy, 0), 
            Vec3(-14, posy, 2), 
            Vec3(-5, posy, 4), 
            Vec3(4, posy, 6), 
            Vec3(13, posy, 8), 
            Vec3(22, posy, 10), 
            Vec3(31, posy, 12), 
            Vec3(40, posy, 14)
        ]

        # Create plats
        for pos in plat_positions:
            self.platforms.append(PlatformDefault(self.engine_ref, pos, rot, scale))

        # Background
        self.fossil = Entity(self.engine_ref, Vec3(0, 100, 0), Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5), "egg-models/underwater_environment/fossil.gltf", True)
        self.background_albedo = Entity(self.engine_ref, Vec3(-90, 350, -30), Vec3(-90, 0, 0), Vec3(2, 2, 2), "egg-models/background_sea.gltf", True)
        self.background_alpha = Entity(self.engine_ref, Vec3(0, 200, 50), Vec3(-90, 0, 0), Vec3(1.5, 1.5, 1.5), "egg-models/background_sea_shading.gltf", True)

    def update(self):
        super().update()



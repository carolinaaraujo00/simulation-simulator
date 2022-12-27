from panda3d.core import Vec3

from level_one.entity import Entity
from level_one.engine_2d import*
from level_one.collider import Collider

class PlatformDefault(Entity):
    def __init__(self, incoming_engine_ref, pos, rot, scale, spcl_shading):
        super().__init__(incoming_engine_ref, pos, rot, scale, pier_model_path, True, spcl_shading)
        
        self.collider = Collider(self.engine_ref, self, "pier", Vec3(2.8, 0, -0.1), Vec3(1.6, 1, 0.1))

    def update(self):
        super().update()



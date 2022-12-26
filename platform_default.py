from panda3d.core import Vec3

from entity import Entity
from engine_2d import*
from collider import Collider

class PlatformDefault(Entity):
    def __init__(self, incoming_engine_ref, pos, rot, scale, spcl_shading):
        super().__init__(incoming_engine_ref, pos, rot, scale, "egg-models/pier2.gltf", True, spcl_shading)
        
        self.collider = Collider(self.engine_ref, self, "pier", Vec3(2.8, 0, -0.1), Vec3(1.6, 1, 0.1))

    def update(self):
        super().update()



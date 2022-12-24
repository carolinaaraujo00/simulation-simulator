from panda3d.core import Vec3

from entity import Entity
from engine_2d import*
from collider import Collider

class PlatformDefault(Entity):
    def __init__(self, incoming_engine_ref, pos, rot, scale):
        super().__init__(incoming_engine_ref, pos, rot, scale, "egg-models/pier/pier.gltf", True)
        
        self.collider = Collider(self.engine_ref, self, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    def update(self):
        super().update()



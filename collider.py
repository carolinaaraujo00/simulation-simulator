from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, BitMask32, Vec3
import engine_2d


class Collider:
    def __init__(self, engine_ref: engine_2d.Engine2D, entity_ref, name, offset, size):

        self.name = name
        self.offset = offset
        self.size = size

        collider_node = CollisionNode(self.name)
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(CollisionBox(offset, size.x, size.y, size.z))
        collider = entity_ref.mesh.attachNewNode(collider_node)
        engine_ref.cTrav.addCollider(collider, engine_ref.colHandlerEvent)
        if engine_ref.DEBUG:
            collider.show()
   
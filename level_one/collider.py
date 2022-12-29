from panda3d.core import CollisionBox, CollisionNode, BitMask32

from level_one.engine_2d import Engine2D


class Collider:
    def __init__(self, engine_ref: Engine2D, entity_ref, name, offset, size):

        self.name = name
        self.offset = offset
        self.size = size
        self.collider = None

        collider_node = CollisionNode(self.name)
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(CollisionBox(offset, size.x, size.y, size.z))
        self.collider = entity_ref.mesh.attachNewNode(collider_node)
        engine_ref.base.cTrav.addCollider(self.collider, engine_ref.base.colHandlerEvent)
        if engine_ref.DEBUG:
            self.collider.show()
   
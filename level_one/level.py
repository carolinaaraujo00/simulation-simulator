from panda3d.core import NodePath
from level_one.engine_2d import Engine2D 

class Level:
    def __init__(self, incoming_engine_ref: Engine2D, pos, rot, scale):

        self.engine_ref = incoming_engine_ref

        self.pos = pos
        self.rot = rot
        self.scale = scale

        self.lvl_node_path = NodePath("lvl_np")
        self.lvl_node_path.reparentTo(self.engine_ref.base.render)

        self.lvl_node_path.setPos(self.pos)
        self.lvl_node_path.setHpr(self.rot)
        self.lvl_node_path.setScale(self.scale)

        self.actors = []
        self.player = None

    def add_actor(self, new_actor):
        self.actors.append(new_actor)
        self.lvl_node_path.attachNewNode(new_actor.mesh.node())

    def toggle_background(self, toggle):
        pass

    def update(self):
        for actor in self.actors:
            actor.update()
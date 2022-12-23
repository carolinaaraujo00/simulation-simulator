from direct.actor.Actor import Actor

from engine_2d import Engine2D 


class Entity:
    def __init__(self, incoming_engine_ref: Engine2D, pos, rot, scale, model_path, model_or_actor):

        self.engine_ref = incoming_engine_ref
        self.mesh = None

        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.model_actor = model_or_actor
        self.mesh = None

        # Setting the actor
        if self.model_actor:
            self.mesh = self.engine_ref.loader.loadModel(model_path)
        else:
            self.mesh = Actor(model_path)

        self.mesh.reparentTo(self.engine_ref.render)
        self.mesh.setPos(self.pos)
        self.mesh.setH(self.mesh, self.rot.x)
        self.mesh.setP(self.mesh, self.rot.y)
        self.mesh.setR(self.mesh, self.rot.z)
        self.mesh.setScale(self.scale)

    def update(self):
        pass
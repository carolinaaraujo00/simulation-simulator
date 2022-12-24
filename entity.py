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

        self.mesh.setPos(self.pos)
        self.mesh.setHpr(self.rot)
        self.mesh.setScale(self.scale)

        #self.mesh.setTexture(self.engine_ref.alt_txtr_stage, self.engine_ref.blank_txtr)

    def toggle_visibility(self, toggle):
        if toggle:
            self.mesh.show()
        else:
            self.mesh.hide()

    def toggle_texture(self, toggle):
        if toggle:
            self.mesh.clearTexture(self.engine_ref.alt_txtr_stage)
        else:
            self.mesh.setTexture(self.engine_ref.alt_txtr_stage, self.engine_ref.blank_txtr)

    def update(self):
        pass
from direct.actor.Actor import Actor

from level_one.engine_2d import Engine2D 


class Entity:
    def __init__(self, incoming_engine_ref: Engine2D, pos, rot, scale, model_path, model_or_actor, spcl_shading):

        self.engine_ref = incoming_engine_ref
        self.mesh = None

        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.model_actor = model_or_actor
        self.spcl_shading = spcl_shading
        

        # Setting the actor
        if self.model_actor:
            self.mesh = self.engine_ref.base.loader.loadModel(model_path)
            # self.mesh.loop('animations')
            print("model")
        else:
            self.mesh = Actor(model_path)
            print("actor")
            self.mesh.loop('mill')
            # self.mesh.play('mill')
            print(self.mesh.getCurrentAnim())

        self.mesh.setPos(self.pos)
        self.mesh.setHpr(self.rot)
        self.mesh.setScale(self.scale)

        if not self.spcl_shading:
            self.toggle_texture(False)
            self.toggle_wireframe(True)

    def toggle_wireframe(self,toggle):
        if self.mesh:
            if toggle:
                self.mesh.set_render_mode_wireframe()
            else:
                self.mesh.clearRenderMode()

    def toggle_visibility(self, toggle):
        if self.mesh:
            if toggle:
                self.mesh.show()
            else:
                self.mesh.hide()

    def toggle_texture(self, toggle):
        if self.mesh:
            if toggle:
                if not self.spcl_shading:
                    self.mesh.clearTexture(self.engine_ref.alt_txtr_stage)
            else:
                self.mesh.setTexture(self.engine_ref.alt_txtr_stage, self.engine_ref.blank_txtr)

    def update(self):
        pass
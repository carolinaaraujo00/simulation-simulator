from engine_2d import Engine2D 

class Level:
    def __init__(self, incoming_engine_ref: Engine2D, pos, rot, scale):

        self.engine_ref = incoming_engine_ref

        self.pos = pos
        self.rot = rot
        self.scale = scale

        self.actors = []

    def update(self):
        for actor in self.actors:
            actor.update()
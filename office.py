from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import *
from light_setup import *
from common import *
import simplepbr

loadPrcFileData("", configVars)

class ociffer(ShowBase):
    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.actors = []

        # movement variables and key mapping 
        self.init_movement()

        setup_ambient_light(self.render)
        setup_point_light(self.render, (10, 10, 10 ))
        self.set_background_color(0, 0, 0, 1)

        self.cam.setPos(0, 0, 0)

        self.taskMgr.add(self.update, "update")
        # load models
        self.load_office()
        self.load_hands()


    def load_office(self):
        self.office_model = self.loader.loadModel(office_model_path)

        self.office_model.setScale(0.5,0.5,0.5)
        self.office_model.reparentTo(self.render)


    def load_hands(self):
        self.hands = self.loader.loadModel(hand_model_path)

        # self.hands.setPos(20, 10, 5)
        self.hands.setScale(0.3)
        self.hands.reparentTo(self.render)

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt = globalClock.getDt()
        self.check_movement()
        self.hands.setPos(self.cam, (0, 6, -3))
        self.hands.setHpr(180, 0, 0)

        return task.cont


    def init_movement(self):
        self.speed = 4
        self.angle = 0

        self.accept("a", updateKeyMap, ["left", True])
        self.accept("a-up", updateKeyMap, ["left", False])

        self.accept("d", updateKeyMap, ["right", True])
        self.accept("d-up", updateKeyMap, ["right", False])


    def check_movement(self):
        cam_pos = self.cam.getPos()

        if key_map_3d["left"]:
            cam_pos.x -= self.speed * self.dt
        if key_map_3d["right"]:
            cam_pos.x += self.speed * self.dt


        self.cam.setPos(cam_pos)
        self.hands.setPos(cam_pos + (10, 10, 0))

if __name__ == "__main__":
    game = ociffer()
    game.run()
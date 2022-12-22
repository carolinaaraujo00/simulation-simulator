from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import *
from light_setup import *
from direct.showbase.ShowBase import ShowBase
from common import *
import simplepbr


loadPrcFileData("", configVars)

class ociffer(ShowBase):
    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.set_background_color(0, 0, 0, 1)

        # load models
        self.load_office()
        self.cam.setPos(20, 10, 5)
        self.cam.lookAt(self.office_model)
        # light the scene
        setup_ambient_light(self.render)
        setup_point_light(self.render, (50, 50, 50))

    def load_office(self):
        self.office_model = self.loader.loadModel("egg-models/office_space/office.gltf")

        # self.office_model.setPos(0, 50, 0)
        self.office_model.setScale(0.5,0.5,0.5)
        self.office_model.reparentTo(self.render)

game = ociffer()
game.run()
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import *
from light_setup import *
from common import *
from office import * 

loadPrcFileData("", configVars)

# hands should be rendered under the camera, so each time the camera is moved the
# hands move accordingly


class Engine3D(ShowBase):
    # __instance = None

    # def get():
    #     if not Engine3D.__instance:
    #         Engine3D()
    #     return Engine3D.__instance


    # def __init__(self):
    #     if Engine3D.__instance:
    #         raise Exception("Engine3D class already initialised")
    #     else:
    #         Engine3D.__instance = self
    
    
    def __init__(self):
        super().__init__()
        
        self.actors = []

        # movement variables and key mapping 
        self.init_movement()


        self.cam.setPos(100, 100, 5)
        self.taskMgr.add(self.update, "update")

        game = ociffer()

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt = globalClock.getDt()
        self.check_movement()

        return task.cont


    def init_movement(self):
        self.speed = 4
        self.angle = 0

        self.accept("arrow_a", updateKeyMap, ["left", True])
        self.accept("arrow_a-up", updateKeyMap, ["left", False])

        self.accept("arrow_d", updateKeyMap, ["right", True])
        self.accept("arrow_d-up", updateKeyMap, ["right", False])


    def check_movement(self):
        cam_pos = self.cam.getPos()

        if key_map_3d["left"]:
            cam_pos.x -= self.speed * self.dt
        if key_map_3d["right"]:
            cam_pos.x += self.speed * self.dt

        self.cam.setPos(cam_pos)
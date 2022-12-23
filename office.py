import math
from direct.showbase.ShowBase import ShowBase
from direct.interval.LerpInterval import LerpHprInterval
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
        self.disable_mouse()
        self.init_movement()

        setup_ambient_light(self.render)
        setup_point_light(self.render, (10, 10, 10 ))
        self.set_background_color(0, 0, 0, 1)

        # self.cam.setPos(0, 0, 3)

        self.taskMgr.add(self.update, "update")

        self.props = self.win.getProperties()
        self.screensizeX = self.props.getXSize() / 2

        # self.cam.setPos(0, -10, 4) # X = left & right, Y = zoom, Z = Up & down.
        # self.cam.setHpr(0, -15, 0) # Heading, pitch, roll.

        # load models
        self.load_office()
        self.load_hands()
        # self.follow_camera()

    def follow_camera(self):
        self.camera_dummy_node = self.render.attachNewNode("camera_dummy_node")
        self.camera_dummy_node.setPos( 0, 0, 0)
        self.camera_dummy_node.setHpr(180, 0, 0)

        self.cam.reparentTo(self.camera_dummy_node)


    def load_office(self):
        self.office_model = self.loader.loadModel(office_model_path)

        self.office_model.setScale(0.5,0.5,0.5)
        self.office_model.reparentTo(self.render)


    def load_hands(self):
        self.hands = self.loader.loadModel(hand_model_path)
        
        self.hands.setScale(self.cam, 2)
        self.hands.reparentTo(self.render)


    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        
        self.dt = globalClock.getDt()
        self.check_movement(task)
        self.mousePosition(task)

        self.hands.setPos(self.cam, (0, 20, -10))
        self.hands.setHpr(self.cam, (180, -40, 0))
        # self.hands.setScale(self.cam, 1)

        return task.cont


    def init_movement(self):
        self.speed = 4
        self.angle = 0

        self.accept("a", updateKeyMap, ["left", True])
        self.accept("a-up", updateKeyMap, ["left", False])

        self.accept("d", updateKeyMap, ["right", True])
        self.accept("d-up", updateKeyMap, ["right", False])

        self.accept("w", updateKeyMap, ["up", True])
        self.accept("w-up", updateKeyMap, ["up", False])

        self.accept("s", updateKeyMap, ["down", True])
        self.accept("s-up", updateKeyMap, ["down", False])


    def check_movement(self, task):
        cam_pos = self.cam.getPos()

        # Converts camera rotation to a percentage of direction towards X and Y, then applies it
        # Source: https://stackoverflow.com/questions/4550315/python-convert-degrees-to-change-in-x-and-change-in-y
        speed = self.speed * self.dt
        angle = math.radians(self.cam.getH())    # Remember to convert to radians!
        
        change = [speed * math.cos(angle), speed * math.sin(angle)]
        # Debug
        # print(f"change={change[0]:.2f}, {change[1]:.2f}")

        if key_map_3d["left"]:
            cam_pos.x -= change[0]
            cam_pos.y -= change[1]
        if key_map_3d["right"]:
            cam_pos.x += change[0]
            cam_pos.y += change[1]

        if key_map_3d["up"]:
            cam_pos.y += change[0]
            cam_pos.x -= change[1]
        if key_map_3d["down"]:
            cam_pos.y -= change[0]
            cam_pos.x += change[1]

        self.cam.setPos(cam_pos)
        return task.cont


    def mousePosition(self, task):
        if not self.mouseWatcherNode.hasMouse():
            return task.cont
        
        # get the relative mouse position, 
        # its always between 1 and -1
        mpos = self.mouseWatcherNode.getMouse()

        cam_rotation_p = self.cam.getP()
        cam_rotation_h = self.cam.getH()
        # print(self.cam.getHpr())
        
        if mpos.getX() > 0.2: # and self.cam.getH() > -15:
            cam_rotation_h -= self.speed*10 * self.dt

        elif mpos.getX() < -0.2: # and self.cam.getH() < 15:
            cam_rotation_h += self.speed*10 * self.dt

        if mpos.getY() > 0.2 and self.cam.getP() < 10:
            cam_rotation_p += self.speed*10 * self.dt

        elif mpos.getY() < -0.2 and self.cam.getP() > -20:
            cam_rotation_p -= self.speed*10 * self.dt

        self.cam.setHpr((cam_rotation_h, cam_rotation_p, 0))

        return task.cont


if __name__ == "__main__":
    game = ociffer()
    game.run()
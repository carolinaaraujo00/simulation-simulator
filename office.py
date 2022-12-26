import math
from direct.showbase.ShowBase import ShowBase
from direct.interval.LerpInterval import LerpHprInterval
from panda3d.core import loadPrcFileData
from panda3d.core import *
from light_setup import *
from cockroach import *
from printer import *
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
        
        self.cam.setPos(6, 7, 4) # X = left & right, Y = zoom, Z = Up & down.
        self.cam.setHpr(140, -20, 0) # Heading, pitch, roll.

        # load models
        self.load_office()
        self.load_office_room()
        self.load_hands()
        self.setup_desk_lamp()
        self.setup_cockroach()
        self.setup_printer()


    def load_office(self):
        self.office_model = self.loader.loadModel(office_model_path)
        self.office_model.setScale(0.5,0.5,0.5)
        self.office_model.reparentTo(self.render)
        print(self.office_model.getPos())

    
    def load_office_room(self):
        self.office_room_model = self.loader.loadModel(office_room_model_path)
        self.office_room_model.setScale(0.7,0.7,0.7)
        self.office_room_model.reparentTo(self.render)
        print(self.office_room_model.getPos())

    def setup_desk_lamp(self):
        self.desk_lamp = self.loader.loadModel(lamp_model_path)
        self.desk_lamp.setScale(0.5,0.5,0.5)
        self.desk_lamp.setPos(-1.7, -0.68, 3)
        setup_red_spotlight(self.render, (-1.5, -0.21, 3), (-1.7, -0.68, 0))
        print(self.desk_lamp.getPos())

    def setup_cockroach(self):
        self.cockroach = Cockroach(self.office_model, Vec3(-4.87, 0.43, 3.4) )

    def setup_printer(self):
        printer_location = Vec3(2.5, 2.43, 3.777)
        # TODO fix
        # self.printer = self.loader.loadModel(printer_model_path)
        # self.printer.setScale(0.5,0.5,0.5)
        # self.printer.setPos(printer_location)
        # self.printer_paper = Printer(self.office_model, printer_location )

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
        self.hands.setHpr(self.cam, (180, -58, 0))
        # self.hands.setScale(self.cam, 1)
        # print("Cam=", self.cam.getPos())

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

        # Debug purposes

        self.accept("x", updateKeyMap, ["elevate", True])
        self.accept("x-up", updateKeyMap, ["elevate", False])

        self.accept("z", updateKeyMap, ["lower", True])
        self.accept("z-up", updateKeyMap, ["lower", False])


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

        # Debug
        if key_map_3d["elevate"]:
            cam_pos.z += speed
        if key_map_3d["lower"]:
            cam_pos.z -= speed

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
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from common import *
from light_setup import *
import simplepbr

from level_two.cockroach import *
from level_two.printer import *
from level_two.sound_player_two import *


loadPrcFileData("", configVars)

class ociffer(ShowBase):
    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.actors = []

        # movement variables and key mapping 
        self.disable_mouse()
        self.init_movement()

        setup_black_ambient_light(self.render)

        self.set_background_color(0, 0, 0, 1)

        self.sound_player = SoundPlayerTwo(self)
        self.sound_player.init_sounds()

        self.taskMgr.add(self.update, "update")

        self.props = self.win.getProperties()
        self.screensizeX = self.props.getXSize() / 2

        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(self.props)
        
        self.cam.setPos(6, 7, 6) # X = left & right, Y = zoom, Z = Up & down.
        self.cam.setHpr(140, -20, 0) # Heading, pitch, roll.
        self.mouse_sens = 2.5

        # load models
        self.setup_office()
        self.setup_office_room()
        self.setup_hand()
        self.setup_torch()
        self.setup_cockroach()
        self.setup_printer()
        self.setup_ceiling_lights()

        # Play Sounds
        self.sound_player.play_sounds()
        self.sound_player.play_lights_on()


    def setup_office(self):
        self.office_model = self.loader.loadModel(office_model_path)
        self.office_model.setScale(0.8)
        self.office_model.reparentTo(self.render)


    def setup_office_room(self):
        self.office_room_model = self.loader.loadModel(office_room_model_path)
        self.office_room_model.setScale(0.7)
        self.office_room_model.reparentTo(self.render)


    def setup_hand(self):
        self.hand = self.loader.loadModel(hand_model_path)
        self.hand.setScale(self.cam, 0.2)
        self.hand.reparentTo(self.render)


    def setup_torch(self):
        self.sphere = self.loader.loadModel(sphere_model_path)
        self.sphere.setScale(0.1)
        self.sphere.setPos(-3, -1, 3.7)
        self.sphere.reparentTo(self.render)

        self.torch = self.loader.loadModel(torch_model_path)
        self.torch.setPos(-3, -1, 3.25)
        self.torch.setScale(0.9)
        self.torch.reparentTo(self.render)

        setup_torch_spotlight(self.render, self.sphere, (-1.5, -0.21, 2))


    def setup_cockroach(self):
        self.cockroach = Cockroach(self.office_model, Vec3(-4.87, 0.43, 3.4))


    def setup_printer(self):
        printer_location = Vec3(-2.5, 2.43, 3.4)
        self.printer = self.loader.loadModel(printer_model_path)
        self.printer.reparentTo(self.office_model)
        self.printer.setPos(printer_location)
        self.printer_paper = Printer(self.office_model, printer_location )


    def setup_ceiling_lights(self):
        self.c_lamp = self.loader.loadModel(ceiling_lamp_model_path)
        self.c_lamp.setPos(-8, -8, 2)
        self.c_lamp.setScale(4)
        self.c_lamp.reparentTo(self.render)


    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt = globalClock.getDt()

        self.check_movement(task)
        self.mousePosition(task)
        
        self.hand.setPos(self.cam, (0.8, 5, -1.3))
        self.hand.setHpr(self.cam, (200, -45, 0))
        self.hand.setScale(self.cam, 0.2)

        return task.cont


    def init_movement(self):
        self.speed = 6
        self.angle = 0

        self.accept("a", updateKeyMap, ["left", True])
        self.accept("a-up", updateKeyMap, ["left", False])

        self.accept("d", updateKeyMap, ["right", True])
        self.accept("d-up", updateKeyMap, ["right", False])

        self.accept("w", updateKeyMap, ["up", True])
        self.accept("w-up", updateKeyMap, ["up", False])

        self.accept("s", updateKeyMap, ["down", True])
        self.accept("s-up", updateKeyMap, ["down", False])

        # Debug
        self.accept("x", updateKeyMap, ["elevate", True])
        self.accept("x-up", updateKeyMap, ["elevate", False])

        self.accept("z", updateKeyMap, ["lower", True])
        self.accept("z-up", updateKeyMap, ["lower", False])


    def check_movement(self, task):
        cam_pos = self.cam.getPos()

        speed = self.speed * self.dt
        angle = math.radians(self.cam.getH())    # Remember to convert to radians!
        
        change = [speed * math.cos(angle), speed * math.sin(angle)]

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
        mouse_pos = self.win.getPointer(0)

        win_x = self.win.getXSize() 
        win_y = self.win.getYSize() 

        x = mouse_pos.getX()
        y = mouse_pos.getY()

        # movePointer forces the pointer to that position, half win_x and half win_y (center of the screen),
        # if its not possible, it returns false
        if self.win.movePointer(0, win_x // 2, win_y // 2):

            # move the camera accordingly 
            self.cam.setH(self.cam.getH() - (x - win_x / 2) * self.mouse_sens * self.dt) 
            self.cam.setP(self.cam.getP() - (y - win_y / 2) * self.mouse_sens * self.dt)

        return task.cont

import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from common import *
from light_setup import *
import simplepbr
from direct.gui.OnscreenText import OnscreenText,TextNode
import threading

from level_two.cockroach import *
from level_two.printer import *
from level_two.sound_player_two import *
from level_two.lamp import * 

import sys


loadPrcFileData("", configVars)

class ociffer(ShowBase):
    def __init__(self, debug):
        super().__init__()
        simplepbr.init()

        self.set_background_color(0, 0, 0, 1)
        loadingText = OnscreenText("Loading...",1, fg=(1, 1, 1, 1), bg = (0, 0, 0, 1), pos=(0, 0), align=TextNode.ACenter, scale=.07, mayChange=1)
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black

        self.actors = []

        # movement variables and key mapping 
        self.disable_mouse()
        self.lock_move = True 
        self.init_movement()

        setup_black_ambient_light(self.render)


        self.sound_player = SoundPlayerTwo(self)
        self.sound_player.init_sounds()

        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)
        
        self.cam.setPos(9.20, 8.80, 6) # X = left & right, Y = zoom, Z = Up & down.
        self.cam.setHpr(140, -10, 0) # Heading, pitch, roll.
        self.mouse_sens = 2.5
        self.repeat_lights = True

        load_thread = threading.Thread(target=self.thread_function, args=())
        load_thread.start()
        load_thread.join()

        loadingText.cleanup()
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
       
        self.taskMgr.add(self.update, "update")
        
        if not debug: 
            timer = threading.Timer(7.5, self.unlock_move)
            timer.start()
        else: 
            timer = threading.Timer(2, self.unlock_move)
            timer.start()

    def unlock_move(self):
        self.lock_move = False 


    def thread_function(self):
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
        self.office_room_model.setPos(self.office_room_model.getPos() + (10, 10, 0))
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
        self.printer_paper = Printer(self.office_model, printer_location)


    def setup_ceiling_lights(self):
        self.lamp1 = Lamp(self.loader, self.render, (-4, 17, 3))
        self.lamp2 = Lamp(self.loader, self.render, (22, -3, 3))
        # middle_lamp = Lamp(self.loader, self.render, (8, 7, 3))

        self.light_timer = threading.Timer(1, self.lights_off, args=(False,))
        self.light_timer.daemon = True
        self.light_timer.start()

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt = globalClock.getDt()
        
        self.check_movement(task)
        self.mousePosition(task)

        self.hand.setPos(self.cam, (1, 1.5, -0.8))
        self.hand.setHpr(self.cam, (200, -32, 0))
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

        self.accept("escape", sys.exit)


    def mousePosition(self, task):
        mouse_pos = self.win.getPointer(0)

        win_x = self.win.getXSize() 
        win_y = self.win.getYSize() 

        x = mouse_pos.getX()
        y = mouse_pos.getY()

        if self.lock_move:
            self.win.movePointer(0, win_x // 2, win_y // 2)
            
        elif self.mouseWatcherNode.hasMouse() and not self.lock_move:
            # movePointer forces the pointer to that position, half win_x and half win_y (center of the screen),
            # if its not possible, it returns false
            if self.win.movePointer(0, win_x // 2, win_y // 2):

                # move the camera accordingly 
                self.cam.setH(self.cam.getH() - (x - win_x / 2) * self.mouse_sens * self.dt) 
                self.cam.setP(self.cam.getP() - (y - win_y / 2) * self.mouse_sens * self.dt)
        return task.cont


    def check_movement(self, task):
        if not self.lock_move:
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


    # called first, turns off the lights and immediatly after turns them on 
    def lights_off(self, repeat):
        for light in self.lamp1.lights:
            turn_off(light)

        if repeat: 
            self.repeat_lights = not self.repeat_lights

        self.light_timer = threading.Timer(0.05, self.lights_on)
        self.light_timer.daemon = True
        self.light_timer.start()



    # called 0.1 seconds after lights off and turns on the lights
    # waits another second before calling lights off again 
    def lights_on(self):
        for light in self.lamp1.lights:
            self.sound_player.play_interruptor()
            turn_on(light)

        if self.repeat_lights: 
            self.light_timer = threading.Timer(0.05, self.lights_off, args=(True,))
        
        else:
            self.light_timer = threading.Timer(2, self.lights_off, args=(False,))
            self.repeat_lights = not self.repeat_lights

        self.light_timer.daemon = True
        self.light_timer.start()
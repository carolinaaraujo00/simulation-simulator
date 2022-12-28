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
from level_two.balls import *
from panda3d.core import Material


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
        # setup_ambient_light(self.render, office_ambient_black)


        self.sound_player = SoundPlayerTwo(self)
        self.sound_player.init_sounds()

        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)
        
        self.cam.setPos(5, 4.5, 6) # X = left & right, Y = zoom, Z = Up & down.
        self.cam.setHpr(135, -10, 0) # Heading, pitch, roll.
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
        self.setup_giant_orange()
        self.setup_podium()
        self.setup_balls()
        self.setup_pig()
        self.setup_tea_glass()
        # self.render.setShaderAuto()

        # Play Sounds
        self.sound_player.play_sounds()

        # continuous light buzz sound
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
        print("hand =", self.hand.getPos())

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
        self.printer_paper = Printer(self.loader, self.office_model, printer_location )


    def setup_giant_orange(self):
        orange_location = Vec3(-3.5, 17, 2.3)
        self.orange = self.loader.loadModel(orange_map_model_path)

        # attribute grey ambient light to orange
        # Then the light that affects the model

        # setup_model_ambient_light(self.render, self.orange)
        # setup_point_light_in_model_mapping(self.hand, self.orange, Vec3(0,0,0))

        self.orange.setScale(0.2, 0.2, 0.2)
        self.orange.reparentTo(self.office_model)
        self.orange.setPos(orange_location)
        self.orange.setHpr((45, 20, 0))


    def setup_podium(self):
        self.podium = self.loader.loadModel(podium_model_path)
        self.podium.reparentTo(self.render)
        self.podium.setScale(0.35)
        self.podium.setPos(10.6, -5.8, 0)
        self.podium.setHpr((120, 0, 0))
        
        self.text_choose_ball = self.loader.loadModel(text_ball_model_path)
        self.text_choose_ball.reparentTo(self.podium)
        self.text_choose_ball.setPos(0, 0, 15)
        

        sphere = self.loader.loadModel(sphere_model_path)
        sphere.reparentTo(self.podium)
        sphere.setScale(0.1)
        sphere.setPos(-2.8, 0.8, 12)
        setup_torch_spotlight(self.render, sphere, (-1.5, -0.21, 2), True)


    def setup_balls(self):
        ball_location = Vec3(13, -6, 4.34)
        
        # flat ball
        self.flat_ball = Ball(self.loader, self.office_model, ball_location)
        self.flat_ball.create_flat_ball()

        ball_location.x += 0.55
        ball_location.y += -0.2
        self.flat_bronze_ball = Ball(self.loader, self.office_model, ball_location)
        self.flat_bronze_ball.create_flat_ball_bronze()


        # smooth ball
        ball_location = Vec3(14.3, -7, 4.34)
        self.smooth_ball = Ball(self.loader, self.office_model, ball_location)
        self.smooth_ball.create_smooth_ball()

        ball_location.x += 0.3
        ball_location.y -= -0.55
        self.smooth_bronze_ball = Ball(self.loader, self.office_model, ball_location)
        self.smooth_bronze_ball.create_smooth_ball_bronze()

        # moving ball
        ball_location = Vec3(14.3, -7, 4.34)
        self.moving_flat_ball = Ball(self.loader, self.office_model, ball_location)
        self.moving_flat_ball.create_moving_flat_ball()

        # neon ball
        ball_location = Vec3(13, -7.5, 4.34)
        ball_location.x -= -0.1
        ball_location.y += 0.1
        self.flat_neon_ball = Ball(self.loader, self.office_model, ball_location)
        self.flat_neon_ball.create_flat_ball_neon()


    def setup_pig(self):
        self.pig = self.loader.loadModel(gourand_pig_model_path)
        self.pig.setPos(-4.21, -0.03, 5.50)
        self.pig.setHpr(180,0,0)
        self.pig.setScale(0.25)
        self.pig.reparentTo(self.render)


    def setup_tea_glass(self):
        self.tea = self.loader.loadModel(cup_of_tea_model_path)
        # Glass material didn't had transparency originally
        self.glass = Material()
        self.glass_diffuse = (0.3, 0.3, 0.3, 0.3)
        self.glass.setDiffuse(self.glass_diffuse)
        material = self.tea.findMaterial("vidro")
        # Changed material and now it does
        self.tea.replaceMaterial(material, self.glass)
        self.tea.setPos(-0.1, -3.1, 2.7)
        self.tea.setScale(0.75)
        self.tea.reparentTo(self.render)


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
        
        self.text_choose_ball.lookAt(self.cam)

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
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
from level_two.balls import *


loadPrcFileData("", configVars)

class ociffer(ShowBase):
    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.set_background_color(0, 0, 0, 1)
        loadingText = OnscreenText("Loading...",1, fg=(1, 1, 1, 1), bg = (0, 0, 0, 1), pos=(0, 0), align=TextNode.ACenter, scale=.07, mayChange=1)
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black

        self.actors = []

        # movement variables and key mapping 
        self.disable_mouse()
        self.lock_mouse = True 
        self.init_movement()

        setup_black_ambient_light(self.render)


        self.sound_player = SoundPlayerTwo(self)
        self.sound_player.init_sounds()

        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)
        
        self.cam.setPos(6, 7, 6) # X = left & right, Y = zoom, Z = Up & down.
        self.cam.setHpr(140, -20, 0) # Heading, pitch, roll.
        self.mouse_sens = 2.5

        load_thread = threading.Thread(target=self.thread_function, args=())
        load_thread.start()
        load_thread.join()

        loadingText.cleanup()
        self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
       
        self.taskMgr.add(self.update, "update")
        
        timer = threading.Timer(7.5, self.unlock_mouse)
        timer.start()


    def unlock_mouse(self):
        self.lock_mouse = False 


    def thread_function(self):
        # load models
        self.setup_office()
        self.setup_office_room()
        self.setup_hand()
        self.setup_torch()
        self.setup_cockroach()
        self.setup_printer()
        self.setup_ceiling_lights()
        self.setup_balls()
        self.setup_pig()
        self.setup_tea_glass()

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
        self.printer_paper = Printer(self.loader, self.office_model, printer_location )

    def setup_giant_orange(self):
        orange_location = Vec3(-4, 7, 2)
        self.orange = self.loader.loadModel(orange_map_model_path)

        # setup_model_ambient_light(self.render, self.orange)
        # setup_point_light_in_model_mapping(self.hand, self.orange, Vec3(0,0,0))

        self.orange.setScale(0.2, 0.2, 0.2)
        self.orange.reparentTo(self.office_model)
        self.orange.setPos(orange_location)
        self.orange.setHpr((90, 20, 0))

    def setup_balls(self):
        ball_location = Vec3(-4.21, 0.375, 3.55)
        
        self.flat_ball = Ball(self.loader, self.office_model, ball_location)
        self.flat_ball.create_flat_ball()

        ball_location.z = 3.55 + 0.38
        self.flat_bronze_ball = Ball(self.loader, self.office_model, ball_location)
        self.flat_bronze_ball.create_flat_ball_bronze()

        ball_location.z = 3.55
        ball_location.y = -0.03
        self.smooth_ball = Ball(self.loader, self.office_model, ball_location)
        self.smooth_ball.create_smooth_ball()

        ball_location.z = 3.55 + 0.38
        ball_location.y = -0.03
        self.smooth_bronze_ball = Ball(self.loader, self.office_model, ball_location)
        self.smooth_bronze_ball.create_smooth_ball_bronze()

        ball_location.x = -4.88
        ball_location.y = 1.55
        self.moving_flat_ball = Ball(self.loader, self.office_model, ball_location)
        self.moving_flat_ball.create_moving_flat_ball()

        ball_location.x = -4.79
        ball_location.y = 0.66
        ball_location.z = 4.11
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
        self.tea.setPos(-0.1, -3.1, 2.7)
        # self.tea.setHpr(180,0,0)
        self.tea.setScale(0.75)
        self.tea.reparentTo(self.render)

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

        self.hand.setPos(self.cam, (0, 20, -10))
        self.hand.setHpr(self.cam, (180, -58, 0))
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
        mouse_pos = self.win.getPointer(0)

        win_x = self.win.getXSize() 
        win_y = self.win.getYSize() 

        x = mouse_pos.getX()
        y = mouse_pos.getY()

        if self.lock_mouse:
            self.win.movePointer(0, win_x // 2, win_y // 2)
            
        elif self.mouseWatcherNode.hasMouse() and not self.lock_mouse:
            # get the relative mouse position, 
            # its always between 1 and -1

            # movePointer forces the pointer to that position, half win_x and half win_y (center of the screen),
            # if its not possible, it returns false
            if self.win.movePointer(0, win_x // 2, win_y // 2):

                # move the camera accordingly 
                self.cam.setH(self.cam.getH() - (x - win_x / 2) * self.mouse_sens * self.dt) 
                self.cam.setP(self.cam.getP() - (y - win_y / 2) * self.mouse_sens * self.dt)
        return task.cont

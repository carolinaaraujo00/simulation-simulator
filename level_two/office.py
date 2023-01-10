import math

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

# Collisions
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import CollisionTube


loadPrcFileData("", configVars)

class ociffer():
    def __init__(self, base, debug):
        self.base = base
        simplepbr.init()

        self.debug = debug
        self.is_game_ready = False
        self.base.set_background_color(loading_gray)

        loadingText = OnscreenText("Simulating...", 1, scale=0.1, pos=(0, 0), align=TextNode.ACenter, mayChange=1)
        self.base.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
       

        # movement variables and key mapping 
        self.base.disable_mouse()
        self.lock_move = True 
        self.init_movement()
        self.base.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        setup_black_ambient_light(self.base.render)
        # setup_ambient_light(self.render, office_ambient_black)


        self.sound_player = SoundPlayerTwo(self.base)
        self.sound_player.init_sounds()

        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.base.win.requestProperties(self.props)
        
        self.base.cam.setPos(5, 4.5, 6) # X = left & right, Y = zoom, Z = Up & down.
        self.base.cam.setHpr(135, -10, 0) # Heading, pitch, roll.
        self.mouse_sens = 2.5
        self.repeat_lights = True

        load_thread = threading.Thread(target=self.thread_function, args=())
        load_thread.start()
        load_thread.join()

        loadingText.cleanup()
        self.base.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
       
        self.base.taskMgr.add(self.update, "update")
        
        if not self.debug: 
            timer = threading.Timer(7.5, self.unlock_move)
            timer.start()
            # self.camera_pan_out_animation()
            self.camera_credits_animation_pt1()
        else: 
            timer = threading.Timer(0.5, self.unlock_move)
            timer.start()
            self.camera_credits_animation_pt1()



    def camera_pan_out_animation(self):
        self.animation_sequence = Sequence(name="animation_cam")
        self.hand.hide()
        self.base.cam.lookAt((-2.3, -2.97, 3.9))
        self.animation_sequence.append(self.base.cam.posInterval(7, Vec3((5, 4.5, 6)), startPos=Vec3(-1.6, -2.1, 4.2)))
        self.animation_sequence.start()

    
    def unlock_move(self):
        self.lock_move = False 
        self.hand.show()

    def lock_movement(self):
        self.base.disable_mouse()
        self.lock_move = True 


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
        self.setup_telephone()
        self.setup_border_texts()
        self.setup_screen_game()
        self.setup_end_credits_button()
        # self.render.setShaderAuto()

        # Play Sounds
        self.sound_player.play_sounds()

        # continuous light buzz sound
        self.sound_player.play_lights_on() 
        self.is_game_ready = True


    def setup_office(self):
        self.office_model = self.base.loader.loadModel(office_model_path)
        self.office_model.setScale(0.8)
        self.office_model.reparentTo(self.base.render)


    def setup_office_room(self):
        self.office_room_model = self.base.loader.loadModel(office_room_model_path)
        self.office_room_model.setPos(self.office_room_model.getPos() + (10, 10, 0))
        self.office_room_model.setScale(0.7)
        self.office_room_model.reparentTo(self.base.render)


    def setup_hand(self):
        self.hand = self.base.loader.loadModel(hand_model_path)
        self.hand.setScale(self.base.cam, 0.2)
        self.hand.reparentTo(self.base.render)
        colliderNode = CollisionNode("hand")
        # Add a collision-sphere centred on (0, 0, 0), and with a radius of 0.3
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.hand.attachNewNode(colliderNode)
        self.collider.show()


    def setup_torch(self):
        self.sphere = self.base.loader.loadModel(sphere_model_path)
        self.sphere.setScale(0.1)
        self.sphere.setPos(-3, -1, 3.7)
        self.sphere.reparentTo(self.base.render)

        self.torch = self.base.loader.loadModel(torch_model_path)
        self.torch.setPos(-3, -1, 3.25)
        self.torch.setScale(0.9)
        self.torch.reparentTo(self.base.render)

        setup_torch_spotlight(self.base.render, self.sphere, (-1.5, -0.21, 2))


    def setup_cockroach(self):
        self.cockroach = Cockroach(self.office_model, Vec3(-4.87, 0.43, 3.4))


    def setup_printer(self):
        printer_location = Vec3(-2.5, 2.43, 3.4)
        self.printer = self.base.loader.loadModel(printer_model_path)
        self.printer.reparentTo(self.office_model)
        self.printer.setPos(printer_location)
        self.printer_paper = Printer(self.base.loader, self.office_model, printer_location )


    def setup_giant_orange(self):
        orange_location = Vec3(-3.5, 17, 2.3)
        self.orange = self.base.loader.loadModel(orange_map_model_path)

        # attribute grey ambient light to orange
        # Then the light that affects the model

        # setup_model_ambient_light(self.render, self.orange)
        # setup_point_light_in_model_mapping(self.hand, self.orange, Vec3(0,0,0))

        self.orange.setScale(0.2, 0.2, 0.2)
        self.orange.reparentTo(self.office_model)
        self.orange.setPos(orange_location)
        self.orange.setHpr((45, 20, 0))


    def setup_podium(self):
        self.podium = self.base.loader.loadModel(podium_model_path)
        self.podium.reparentTo(self.base.render)
        self.podium.setScale(0.2)
        self.podium.setPos(14, -2.5, 0)
        self.podium.setHpr((-120, 0, 0))
        
        self.text_choose_ball = self.base.loader.loadModel(text_ball_model_path)
        self.text_choose_ball.reparentTo(self.podium)
        self.text_choose_ball.setScale(1.5)
        self.text_choose_ball.setPos(9.8, 6.2, 23)
        

        sphere = self.base.loader.loadModel(sphere_model_path)
        sphere.reparentTo(self.podium)
        sphere.setScale(0.07)
        sphere.setPos(15.6, 6.2, 16.8)
        # sphere.setPos(13, -8, 5)
        setup_torch_spotlight(self.base.render, sphere, (-1.5, -0.21, 2), True)


    def setup_balls(self):
        ball_location = Vec3(16.3, -6.1, 2.95)
        ball_text_location = Vec3(16.3, -6.1, 2.67)

        # Text Loaders
        self.flat_shading = self.base.loader.loadModel(flat_shading_model_path)
        self.flat_shading_move = self.base.loader.loadModel(flat_shading_model_path)
        self.phong_shading = self.base.loader.loadModel(phong_shading_model_path)
        self.neon_shading = self.base.loader.loadModel(neon_shading_model_path)

        # flat ball
        self.flat_bronze_ball = Ball(self.base.loader, self.office_model, ball_location)
        self.flat_bronze_ball.create_flat_ball_bronze()
 
        ball_location.x += 0.6
        ball_location.y += -0.4
        self.flat_ball = Ball(self.base.loader, self.office_model, ball_location)
        self.flat_ball.create_flat_ball()

        # Flat Balls Text
        ball_text_location = Vec3(18.2, -6.7, 2.67)
        ball_text_location.x += -0.5
        ball_text_location.y += 0.5
        self.flat_shading.setScale(0.1)
        self.flat_shading.setHpr(160, 0, 0)
        self.flat_shading.reparentTo(self.office_model)
        self.flat_shading.setPos(ball_text_location)




        # smooth ball
        ball_location = Vec3(18.2, -6.7, 2.95)
        ball_location.x += -0.5
        ball_location.y += 1
        self.smooth_bronze_ball = Ball(self.base.loader, self.office_model, ball_location)
        self.smooth_bronze_ball.create_smooth_ball_bronze()

        ball_location.x += 0.8
        ball_location.y += 0.4
        self.smooth_ball = Ball(self.base.loader, self.office_model, ball_location)
        self.smooth_ball.create_smooth_ball()

        # Phong Balls Text
        ball_text_location.x += 0.24
        ball_text_location.y += 1.1
        self.phong_shading.setScale(0.1)
        self.phong_shading.setHpr(200, 0, 0)
        self.phong_shading.reparentTo(self.office_model)
        self.phong_shading.setPos(ball_text_location)




        # moving ball
        ball_location = Vec3(14.3, -7, 4.34)
        self.moving_flat_ball = Ball(self.base.loader, self.office_model, ball_location)
        self.moving_flat_ball.create_moving_flat_ball()

        # Flat Balls Moving Text
        ball_text_location = Vec3(-2.93, -0.5, 3.45)
        self.flat_shading_move.setScale(0.1)
        self.flat_shading_move.setHpr(90,0,0)
        self.flat_shading_move.reparentTo(self.office_model)
        self.flat_shading_move.setPos(ball_text_location)




        # neon ball
        ball_location = Vec3(18.2, -6.7, 2.95)
        self.flat_neon_ball = Ball(self.base.loader, self.office_model, ball_location)
        self.flat_neon_ball.create_flat_ball_neon()

        # Neon Shading Text
        ball_text_location = Vec3(18.2, -6.7, 2.67)
        ball_text_location.x += -0.2
        ball_text_location.y += 0.2
        self.neon_shading.setScale(0.08)
        self.neon_shading.setHpr(120,0,0)
        self.neon_shading.reparentTo(self.office_model)
        self.neon_shading.setPos(ball_text_location)
        

    def setup_border_texts(self):
        self.border_texts = [] 
        self.border_texts.append(self.base.loader.loadModel(the_end_model_path))
        self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))
        # self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))
        self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))

        self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))
        self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))
        self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))
        self.border_texts.append(self.base.loader.loadModel(text_escape_model_path))

        self.border_limites = [] 

        self.border_limites.append(Vec3(-20,-20,6))
        self.border_limites.append(Vec3(20,-20,6))
        # self.border_limites.append(Vec3(20,20,6))
        self.border_limites.append(Vec3(-20,20,6))
        self.border_limites.append(Vec3(-50,-50,6))
        self.border_limites.append(Vec3(50,-50,6))
        self.border_limites.append(Vec3(60,60,6))
        self.border_limites.append(Vec3(-50,50,6))

        border_counter = 0
        for text in self.border_texts:
            text.setScale(1)
            text.reparentTo(self.base.render)
            text.setPos(self.border_limites[border_counter])
            border_counter += 1


    def setup_screen_game(self):
        self.angler_fish = self.base.loader.loadModel(angler_fish_model_path)
        self.angler_fish.setPos((-2.3, -2.43, 4.0))
        self.angler_fish.setHpr((45, 0, 0))
        self.angler_fish.setScale((0.002))
        self.angler_fish.reparentTo(self.base.render)

        self.fossil = self.base.loader.loadModel(fossil_model_path)
        self.fossil.setPos((-2.35, -2.98, 3.75))
        self.fossil.setHpr((138, 0, 0))
        self.fossil.setScale((0.0026,0.0022,0.0022))
        self.fossil.reparentTo(self.base.render)

        self.background_albedo = self.base.loader.loadModel(background_sea_model_path)
        self.background_albedo.setPos((-3.2,-4.35, 4.8))
        self.background_albedo.setHpr((48, 0, 0))
        self.background_albedo.setScale((0.0071, 0.0071,0.0082))
        self.background_albedo.reparentTo(self.office_model)

        screen_sphere = self.base.loader.loadModel(sphere_model_path)
        screen_sphere.reparentTo(self.office_model)
        screen_sphere.setScale(0.07)
        screen_sphere.setPos(-2.50,-3.28, 5.99)
        setup_torch_spotlight(self.base.render, screen_sphere, (0,0,0), True)


    def setup_pig(self):
        self.pig = self.base.loader.loadModel(gouraud_pig_model_path)
        self.pig.setPos(-4.21, -0.03, 5.50)
        self.pig.setHpr(180,0,0)
        self.pig.setScale(0.25)
        self.pig.reparentTo(self.base.render)

        self.pig_gouraud_shading = self.base.loader.loadModel(gouraud_shading_model_path)
        self.pig_gouraud_shading.setScale(0.1)
        self.pig_gouraud_shading.setHpr(0,90,90)
        self.pig_gouraud_shading.reparentTo(self.base.render)
        self.pig_gouraud_shading.setPos((-3.90, -1.99, 5.40))


    def setup_tea_glass(self):
        self.tea = self.base.loader.loadModel(cup_of_tea_model_path)
        # Glass material didn't had transparency originally
        self.glass = Material()
        self.glass_diffuse = (0.3, 0.3, 0.3, 0.3)
        self.glass.setDiffuse(self.glass_diffuse)
        material = self.tea.findMaterial("vidro")
        # Changed material and now it does
        self.tea.replaceMaterial(material, self.glass)
        self.tea.setPos(-0.1, -3.1, 2.7)
        self.tea.setScale(0.75)
        self.tea.reparentTo(self.base.render)


    def setup_ceiling_lights(self):
        self.lamp1 = Lamp(self.base.loader, self.base.render, (-4, 17, 3))
        self.lamp2 = Lamp(self.base.loader, self.base.render, (22, -3, 3))
        # middle_lamp = Lamp(self.loader, self.render, (8, 7, 3))

        self.light_timer = threading.Timer(1, self.lights_off, args=(False,))
        self.light_timer.daemon = True
        self.light_timer.start()


    def setup_telephone(self):
        self.telephone_base = self.base.loader.loadModel(telephone_base_model_path)
        self.telephone_base.setPos(1.05, -2.6, 2.9)
        self.telephone_base.setScale(0.75)
        self.telephone_base.reparentTo(self.base.render)

        self.telephone_ring = Actor(telephone_ring_model_path, {"ring": telephone_ring_model_path})
        self.telephone_ring.loop("ring")
        self.telephone_ring.setPlayRate(1, 'ring')
        self.telephone_ring.setScale(0.75)
        self.telephone_ring.setPos(1.05, -2.45, 2.95)
        self.telephone_ring.setHpr(0, 0, 5)
        self.telephone_ring.reparentTo(self.base.render)


    def camera_credits_animation_pt1(self):
        self.hand.hide()
        self.lock_movement()
        self.animation_sequence = Sequence(name="animation_credits_cam1")
        self.animation_sequence.append(self.base.cam.posInterval(7, Vec3((55, 55, 6)), startPos=self.base.cam.getPos()))
        # self.animation_sequence.append(self.base.cam.hprInterval(1, Point3(0,0,10) , startHpr=self.base.cam.getPos()))
        self.animation_sequence.start()
        self.hand.hide()
        self.lock_movement()
        # self.hand.show()

    def setup_end_credits_button(self):
        self.credits_button = self.base.loader.loadModel(red_button_model_path)
        self.credits_button.setPos(5, 0, 2.9)
        self.credits_button.setScale(0.50)
        self.credits_button.reparentTo(self.office_model)

        self.credits_text = self.base.loader.loadModel(credits_text_model_path)
        self.credits_text.setPos(50, 50, 10)
        self.credits_text.setScale(0.50)
        self.credits_text.reparentTo(self.office_model)


        self.pusher.addCollider(self.collider, self.hand)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        self.base.cTrav.addCollider(self.collider, self.pusher)

        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        


    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt = globalClock.getDt()
        
        self.check_movement(task)
        self.mousePosition(task)

        self.hand.setPos(self.base.cam, (1, 1.5, -0.8))
        self.hand.setHpr(self.base.cam, (200, -32, 0))
        self.hand.setScale(self.base.cam, 0.2)

        return task.cont


    def init_movement(self):
        self.speed = 6
        self.angle = 0

        self.base.accept("a", updateKeyMap, ["left", True])
        self.base.accept("a-up", updateKeyMap, ["left", False])
        self.base.accept("arrow_left", updateKeyMap, ["left", True])
        self.base.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.base.accept("d", updateKeyMap, ["right", True])
        self.base.accept("d-up", updateKeyMap, ["right", False])
        self.base.accept("arrow_right", updateKeyMap, ["right", True])
        self.base.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.base.accept("w", updateKeyMap, ["up", True])
        self.base.accept("w-up", updateKeyMap, ["up", False])
        self.base.accept("arrow_up", updateKeyMap, ["up", True])
        self.base.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.base.accept("s", updateKeyMap, ["down", True])
        self.base.accept("s-up", updateKeyMap, ["down", False])
        self.base.accept("arrow_down", updateKeyMap, ["up", True])
        self.base.accept("arrow_down-up", updateKeyMap, ["up", False])

        # Debug
        if self.debug:
            self.base.accept("x", updateKeyMap, ["elevate", True])
            self.base.accept("x-up", updateKeyMap, ["elevate", False])

            self.base.accept("z", updateKeyMap, ["lower", True])
            self.base.accept("z-up", updateKeyMap, ["lower", False])

            self.base.accept("escape", sys.exit)


    def mousePosition(self, task):
        mouse_pos = self.base.win.getPointer(0)

        win_x = self.base.win.getXSize() 
        win_y = self.base.win.getYSize() 

        x = mouse_pos.getX()
        y = mouse_pos.getY()

        if self.lock_move:
            self.base.win.movePointer(0, win_x // 2, win_y // 2)
            
        elif self.base.mouseWatcherNode.hasMouse() and not self.lock_move:
            # movePointer forces the pointer to that position, half win_x and half win_y (center of the screen),
            # if its not possible, it returns false
            if self.base.win.movePointer(0, win_x // 2, win_y // 2):

                # move the camera accordingly 
                self.base.cam.setH(self.base.cam.getH() - (x - win_x / 2) * self.mouse_sens * self.dt) 
                self.base.cam.setP(self.base.cam.getP() - (y - win_y / 2) * self.mouse_sens * self.dt)  
        if self.is_game_ready:
            self.text_choose_ball.lookAt(self.base.cam)
            for text in self.border_texts:
                text.lookAt(self.base.cam)

        return task.cont


    def check_movement(self, task):
        if not self.lock_move:
            cam_pos = self.base.cam.getPos()

            speed = self.speed * self.dt
            angle = math.radians(self.base.cam.getH())    # Remember to convert to radians!
            
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

            self.base.cam.setPos(cam_pos)

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


    def run(self):
        self.base.run()
import numpy

from panda3d.core import CollisionTraverser, CollisionHandlerEvent, loadPrcFileData, TextureStage
from direct.showbase.Transitions import Transitions

import simplepbr 

from common import *
from light_setup import *


loadPrcFileData("", configVars)

# Used to parse collision by any actor that needs it
def last_string_from_node(node):
    temp_string = str(node)
    index = temp_string.rfind("/") + 1
    return temp_string[index:]

class Engine2D():
    def __init__(self, base, debug):
        # super().__init__()
        self.base = base

        simplepbr.init()

        # Consts
        self.GRAVITY = -0.5
        self.ACCEL_MODIFIER = 0.5
        self.DEBUG = debug  # Can be used to debug collisions for example
        self.cam_x_limits = [-95, 50]
        self.cam_z_limits = [-30, 30]
        self.cam_z_offset = 1.5

        # self.main_event = main_event

        # Vars
        self.dt_time = 0

        self.levels = []
        self.current_level = None

        self.cTrav = None
        self.colHandlerEvent = None

        self.fade_trans = Transitions(self.base.loader)
        self.time_to_start_fade = 1
        self.fade_time = 2

        self.alt_txtr_stage = TextureStage("custom_ts")
        self.blank_txtr = self.base.loader.loadTexture(blank_texture)

        # Init setup
        self.base.set_background_color(0.1, 0.1, 0.2, 1)
        self.base.cam.setPos(0, -30, 2)

        # Set initial fade in
        self.fade_trans.setFadeColor(0, 0, 0)
        self.fade_trans.fadeOut(0.01) # TODO: Not the best way to start with a black screen, but couldn't find easy way to do it.

        # Setting up collision vars
        self.base.cTrav = CollisionTraverser()  # VAR NEEDS TO HAVE THIS NAME. PANDA3D SHENANIGANS...
        self.base.colHandlerEvent = CollisionHandlerEvent()
        self.base.colHandlerEvent.addInPattern('%fn-into-%in')
        self.base.colHandlerEvent.addAgainPattern('%fn-again-%in')
        self.base.colHandlerEvent.addOutPattern('%fn-out-%in')

        if self.DEBUG:
            self.cTrav.showCollisions(self.base.render)

            self.base.accept("1", self.change_shading, [1])
            self.base.accept("2", self.change_shading, [2])
            self.base.accept("3", self.change_shading, [3])
            self.base.accept("4", self.change_shading, [4])
            self.base.accept("5", self.change_shading, [5])
        else:
            self.base.disable_mouse()
        

        # Tasks setup
        self.base.taskMgr.add(self.update, "update")
        self.base.taskMgr.doMethodLater(self.time_to_start_fade, self.fade_screen_in, "custom_fade")

    def set_cam_pos(self, new_pos):
        self.base.cam.setX(numpy.clip(new_pos.x, self.cam_x_limits[0], self.cam_x_limits[1]))
        self.base.cam.setZ(numpy.clip(new_pos.z + self.cam_z_offset, self.cam_z_limits[0], self.cam_z_limits[1]))

    def add_level(self, new_level):
        self.levels.append(new_level)
        self.current_level = self.levels[0]

    def change_shading(self, index):
        match index:
            case 1:
                for actor in self.current_level.actors:
                    actor.toggle_wireframe(True)

                self.current_level.toggle_background(False)
            case 2:
                for actor in self.current_level.actors:
                    actor.toggle_wireframe(False)

                setup_black_ambient_light(self.base.render)
            case 3:
                for actor in self.current_level.actors:
                    actor.toggle_wireframe(False)

                self.current_level.toggle_background(True)

                setup_blue_point_light(self.base.render, (-50, 0, 20)) 
            case 4:
                for actor in self.current_level.actors:
                    actor.toggle_wireframe(False)
                    actor.toggle_texture(True)
                
                self.current_level.toggle_background(True)
            case 5:
                self.current_level.player.disable_input()

                self.base.userExit()

            case _:
                print('Command not recognized')
    


    def fade_screen_in(self, task):
        self.fade_trans.fadeIn(self.fade_time)
        return task.done

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt_time = globalClock.getDt()     

        self.current_level.update()

        return task.cont

    def run(self):
        self.base.run()
from panda3d.core import CollisionTraverser, CollisionHandlerEvent, loadPrcFileData, TextureStage
from direct.showbase.ShowBase import ShowBase
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

class Engine2D(ShowBase):
    def __init__(self, debug):
        super().__init__()
        simplepbr.init()

        # Consts
        self.GRAVITY = -0.01
        self.ACCEL_MODIFIER = 0.5
        self.DEBUG = debug  # Can be used to debug collisions for example

        # Vars
        self.dt_time = 0

        self.levels = []
        self.current_level = None

        self.cTrav = None
        self.colHandlerEvent = None

        self.fade_trans = Transitions(self.loader)
        self.time_to_start_fade = 1
        self.fade_time = 2

        self.alt_txtr_stage = TextureStage("custom_ts")
        self.blank_txtr = self.loader.loadTexture("BlankTextr.png")

        # Init setup
        self.set_background_color(0.1, 0.1, 0.2, 1)
        self.cam.setPos(0, -30, 2)

        # Set initial fade in
        self.fade_trans.setFadeColor(0, 0, 0)
        self.fade_trans.fadeOut(0.01) # TODO: Not the best way to start with a black screen, but couldn't find easy way to do it.

        # Setting up collision vars
        self.cTrav = CollisionTraverser()  # VAR NEEDS TO HAVE THIS NAME. PANDA3D SHENANIGANS...
        if self.DEBUG:
            self.cTrav.showCollisions(self.render)

        self.colHandlerEvent = CollisionHandlerEvent()
        self.colHandlerEvent.addInPattern('%fn-into-%in')
        self.colHandlerEvent.addAgainPattern('%fn-again-%in')
        self.colHandlerEvent.addOutPattern('%fn-out-%in')

        # Shading setup
        #self.wireframe_on()

        self.accept("1", self.change_shading, [1])
        self.accept("2", self.change_shading, [2])
        self.accept("3", self.change_shading, [3])
        self.accept("4", self.change_shading, [4])

        # Tasks setup
        self.taskMgr.add(self.update, "update")
        self.taskMgr.doMethodLater(self.time_to_start_fade, self.fade_screen_in, "custom_fade")

    def add_level(self, new_level):
        self.levels.append(new_level)
        self.current_level = self.levels[0]

    def change_shading(self, index):
        match index:
            case 1:
                self.wireframe_on()
                self.current_level.toggle_background(False)
            case 2:
                self.wireframe_off()
                self.current_level.toggle_background(False)
                setup_ambient_light(self.render)
            case 3:
                self.current_level.toggle_background(True)
                setup_point_light(self.render, (-50, 0, 20)) 
            case 4:
                for actor in self.current_level.actors:
                    actor.toggle_texture(True)
            case _:
                print('Command not recognized')

    def fade_screen_in(self, task):
        self.fade_trans.fadeIn(self.fade_time)
        #self.player.accept_input()
        return task.done

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt_time = globalClock.getDt()     

        self.current_level.update()

        return task.cont

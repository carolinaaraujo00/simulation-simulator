from panda3d.core import CollisionTraverser, CollisionHandlerEvent, loadPrcFileData, CollisionNode
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
        self.cTrav = None
        self.colHandlerEvent = None
        self.fade_trans = Transitions(self.loader)
        self.time_to_start_fade = 1
        self.fade_time = 2

        # Init setup
        self.set_background_color(0.1, 0.1, 0.2, 1)
        self.cam.setPos(0, -30, 2)
        setup_ambient_light(self.render)
        #setup_point_light(self.render, (15, 0, 20)) 

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

        # Tasks setup
        self.taskMgr.add(self.update, "update")
        self.taskMgr.doMethodLater(self.time_to_start_fade, self.fade_screen_in, "custom_fade")

    def fade_screen_in(self, task):
        self.fade_trans.fadeIn(self.fade_time)
        #self.player.accept_input()
        return task.done

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt_time = globalClock.getDt()     

        # Logic Loop
        for level in self.levels:
            level.update()

        return task.cont

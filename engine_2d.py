import numpy

from panda3d.core import CollisionTraverser, CollisionHandlerEvent, loadPrcFileData, CollisionNode
from direct.showbase.ShowBase import ShowBase
import simplepbr 

from common import *
from light_setup import *


loadPrcFileData("", configVars)

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
        self.player = None
        self.actors = []
        self.cTrav = None
        self.colHandlerEvent = None

        # Init setup
        self.set_background_color(0.1, 0.1, 0.2, 1)
        self.cam.setPos(0, -30, 2)
        setup_ambient_light(self.render)
        #setup_point_light(self.render, (15, 0, 20)) 

        

        # Setting up collision vars
        self.cTrav = CollisionTraverser()  # VAR NEEDS TO HAVE THIS NAME. PANDA3D SHENANIGANS...
        if self.DEBUG:
            self.cTrav.showCollisions(self.render)

        self.colHandlerEvent = CollisionHandlerEvent()
        self.colHandlerEvent.addInPattern('%fn-into-%in')
        self.colHandlerEvent.addAgainPattern('%fn-again-%in')
        self.colHandlerEvent.addOutPattern('%fn-out-%in')


        # Adding the update aka MainLoop to the Task manager
        self.taskMgr.add(self.update, "update")

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt_time = globalClock.getDt()

        # Logic Loop
        for actor in self.actors:
            actor.update()

        self.cam.setX(numpy.clip(self.player.pos.x, -100, 40))

        #TODO: Polish z movement
        self.cam.setZ(numpy.clip(self.player.pos.z + 1.5, -100, 100))

        return task.cont

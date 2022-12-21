from direct.showbase.ShowBase import ShowBase
from common import *
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, loadPrcFileData
from light_setup import setup_point_light

loadPrcFileData("", configVars)


class Engine2D(ShowBase):
    def __init__(self):
        super().__init__()

        # Consts
        self.GRAVITY = -0.08
        self.ACCEL_MODIFIER = 0.5
        self.DEBUG = False  # Can be used to debug collisions for example

        # Vars
        self.dt_time = 0
        self.player = None
        self.actors = []
        self.cTrav = None
        self.colHandlerQueue = None

        # Init setup
        self.set_background_color(0.1, 0.1, 0.2, 1)
        self.cam.setPos(0, -65, 15)
        setup_point_light(self.render, (15, 0, 20))  # Comes from the other file

        # Setting up collision vars
        self.cTrav = CollisionTraverser()  # VAR NEEDS TO HAVE THIS NAME. PANDA3D SHENANIGANS...
        self.colHandlerQueue = CollisionHandlerQueue()

        # Adding the update aka MainLoop to the Task manager
        self.taskMgr.add(self.update, "update")

    # Called every frame
    def update(self, task):
        # globalClock is, naturally, a panda3d global, despite what the IDE might say
        self.dt_time = globalClock.getDt()

        # Logic Loop
        for actor in self.actors:
            actor.update()

        self.cam.setX(self.player.position.x)

        return task.cont

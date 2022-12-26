from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3
from direct.interval.IntervalGlobal import Sequence

from common import *


class Printer:
    def __init__(self, scene, location):
        self.actor = None   
        self.position = location  # This is also the initial position of the actor
        self.hpr = Point3(0, 0, 0)
        self.scale = Vec3(0.5, 0.5, 0.5)

        # Setting the actor
        # self.actor = Actor(paper_model_path, {"Print": paper_model_path,"Print_Floor": paper_model_path })
        self.actor = Actor(paper_model_path, {"Print_Floor": paper_model_path })
        self.actor.reparentTo(scene)
        self.actor.setPos(self.position)
        self.actor.setScale(self.scale)
        self.actor.loop("Print_Floor")
        self.actor.setPlayRate(1, 'Print_Floor')
        self.setup_animation()
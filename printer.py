from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3
from direct.interval.IntervalGlobal import Sequence

from common import *


class Printer:
    def __init__(self, scene, location):
        self.actor = None   
        self.position = location  # This is also the initial position of the actor
        self.previous_position = location  
        self.start_position = location  
        self.previous_hpr = Point3(0, 0, 0)
        self.hpr = Point3(0, 0, 0)
        self.scale = Vec3(1,1,1)


        # Setting the actor
        self.actor = Actor(paper_model_path)
        print("actor=",self.actor)
        # self.actor = Actor(paper_model_path, {"print": paper_model_path })
        # print("actor=",self.actor)
        self.actor.reparentTo(scene)
        self.actor.setPos(self.position)
        self.actor.setHpr(90,0,0)
        self.actor.setScale(self.scale)
        # self.actor.loop("print")
        # self.actor.setPlayRate(1, 'print')
        self.setup_animation()


    def setup_animation(self):
        print("self.position", self.position)
        intervals = []
        # start Vec3(-2.5, 2.43, 3.4)
        intervals.append(self.define_new_hpr_interval(0, Point3(90, 0, 0) ))
        intervals.append(self.define_new_interval(0, Vec3(-3.0, 2.5, 3.8)))
        intervals.append(self.define_new_interval(7, Vec3(-1, 2.5, 3.8)))
        intervals.append(self.define_new_interval(1, Vec3(-0.5, 2.5, 3.85)))
        intervals.append(self.define_new_interval(1, Vec3(1, 2.5, 3.85)))
        intervals.append(self.define_new_hpr_interval(0.05, Point3(95, -5, 0) ))
        intervals.append(self.define_new_interval(1, Vec3(3, 2.5, 3)))
        intervals.append(self.define_new_hpr_interval(0.1, Point3(100, 0, 0) ))
        intervals.append(self.define_new_interval(1, Vec3(2, 2.8, 2)))
        intervals.append(self.define_new_hpr_interval(0.1, Point3(105, 5, 0) ))
        intervals.append(self.define_new_interval(1, Vec3(2, 3.1, 1)))
        intervals.append(self.define_new_hpr_interval(0.1, Point3(105, 0, 0) ))
        intervals.append(self.define_new_interval(1, Vec3(1,3.3, 0.5)))
        intervals.append(self.define_new_interval(1, Vec3(1.3, 3.5, 0.28)))
        intervals.append(self.define_new_interval(1, Vec3(1.3, 3.5, 0.28)))


        self.animation_sequence = Sequence(name="animation_printer")
        
        for x in intervals:
            self.animation_sequence.append(x)

        self.animation_sequence.loop()


    def define_new_interval(self, duration, new_position):
        self.previous_position = self.position
        self.position = new_position
        posInterval = self.actor.posInterval(duration, self.position, startPos=self.previous_position)
        return posInterval


    def define_new_hpr_interval(self, duration, new_hpr):
        self.previous_hpr = self.hpr
        self.hpr = new_hpr
        hprInterval = self.actor.hprInterval(duration, self.hpr, startHpr=self.previous_hpr)
        return hprInterval

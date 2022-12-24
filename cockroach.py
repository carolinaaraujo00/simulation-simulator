from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, BitMask32, Vec3, Point3
from direct.interval.IntervalGlobal import Sequence

from common import *

class Cockroach:
    def __init__(self, scene, location):
        self.actor = None   
        self.position = location  # This is also the initial position of the actor
        self.previous_position = location  # This is also the initial position of the actor
        self.start_position = location  # This is also the initial position of the actor
        
        self.previous_hpr = Point3(0, 0, 0)
        self.hpr = Point3(0, 0, 0)

        self.scale = Vec3(0.25, 0.25, 0.25)
        # self.scale = Vec3(0.5, 0.5, 0.5)

        # Movement variables
        self.velocity = Vec3(0, 0, 0)

        # Setting the actor
        self.actor = Actor(cockroach_model_path, {"Walk": cockroach_model_path})
        # self.actor.find("**/Object_4").node().setIntoCollideMask(BitMask32.bit(2))
        self.actor.reparentTo(scene)
        self.actor.setPos(self.position)
        self.actor.setScale(self.scale)
        self.actor.loop("Walk")
        self.actor.setPlayRate(1, 'Walk')
        self.setup_animation()


    def setup_animation(self):
        # seconds, final position, start position
        print("Animation")
        print("self.position", self.position)
        intervals = []

        # start                                     Vec3(-4.6, 0.80, 3.4)
        intervals.append(self.define_new_interval(2, Vec3(-3.6, -2.35, 3.4)))
        intervals.append(self.define_new_hpr_interval(0.5, Point3(45, 0, 0) ))
        intervals.append(self.define_new_interval(0.1, Vec3(-3.6, -2.35, 3.5)))


        # starts climbing
        intervals.append(self.define_new_hpr_interval(0.1, Point3(45, -90, 0) ))
        intervals.append(self.define_new_interval(0.3, Vec3(-3.6, -2.35, 4)))
        intervals.append(self.define_new_hpr_interval(0.1, Point3(45, 0, 0) ))
        intervals.append(self.define_new_interval(0.3, Vec3(-3.35, -2.4, 4)))
        intervals.append(self.define_new_hpr_interval(0.1, Point3(45, -90, 0) ))
        intervals.append(self.define_new_interval(1, Vec3(-3.35, -2.4, 6.1)))
        intervals.append(self.define_new_hpr_interval(1, Point3(45, 0, 0) ))
        intervals.append(self.define_new_interval(1, Vec3(-2.83,-3.58, 6.1)))

        # rotation on top of pc
        intervals.append(self.define_new_hpr_interval(0.5, Point3(150, 0, 0) ))
        intervals.append(self.define_new_hpr_interval(2,Point3(150, -5, 0) ))
        intervals.append(self.define_new_hpr_interval(1,Point3(200, -5, 0) ))
        intervals.append(self.define_new_hpr_interval(1,Point3(100, -5, 0) ))
        intervals.append(self.define_new_hpr_interval(1,Point3(200, -5, 0) ))
        intervals.append(self.define_new_hpr_interval(1,Point3(150, 0, 0) ))
        intervals.append(self.define_new_hpr_interval(1,Point3(510, 0, 0) ))
        intervals.append(self.define_new_hpr_interval(1,Point3(510, 0, 0) ))

        # end
        intervals.append(self.define_new_hpr_interval(1,Point3(330, 0, 0) ))
        intervals.append(self.define_new_interval(3, Vec3(-3.65,-4.5, 6.1)))
        intervals.append(self.define_new_hpr_interval(0,Point3(0, 0, 0) ))

        self.animation_sequence = Sequence(name="animation_sequence")
        
        for x in intervals:
            self.animation_sequence.append(x)

        self.animation_sequence.loop()


    def define_new_interval(self, duration, new_position):
        self.previous_position = self.position
        self.position = new_position
        posInterval = self.actor.posInterval(duration, self.position, startPos=self.previous_position)
        # posInterval = self.actor.posInterval(duration, self.position, startPos=self.position)
        print("self.position", self.position)
        return posInterval


    def define_new_hpr_interval(self, duration, new_hpr):
        self.previous_hpr = self.hpr
        self.hpr = new_hpr
        hprInterval = self.actor.hprInterval(duration, self.hpr, startHpr=self.previous_hpr)
        # print("self.hpr", self.hpr)
        return hprInterval

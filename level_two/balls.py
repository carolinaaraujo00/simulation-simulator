from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3
from direct.interval.IntervalGlobal import Sequence

from common import *


class Ball:
    def __init__(self, loader, scene, location):
        self.actor = None   
        self.loader = loader
        self.scene = scene

        self.position = location  # This is also the initial position of the actor
        self.previous_position = location  
        self.start_position = location  
        self.previous_hpr = Point3(0, 0, 0)
        self.hpr = Point3(0, 0, 0)
        self.scale = Vec3(0.2, 0.2, 0.2)

        # self.setup_animation()

    def create_flat_ball(self):
        self.actor = self.loader.loadModel(flat_ball_model_path)
        self.setup_ball()

    def create_smooth_ball(self):
        self.actor = self.loader.loadModel(smooth_ball_model_path)
        self.setup_ball()

    def create_moving_flat_ball(self):
        self.actor = self.loader.loadModel(flat_ball_model_path)
        self.setup_ball()
        self.setup_animation()

    # Setup scale, parent and position of ball
    def setup_ball(self):
        self.actor.setScale(self.scale)
        self.actor.reparentTo(self.scene)
        self.actor.setPos(self.position)


    def setup_animation(self):
        intervals = []
        # Ball in works
        intervals.append(self.define_new_interval(0, self.position, Point3(0, 0, 0) ))
        
        # Paper starts Falling

        self.animation_sequence = Sequence(name="animation_ball")
        
        for x in intervals:
            self.animation_sequence.append(x)

        self.animation_sequence.loop()

    def define_new_interval(self, duration, new_position, new_hpr):
        self.previous_position = self.position
        self.position = new_position
        self.previous_hpr = self.hpr
        self.hpr = new_hpr
        # PosHprInterval(nodePath, duration, pos, hpr, startPos, startHpr)
        posInterval = self.actor.PosHprInterval(duration, self.position, self.hpr, startPos=self.previous_position, startPos=self.previous_hpr)
        # posInterval = self.actor.PosHprInterval(self.actor, duration, self.position, startPos=self.previous_position)
        return posInterval

from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3
from direct.interval.IntervalGlobal import Sequence

from common import *
from panda3d.core import Material

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

        # Creates materials for balls
        self.polished_bronze = Material()
        self.red_neon = Material()

        # Polished Bronze material settings
        p_bronze_ambient = (0.25, 0.148, 0.06475, 1)
        p_bronze_diffuse = (0.4, 0.2368, 0.1036, 1)
        p_bronze_specular = (0.774597, 0.458561, 0.200621, 1)
        # p_bronze_shiness = 76.8
        p_bronze_shiness = 128

        self.polished_bronze.setAmbient(p_bronze_ambient)
        self.polished_bronze.setDiffuse(p_bronze_diffuse)
        self.polished_bronze.setShininess(p_bronze_shiness)
        self.polished_bronze.setSpecular(p_bronze_specular)

        # Red Neon ball with emission
        self.red_neon_ambient = (1, 0, 0, 1)
        self.red_neon_diffuse = (1, 0, 0, 1)
        self.red_neon_specular = (1, 1, 1, 1)
        self.red_neon_shiness = 128

        self.red_neon.setAmbient(self.red_neon_ambient)
        self.red_neon.setDiffuse(self.red_neon_diffuse)
        self.red_neon.setEmission(self.red_neon_ambient)
        self.red_neon.setShininess( self.red_neon_shiness)
        self.red_neon.setSpecular(self.red_neon_specular)

    # creates differentes types of balls 

    def create_flat_ball(self):
        self.actor = self.loader.loadModel(flat_ball_model_path)
        self.setup_ball()

    def create_smooth_ball(self):
        self.actor = self.loader.loadModel(smooth_ball_model_path)
        self.setup_ball()

    def create_flat_ball_bronze(self):
        self.actor = self.loader.loadModel(flat_ball_model_path)
        self.setup_ball()
        # Needs to find the original material, even if empty, and replace with new one
        material = self.actor.findMaterial("Material.001")
        self.actor.replaceMaterial(material, self.polished_bronze) # Apply the material to this nodePath

    def create_flat_ball_neon(self):
        self.actor = self.loader.loadModel(flat_ball_model_path)
        self.setup_ball()
        material = self.actor.findMaterial("Material.001")
        self.actor.replaceMaterial(material, self.red_neon)

    def create_smooth_ball_bronze(self):
        self.actor = self.loader.loadModel(smooth_no_mat_ball_model_path)
        self.setup_ball()
        material = self.actor.findMaterial("fallback material")
        self.actor.replaceMaterial(material, self.polished_bronze)

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
        # Ball in works Start Vec3(-4.88, 1.55, 3.55)
        intervals.append(self.define_new_interval(0, Vec3(-4.88, 1.55, 3.55), Point3(0, 0, 0) ))
        intervals.append(self.define_new_interval(2, Vec3(-3.43, 1.55, 3.55), Point3(0, 0, 360) ))
        # Side
        intervals.append(self.define_new_interval(2, Vec3(-3.43, 0, 3.55), Point3(0, 360, 360) ))
        intervals.append(self.define_new_interval(2,  Vec3(-3.43,  1.55, 3.55), Point3(0, 0, 360) ))
        # Return
        # intervals.append(self.define_new_interval(2, Vec3(-3.43,  1.55, 3.55), Point3(0, 0, 0) ))
        intervals.append(self.define_new_interval(2, Vec3(-4.88, 1.55, 3.55), Point3(0, 0, 0) ))

        self.animation_sequence = Sequence(name="animation_ball")
        
        for x in intervals:
            self.animation_sequence.append(x)

        self.animation_sequence.loop()

    def define_new_interval(self, duration, new_position, new_hpr):
        self.previous_position = self.position
        self.position = new_position
        self.previous_hpr = self.hpr
        self.hpr = new_hpr
        posInterval = self.actor.posHprInterval(duration, self.position, self.hpr, startPos=self.previous_position, startHpr=self.previous_hpr)
        return posInterval

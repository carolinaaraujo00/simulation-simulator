from common import *
from light_setup import * 

class Lamp():
    def __init__(self, loader, render, pos):
        self.loader = loader
        self.render = render
        self.pos = pos 

        self.lights = []

        self.load_lamp()
        self.load_spheres()
    

    def load_lamp(self):
        self.lamp = self.loader.loadModel(ceiling_lamp_model_path)
        self.lamp.setPos(self.pos)
        self.lamp.setHpr(140, 0, 0)
        self.lamp.setScale(4)
        self.lamp.reparentTo(self.render)


    def load_spheres(self):
        # first sphere + light
        self.sphere1 = self.loader.loadModel(sphere_model_path)
        self.sphere1.reparentTo(self.lamp)
        self.sphere1.setPos(-0.002, -0.2, 2.475)
        self.sphere1.setScale(0.017)

        light = setup_ceiling_light(self.render, self.sphere1, self.sphere1.getPos(self.render))
        self.lights.append(light)
        

        # second sphere + light

        self.sphere2 = self.loader.loadModel(sphere_model_path)
        self.sphere2.reparentTo(self.lamp)
        self.sphere2.setPos(-0.002, 0.2, 2.475)
        self.sphere2.setScale(0.018)

        light = setup_ceiling_light(self.render, self.sphere2, self.sphere2.getPos(self.render))
        self.lights.append(light)
from common import *
from light_setup import * 

class Lamp():
    def __init__(self, loader, render, pos):
        self.loader = loader
        self.render = render
        self.pos = pos 

        self.spheres = {
            "left" : [],
            "right" : []
        }
        
        self.load_lamp()
        self.load_spheres()
    
    def load_lamp(self):
        self.lamp = self.loader.loadModel(ceiling_lamp_model_path)
        self.lamp.setPos(self.pos)
        self.lamp.setHpr(140, 0, 0)
        self.lamp.setScale(4)
        self.lamp.reparentTo(self.render)

    def load_spheres(self):
        # LEFT SIDE
        self.sphere1 = self.loader.loadModel(sphere_model_path)
        self.sphere1.reparentTo(self.lamp)
        self.sphere1.setPos(0.053, -0.5, 2.475)
        self.sphere1.setScale(0.018)
        self.spheres["left"].append(self.sphere1)
        setup_ceiling_light(self.render, self.sphere1, self.sphere1.getPos(self.render))
        
        self.sphere2 = self.loader.loadModel(sphere_model_path)
        self.sphere2.reparentTo(self.lamp)
        self.sphere2.setPos(0.053, 0, 2.475)
        self.sphere2.setScale(0.018)
        self.spheres["left"].append(self.sphere2)
        setup_ceiling_light(self.render, self.sphere2, self.sphere2.getPos(self.render))

        self.sphere3 = self.loader.loadModel(sphere_model_path)
        self.sphere3.reparentTo(self.lamp)
        self.sphere3.setPos(0.053, 0.5, 2.475)
        self.sphere3.setScale(0.018)
        self.spheres["left"].append(self.sphere3)
        setup_ceiling_light(self.render, self.sphere3, self.sphere3.getPos(self.render))


        # RIGHT SIDE
        self.sphere4 = self.loader.loadModel(sphere_model_path)
        self.sphere4.reparentTo(self.lamp)
        self.sphere4.setPos(-0.052, -0.5, 2.475)
        self.sphere4.setScale(0.018)
        self.spheres["right"].append(self.sphere4)
        setup_ceiling_light(self.render, self.sphere4, self.sphere4.getPos(self.render))
        
        self.sphere5 = self.loader.loadModel(sphere_model_path)
        self.sphere5.reparentTo(self.lamp)
        self.sphere5.setPos(-0.052, 0, 2.475)
        self.sphere5.setScale(0.018)
        self.spheres["right"].append(self.sphere5)
        setup_ceiling_light(self.render, self.sphere5, self.sphere5.getPos(self.render))

        self.sphere6 = self.loader.loadModel(sphere_model_path)
        self.sphere6.reparentTo(self.lamp)
        self.sphere6.setPos(-0.052, 0.5, 2.475)
        self.sphere6.setScale(0.018)
        self.spheres["right"].append(self.sphere6)
        setup_ceiling_light(self.render, self.sphere6, self.sphere6.getPos(self.render))
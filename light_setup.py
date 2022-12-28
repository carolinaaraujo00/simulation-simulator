from panda3d.core import PointLight, AmbientLight, Spotlight
from panda3d.core import PerspectiveLens
from common import * 

###################################################
#                  ANGLER LIGHTS                  #
###################################################

# AMBIENT LIGHTS

def setup_black_ambient_light(render):
    # it needs no position because..... it's ambient
    alight = AmbientLight('alight')
    alight.setColor(angler_ambient)
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)

# POINT LIGHTS

def setup_blue_point_light(render, pos):
    plight = PointLight("plight")
    #plight.setShadowCaster(True, 1280, 1280)
    
    # Color Blue
    plight.setColor((0.1, 0.5, 0.5, 1))
    plnp = render.attachNewNode(plight)
    plnp.setPos(pos[0], pos[1], pos[2])
    #plight.setAttenuation((1.4, 0, 0))
    render.setLight(plnp) 

def setup_black_point_light(render, pos):
    plight = PointLight("plight")
    plight.setColor((0, 0, 0, 1))
    plnp = render.attachNewNode(plight)
    plnp.setPos(pos[0], pos[1], pos[2])
    render.setLight(plnp) 

def setup_point_light(render, pos):
    # Point light
    plight = PointLight("plight")
    #plight.setShadowCaster(True, 1280, 1280)
    
    plight.setColor(angler_p_light)
    plnp = render.attachNewNode(plight)
    plnp.setPos(pos[0], pos[1], pos[2])

    #plight.setAttenuation((1.4, 0, 0))
    render.setLight(plnp) 



###################################################
#                  OFFICE LIGHTS                  #
###################################################

def setup_office_ambient_light(render):
    # it needs no position because..... it's ambient
    alight = AmbientLight('alight')
    alight.setColor(office_ambient_black)
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)


def setup_point_light_in_model(render, model, position):
    plight = PointLight("plight")
    #plight.setShadowCaster(True, 1280, 1280)
    plight.setColor((0.83137, 0.42353, 0.00784, 1))
    plnp = model.attachNewNode(plight)

    plnp.setPos(position)
    plight.setAttenuation((0, 0, 1))
    plight.setMaxDistance(1)

    render.setLight(plnp)

def setup_ceiling_light(render, model, position):
    plight = PointLight("plight")

    plnp = model.attachNewNode(plight)

    plnp.setPos(position)
    plight.setColor((0.6471, 0.3608, 0.6078, 1))
    plight.setAttenuation((0.2, 0.05, 0.05))
    # plight.setAttenuation((0, 0, 1))
    plight.setMaxDistance(1)
    # plight.setShadowCaster(True, 512, 512)
    render.setLight(plnp)


def setup_torch_spotlight(render, model, position):
    # Point light
    plight = PointLight("plight")
    plight.setAttenuation((1, 0, 0)) # constant, linear and quadratic

    lens = PerspectiveLens()
    plight.setLens(lens)

    plight.setColor(torch_yellow)

    plnp = model.attachNewNode(plight)
    plnp.setPos(position[0], position[1], position[2])
    plnp.lookAt(position[0], position[1], 0)

    render.setLight(plnp)



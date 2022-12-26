from panda3d.core import PointLight, AmbientLight, Spotlight
from panda3d.core import PerspectiveLens

def setup_ambient_light(render):
    # it needs no position because..... it's ambient
    alight = AmbientLight('alight')
    alight.setColor((0.08, 0.08, 0.08, 1))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)


def setup_point_light(render, pos):
    # Point light
    plight = PointLight("plight")
    #plight.setShadowCaster(True, 1280, 1280)
    
    plight.setColor((0.1, 0.5, 0.5, 1))
    plnp = render.attachNewNode(plight)
    plnp.setPos(pos[0], pos[1], pos[2])

    #plight.setAttenuation((1.4, 0, 0))
    render.setLight(plnp) 

def setup_red_spotlight(render, model, position):
    # Point light
    plight = PointLight("plight")
    plight.setAttenuation((1, 0, 0)) # constant, linear and quadratic
    # plight.setShadowCaster(True, 1280, 1280)

    lens = PerspectiveLens()
    plight.setLens(lens)

    plight.setColor((0.83137, 0.42353, 0.00784, 1))

    plnp = model.attachNewNode(plight)
    plnp.setPos(position[0], position[1], position[2])
    plnp.lookAt(position[0], position[1], 0)

    render.setLight(plnp)



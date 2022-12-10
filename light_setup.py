from panda3d.core import PointLight, AmbientLight


def setup_point_light(render, pos):
    # Point light
    # plight = PointLight("plight")
    # plight.setColor((1, 1, 1, 1))
    # plnp = render.attachNewNode(plight)
    # plnp.setPos(pos[0], pos[1], pos[2])
    # # plight.setAttenuation((0, 0, 1))
    # render.setLight(plnp)

    # Ambient light
    alight = AmbientLight("alight")
    alight.setColor((0.8, 0.8, 0.8, 1))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)


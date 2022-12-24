from panda3d.core import Vec3

from engine_2d import*
from player_char_2d import*
from entity import Entity
from collider import Collider

if __name__ == "__main__":
    engine = Engine2D(False)

    # Player
    player_char_2d = PlayerChar2D(engine, Vec3(-100, -15, 5), Vec3(-90, 0, 0), Vec3(0.01, 0.01, 0.01), "egg-models/angler_fish/angler_fish.gltf", True)
    col_player = Collider(engine, player_char_2d, "player_char_2d", Vec3(0, 0, -10), Vec3(20, 40, 25))
    engine.player = player_char_2d
    engine.actors.append(player_char_2d)



    posy = -15
    posz = -3

    rot = Vec3(0, -90, -90)
    scale = Vec3(1, 1 ,1)


    # Platforms
    # TODO: Do platforms properly. As of right now, this just serves to exemplify/blockout a possible level progression.
    pier1 = Entity(engine, Vec3(-100, posy, -3), rot, scale, "egg-models/pier/pier.gltf", True)
    col1 = Collider(engine, pier1, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier2 = Entity(engine, Vec3(-90, posy, -5), rot, scale, "egg-models/pier/pier.gltf", True)
    col2 = Collider(engine, pier2, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier3 = Entity(engine, Vec3(-80, posy, -7), rot, scale, "egg-models/pier/pier.gltf", True)
    col3 = Collider(engine, pier3, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier4 = Entity(engine, Vec3(-69, posy, -9), rot, scale, "egg-models/pier/pier.gltf", True)
    col4 = Collider(engine, pier4, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier5 = Entity(engine, Vec3(-58, posy, -11), rot, scale, "egg-models/pier/pier.gltf", True)
    col5 = Collider(engine, pier5, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier6 = Entity(engine, Vec3(-51, posy, -9), rot, scale, "egg-models/pier/pier.gltf", True)
    col6 = Collider(engine, pier6, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier6 = Entity(engine, Vec3(-44, posy, -7), rot, scale, "egg-models/pier/pier.gltf", True)
    col6 = Collider(engine, pier6, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier7 = Entity(engine, Vec3(-37, posy, -5), rot, scale, "egg-models/pier/pier.gltf", True)
    col7 = Collider(engine, pier7, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier8 = Entity(engine, Vec3(-30, posy, -3), rot, scale, "egg-models/pier/pier.gltf", True)
    col8 = Collider(engine, pier8, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier9 = Entity(engine, Vec3(-23, posy, 0), rot, scale, "egg-models/pier/pier.gltf", True)
    col9 = Collider(engine, pier9, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier10 = Entity(engine, Vec3(-14, posy, 2), rot, scale, "egg-models/pier/pier.gltf", True)
    col10 = Collider(engine, pier10, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier11 = Entity(engine, Vec3(-5, posy, 4), rot, scale, "egg-models/pier/pier.gltf", True)
    col11 = Collider(engine, pier11, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier12 = Entity(engine, Vec3(4, posy, 6), rot, scale, "egg-models/pier/pier.gltf", True)
    col12 = Collider(engine, pier12, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier13 = Entity(engine, Vec3(13, posy, 8), rot, scale, "egg-models/pier/pier.gltf", True)
    col13 = Collider(engine, pier13, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier14 = Entity(engine, Vec3(22, posy, 10), rot, scale, "egg-models/pier/pier.gltf", True)
    col14 = Collider(engine, pier14, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier15 = Entity(engine, Vec3(31, posy, 12), rot, scale, "egg-models/pier/pier.gltf", True)
    col15 = Collider(engine, pier15, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier16 = Entity(engine, Vec3(40, posy, 14), rot, scale, "egg-models/pier/pier.gltf", True)
    col16 = Collider(engine, pier16, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    # Background
    fossil = Entity(engine, Vec3(0, 100, 0), Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5), "egg-models/underwater_environment/fossil.gltf", True)
    background_albedo = Entity(engine, Vec3(-90, 350, -30), Vec3(-90, 0, 0), Vec3(2, 2, 2), "egg-models/background_sea.gltf", True)
    background_alpha = Entity(engine, Vec3(0, 200, 50), Vec3(-90, 0, 0), Vec3(1.5, 1.5, 1.5), "egg-models/background_sea_shading.gltf", True)


    # Loading office 
    """     office_model = engine.loader.loadModel("egg-models/office_space/office.gltf")
    office_model.reparentTo(engine.render) """

    engine.run()

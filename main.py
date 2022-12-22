from panda3d.core import Vec3

from engine_2d import*
from fish_player import*
from entity import Entity
from collider import Collider

if __name__ == "__main__":
    engine = Engine2D(False)


    player = FishPlayer(engine)
    engine.actors.append(player)
    engine.player = player
    

    pier1 = Entity(engine, Vec3(0, 0, -9), Vec3(0, -90, -90), Vec3(5, 5, 5), "egg-models/pier/pier.gltf", True)
    col1 = Collider(engine, pier1, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))



    pier2 = Entity(engine, Vec3(42, 0, -9), Vec3(0, -90, -90), Vec3(5, 5, 5), "egg-models/pier/pier.gltf", True)
    col2 = Collider(engine, pier2, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))

    pier3 = Entity(engine, Vec3(-35, 0, -15), Vec3(0, -90, -90), Vec3(5, 5, 5), "egg-models/pier/pier.gltf", True)
    col3 = Collider(engine, pier3, "pier", Vec3(0, -2, 0.5), Vec3(1, 1, 3))




    # Loading office 
    """     office_model = engine.loader.loadModel("egg-models/office_space/office.gltf")
    office_model.reparentTo(engine.render) """

    engine.run()

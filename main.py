from engine_2d import*
from fish_player import*

if __name__ == "__main__":
    engine = Engine2D()

    player = FishActor(engine)
    engine.actors.append(player)
    engine.player = player

    # Loading the floor and the platforms
    floor = engine.loader.loadModel("egg-models/floor")
    floor.reparentTo(engine.render)

    engine.run()

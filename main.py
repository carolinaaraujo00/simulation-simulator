from level_one.engine_2d import *
from level_one.level_underwater import LevelUnderwater
from level_two.office import ociffer 
import sys
from direct.showbase.ShowBase import ShowBase


def run(level : int):
    # Open a window with 3d and 2d graphic elements
    base = ShowBase()


    if level == 1: 

        engine = Engine2D(base, debug = False)

        # Set underwater level
        underwater = LevelUnderwater(engine, Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(1, 1, 1))
        engine.add_level(underwater)

        # Panda 3D doesn't support multiple instances aka bases, so in case level 1 runs first, when transitioning to level 2,
        # we need to kill the first instance, catch the exception, and create level 2 from scratch.
        try:
            engine.run()

        # Illegal Move. No one needs to know O.O
        except SystemExit as e:
            base.destroy()
            base = ShowBase()
            game = ociffer(base, debug = False) 
            game.run()

    elif level == 2:
            # Debug purposes
            game = ociffer(base, debug = True) 
            game.run()

    else:
        sys.exit(0)

if __name__ == "__main__":
    run(level = 1)

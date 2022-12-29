from panda3d.core import Vec3
from level_one.engine_2d import *
from level_one.level_underwater import LevelUnderwater
from level_two.office import ociffer 
import sys
from direct.showbase.ShowBase import ShowBase
def run(level : int):
    base = ShowBase()
    if level == 1: 

        engine = Engine2D(base, False)

        # Set underwater level
        underwater = LevelUnderwater(engine, Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(1, 1, 1))
        engine.add_level(underwater)

        try:
            engine.run()

        except SystemExit as e:
            base.destroy()
            base = ShowBase()
            game = ociffer(base, debug = False) 
            game.run()


    elif level == 2:
            game = ociffer(base, debug = False) 
            game.run()

    else:
        sys.exit(0)

if __name__ == "__main__":
    run(level = 2)


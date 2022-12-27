from panda3d.core import Vec3
from level_one.engine_2d import *
from level_one.level_underwater import LevelUnderwater
from level_two.office import ociffer 

import sys

def run(level : int):
    if level == 1: 
        engine = Engine2D(False)

        # Set underwater level
        first_lvl = LevelUnderwater(engine, Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(1, 1, 1))
        engine.add_level(first_lvl)

        engine.run()

    elif level == 2: 
        game = ociffer() 
        game.run()

    else:
        sys.exit(0)

run(level = 2)



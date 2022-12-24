from panda3d.core import Vec3

from engine_2d import*
from level_underwater import LevelUnderwater


if __name__ == "__main__":
    engine = Engine2D(True)

    # Set underwater level
    first_lvl = LevelUnderwater(engine, Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(1, 1, 1))
    engine.add_level(first_lvl)

    engine.run()

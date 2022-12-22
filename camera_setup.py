from panda3d.core import OrthographicLens

class Camera:
    def __init__(self, engine, camera):
        lens = OrthographicLens()
        multiplier = 2.6
        lens.setFilmSize(24 * multiplier, 36 * multiplier)  # Or whatever is appropriate for your scene
        lens.setFocalLength(50)
        # lens.setFov(90)
        # lens.setFilmSize(16, 9)  # Or whatever is appropriate for your scene
        # lens.setNearFar(-50, 50)    
        lens.setAspectRatio(1920/1080)
        camera.node().setLens(lens)
        # camera.node().getLens()

    # def setup_camera_controls():
        # TODO: make global input manager
        # Keyboard input events
        # engine.accept("arrow_left", update_key_map, ["left", True])
        # self.engine_ref.accept("arrow_left-up", update_key_map, ["left", False])
        # self.engine_ref.accept("arrow_right", update_key_map, ["right", True])
        # self.engine_ref.accept("arrow_right-up", update_key_map, ["right", False])
        # self.engine_ref.accept("arrow_up", self.jump)
from panda3d.core import OrthographicLens
from common import *

class MainCamera:
    def __init__(self, main_camera):
        self.camera = main_camera
        self.original_lens = None
        self.ortho_lens = None
        self.current_fov = None
        self.is_ortho = False

        self.save_perspective()
        self.setup_camera_perspective(self.camera)

        # self.init_movement()


    def save_perspective(self) -> None:
        self.original_lens = self.camera.node().getLens()
        self.current_fov = self.original_lens.getFov()
        print("Fov=", self.current_fov)


        # lens.setFov(51, 30)
        # lens.setFilmSize(16, 9)  # Or whatever is appropriate for your scene
        # lens.setNearFar(-50, 50)    
    def setup_camera_perspective(self, camera):
        lens = OrthographicLens()
        # multiplier = 5
        # multiplier = 2.6
        multiplier = 0.6
        lens.setFilmSize(24 * multiplier, 36 * multiplier)  # Or whatever is appropriate for your scene
        lens.setFocalLength(50)
        lens.setAspectRatio(1920/1080)
        # lens.setAspectRatio(1280/720)
        self.ortho_lens = lens
        camera.node().setLens(lens)

    def change_camera_ortho(self) -> None:
        self.is_ortho = not self.is_ortho
        if self.is_ortho:
            print("Is ortho")
            self.camera.node().setLens(self.ortho_lens)
        else:
            print("Is pers")
            self.camera.node().setLens(self.original_lens)

    def change_camera_to_ortho(self, change_to_ortho : bool) -> None:
        self.is_ortho = change_to_ortho
        if change_to_ortho:
            self.camera.node().setLens(self.ortho_lens)
        else:
            self.camera.node().setLens(self.original_lens)

    def set_camera_fov(self, fov_value : int, focal_length_value : int):
        lens = self.camera.node().getLens()
        lens.setFov(fov_value)
        # lens.setFocalLength(focal_length_value)

    def get_camera_fov(self):
        lens = self.camera.node().getLens()
        return lens.getFov()

    def add_camera_fov(self):
        lens = self.camera.node().getLens()
        self.current_fov = self.current_fov + 3
        lens.setFov(self.current_fov)
        print("FOV = ", self.current_fov)
    
    def subtract_camera_fov(self):
        lens = self.camera.node().getLens()
        self.current_fov = self.current_fov - 3
        lens.setFov(self.current_fov)
        print("FOV = ", self.current_fov)

    def init_movement(self):

        self.accept("KP_Add", updateCameraKeyMap, ["plus_fov", True])
        self.accept("KP_Add-up", updateCameraKeyMap, ["plus_fov", False])

        self.accept("KP_Subtract", updateCameraKeyMap, ["minus_fov", True])
        self.accept("KP_Subtract-up", updateCameraKeyMap, ["minus_fov", False])

    # Called every frame
    # def update(self, task):
    def update(self):
        if camera_input_map["plus_fov"]:
            print("update")
            self.add_camera_fov()
        if camera_input_map["minus_fov"]:
            print("update")
            self.subtract_camera_fov()

        # return task.cont
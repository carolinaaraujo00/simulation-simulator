from panda3d.core import OrthographicLens
from common import *
import threading
import time


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
            self.camera.node().setLens(self.ortho_lens)
        else:
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

    def get_camera_fov(self):
        lens = self.camera.node().getLens()
        return lens.getFov()

    def add_camera_fov(self):
        lens = self.camera.node().getLens()
        self.current_fov = self.current_fov + 0.1
        lens.setFov(self.current_fov)
    
    def subtract_camera_fov(self):
        lens = self.camera.node().getLens()
        self.current_fov = self.current_fov - 0.1
        lens.setFov(self.current_fov)

    def fov_breathing_effect_start(self):
        self.is_breathing = True
        self.fov_breath = threading.Thread(target=self.fov_increase_method, args=())
        self.fov_breath.daemon = True
        self.fov_breath.start()

    def fov_increase_method(self):
        self.breathing_counter = 0
        self.incraesing = True

        while self.is_breathing:
            time.sleep(0.017)
            if not self.is_ortho:
                if self.incraesing:
                    self.add_camera_fov()
                    self.breathing_counter = self.breathing_counter + 1
                    if self.breathing_counter >= 10:
                        self.incraesing = False
                else:
                    self.subtract_camera_fov()
                    self.breathing_counter = self.breathing_counter - 1
                    if self.breathing_counter <= 0:
                        self.incraesing = True
        # TODO: stop thread
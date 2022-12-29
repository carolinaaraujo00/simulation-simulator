from panda3d.core import OrthographicLens
from common import *
import threading
import time
from level_one.sound_player_one import *


class MainCamera:
    def __init__(self, main_camera, sound_player):
        self.camera = main_camera
        self.sound_player = sound_player
        self.original_lens = None
        self.ortho_lens = None
        self.current_fov = None
        self.is_ortho = False

        self.save_perspective()
        self.setup_camera_perspective(self.camera)

        self.is_breathing = False
        self.can_play_glitch = True

    def save_perspective(self) -> None:
        self.original_lens = self.camera.node().getLens()
        self.current_fov = self.original_lens.getFov()

    def setup_camera_perspective(self, camera):
        lens = OrthographicLens()
        multiplier = 0.6
        lens.setFilmSize(24 * multiplier, 36 * multiplier)  # Or whatever is appropriate for your scene
        lens.setFocalLength(50)
        lens.setAspectRatio(1920/1080)
        self.ortho_lens = lens
        camera.node().setLens(lens)

    def change_camera_ortho(self) -> None:
        self.is_ortho = not self.is_ortho
        if self.is_ortho:
            self.can_play_glitch = True
            self.is_breathing = False
            self.camera.node().setLens(self.ortho_lens)
        else:
            self.camera.node().setLens(self.original_lens)

    def change_camera_to_ortho(self, change_to_ortho : bool) -> None:
        self.is_ortho = change_to_ortho
        if change_to_ortho:
            self.can_play_glitch = True
            self.is_breathing = False
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
        self.fov_breath = threading.Thread(target=self.fov_breath_method, args=())
        self.fov_breath.daemon = True
        self.fov_breath.start()

    def camera_glitch_effect_start(self):
        self.is_glitchy = True
        self.camera_glitch = threading.Thread(target=self.camera_glitch_effect, args=())
        self.camera_glitch.daemon = True
        self.camera_glitch.start()

    def camera_glitch_effect(self):
        while self.is_glitchy:
            time.sleep(7)
            if self.can_play_glitch:
                if not self.is_breathing:
                    self.sound_player.glitch()
                    self.change_camera_ortho()
                    time.sleep(0.5)
                    self.change_camera_ortho()


    def fov_breath_method(self):
        if self.is_ortho:
            return

        self.can_play_glitch = False
        self.is_breathing = True
        self.breathing_counter = 0
        self.incraesing = True
        self.zoom_in_out = 0

        while self.zoom_in_out < 1:
            time.sleep(0.017)
            if not self.is_ortho:
                if self.incraesing:
                    self.add_camera_fov()
                    self.breathing_counter = self.breathing_counter + 1
                    if self.breathing_counter >= 20:
                        self.incraesing = False
                else:
                    self.subtract_camera_fov()
                    self.breathing_counter = self.breathing_counter - 1
                    if self.breathing_counter <= -20:
                        self.incraesing = True
                        self.zoom_in_out = self.zoom_in_out + 1
        
        self.can_play_glitch = True
        self.is_breathing = False

    def stop_threads(self):
        self.zoom_in_out = 3
        self.is_breathing = False
        self.is_glitchy = False
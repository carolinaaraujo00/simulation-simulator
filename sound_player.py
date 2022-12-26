from panda3d.core import Vec3

from engine_2d import *
from common import *
from panda3d.core import AudioSound

class SoundPlayer:
    def __init__(self, incoming_engine_ref: Engine2D):
        self.engine_ref = incoming_engine_ref

    def init_level1_sounds(self):
        self.power_up_sound = self.engine_ref.loader.loadSfx(power_up_sound_path)
        self.underwater_music = self.engine_ref.loader.loadSfx(underwater_sound_path)
        self.power_up_sound.setLoop(False)
        self.set_volumes_level1(0.1)
        self.underwater_music.play()

    def set_volumes_level1(self, volume_value):
        self.underwater_music.setVolume(volume_value)
        self.power_up_sound.setVolume(volume_value)

    def level1_power_up(self):
        self.power_up_sound.play()

    def init_level2_sounds(self):
        self.intro_sound = self.engine_ref.loader.loadSfx(intro_level2_sound_path)
        self.intro_music = self.engine_ref.loader.loadSfx(music_level2_sound_path)

        self.intro_sound.setLoop(False)
        self.intro_music.setLoop(True)
        self.set_volumes_level2(0.3)

    def set_volumes_level2(self, volume_value):
        self.intro_sound.setVolume(volume_value)
        self.intro_music.setVolume(volume_value)

    def play_level2_sounds(self):
        self.intro_sound.play()
        self.intro_music.play()
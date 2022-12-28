from level_one.engine_2d import *
from common import *

class SoundPlayerOne:
    def __init__(self, incoming_engine_ref: Engine2D):
        self.engine_ref = incoming_engine_ref

    def init_sounds(self):
        self.power_up_sound = self.engine_ref.base.loader.loadSfx(power_up_sound_path)
        self.underwater_music = self.engine_ref.base.loader.loadSfx(underwater_sound_path)
        self.glitch_sound = self.engine_ref.base.loader.loadSfx(glitch_sound_path)
        elf.death_sound = self.engine_ref.base.loader.loadSfx(death_sound_path)
        self.power_up_sound.setLoop(False)
        self.death_sound.setLoop(False)
        self.underwater_music.setLoop(True)
        self.set_volumes(0.1)
        self.underwater_music.play()

    def set_volumes(self, volume_value):
        self.underwater_music.setVolume(volume_value)
        self.power_up_sound.setVolume(0.3)
        self.death_sound.setVolume(0.7)
        self.glitch_sound.setVolume(0.7)

    def power_up(self):
        self.power_up_sound.play()

    def glitch(self):
        self.glitch_sound.play()

    def death(self):
        self.death_sound.play()

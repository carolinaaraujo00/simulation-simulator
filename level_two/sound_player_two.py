from panda3d.core import Vec3

from common import *
import time
import threading

from level_one.engine_2d import *

class SoundPlayerTwo:
    def __init__(self, incoming_engine_ref: Engine2D):
        self.engine_ref = incoming_engine_ref

    # Loads sounds from level 2
    def init_sounds(self):
        self.intro_music = self.engine_ref.loader.loadSfx(music_level2_sound_path)
        self.intro_sound = self.engine_ref.loader.loadSfx(intro_level2_sound_path)
        self.light_on = self.engine_ref.loader.loadSfx(light_on_level2_sound_path)
        self.light_buzz = self.engine_ref.loader.loadSfx(light_buzz_level2_sound_path)
        self.cockroach = self.engine_ref.loader.loadSfx(cockroach_level2_sound_path)
        self.printer = self.engine_ref.loader.loadSfx(printer_level2_sound_path)
        self.ring = self.engine_ref.loader.loadSfx(phone_ring_sound_path)
        
        # Setups up the sounds on loop and it's volumes
        self.intro_music.setLoop(True)
        self.cockroach.setLoop(True)
        self.light_buzz.setLoop(True)
        self.ring.setLoop(True)

        self.light_on.setLoop(False)
        self.printer.setLoop(False)
        self.intro_sound.setLoop(False)
        self.set_volumes(0.3, 0.1)

    def set_volumes(self, main_volume, background_volume):
        self.intro_sound.setVolume(main_volume)
        self.intro_music.setVolume(main_volume)

        self.cockroach.setVolume(background_volume)
        self.light_buzz.setVolume(background_volume * 3)
        self.light_on.setVolume(background_volume * 3)
        self.printer.setVolume(background_volume)
        self.ring.setVolume(background_volume/3)

    # waits a while to start playing music before the game starts
    def wait_for_load_thread(self):
        time.sleep(4)
        self.intro_sound.play()
        self.intro_music.play()

    # Flickring sound effect with timer
    def play_lights_on_thread(self):
        self.light_on.play()
        time.sleep(self.light_on.getTime())
        self.light_buzz.play()

    # Plays all sounds of the game
    def play_sounds(self):
        x = threading.Thread(target=self.wait_for_load_thread, args=())
        x.daemon = True
        x.start()
        self.cockroach.play()
        self.printer.play()
        self.ring.play()

    def play_lights_on(self):
        x = threading.Thread(target=self.play_lights_on_thread, args=())
        x.daemon = True
        x.start()

    def play_interruptor(self):
        self.light_on.play()


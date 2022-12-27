from enum import Enum

configVars = """
win-size 1280 720
show-frame-rate-meter 1
window-title Simulation Simulator
"""

hand_model_path = "egg-models/hands/fps-hands.gltf"

# office_model_path = "egg-models/office_space/office.gltf"
office_model_path = "egg-models/office_space/office_finish_v3.gltf"

office_room_model_path = "egg-models/office_space/office_room.gltf"

cockroach_model_path = "egg-models/cockroach/cockroach.gltf"

printer_model_path = "egg-models/others/deskjet_printer/printer_anim_v2.gltf"
paper_model_path = "egg-models/others/deskjet_printer/paper_anim_v2.gltf"

lamp_model_path = "egg-models/office_space/lamp.gltf"

# Sounds
underwater_sound_path = "sounds/level1/Underwater.ogg"
power_up_sound_path = "sounds/level1/power_up.wav"

intro_level2_sound_path = "sounds/level2/intro.ogg"
music_level2_sound_path = "sounds/level2/music.ogg"

light_on_level2_sound_path = "sounds/level2/light_on.ogg"
light_buzz_level2_sound_path = "sounds/level2/light_buzz.ogg"
cockroach_level2_sound_path = "sounds/level2/cockroach.wav"
printer_level2_sound_path = "sounds/level2/printer.ogg"


key_map_3d = {
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False,
    "elevate" : False,
    "lower" : False
}

def updateKeyMap(key, state):
    key_map_3d[key] = state
from enum import Enum
from panda3d.core import Vec3

configVars = """
win-size 1280 720
show-frame-rate-meter 1
window-title Simulation Simulator
"""

model_path = "models/"
sound_path = "sounds/"

level_one = "level_one/"
level_two = "level_two/"


##################################################
#                  ANGLER FISH                   #
##################################################
# TEXTURES
blank_texture = level_one + "BlankTextr.png"


# MODEL PATHS
angler_fish_model_path = model_path + level_one + "angler_fish/angler_fish.gltf"

fossil_model_path = model_path + level_one + "underwater_environment/fossil.gltf"

background_sea_model_path = model_path + level_one + "background_sea.gltf"

background_sea_shading_model_path = model_path + level_one + "background_sea_shading.gltf"

pier_model_path = model_path + level_one + "pier2.gltf"

orb_model_path = model_path + level_one + "shading_orb/magic_orb.egg"

orb_anim_model_path = model_path + level_one + "shading_orb/magic_orb-Orb rotation_GLTF_created_0"


# SOUNDS
underwater_sound_path = sound_path + level_one + "Underwater.ogg"

power_up_sound_path = sound_path + level_one + "power_up.wav"


##################################################
#                  OFICE SPACE                   #
##################################################

# MODEL PATHS
hand_model_path = model_path + level_two +"hands/fps-hands.gltf"

office_model_path = model_path + level_two + "office_space/office_final.gltf"

office_room_model_path = model_path + level_two + "office_space/office_room.gltf"

lamp_model_path = model_path + level_two + "office_space/lamp.gltf"

cockroach_model_path = model_path + level_two + "cockroach/cockroach.gltf"

printer_model_path = model_path + level_two + "deskjet_printer/printer.gltf"

paper_model_path = model_path + level_two + "deskjet_printer/paper_anim.gltf"

# SOUNDS
intro_level2_sound_path = sound_path + level_two + "intro.ogg"
music_level2_sound_path = sound_path + level_two + "music.ogg"

light_on_level2_sound_path = sound_path + level_two + "light_on.ogg"
light_buzz_level2_sound_path = sound_path + level_two + "light_buzz.ogg"
cockroach_level2_sound_path = sound_path + level_two + "cockroach.ogg"
printer_level2_sound_path = sound_path + level_two + "printer.ogg"

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
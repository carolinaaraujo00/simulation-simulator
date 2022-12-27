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


angler_ambient = (0.08, 0.08, 0.08, 1)
angler_p_light = (0.1, 0.5, 0.5, 1)


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
#                 OFFICE SPACE                   #
##################################################

torch_yellow = (0.83137, 0.42353, 0.00784, 1)
office_ambient_black = (0.00, 0.03, 0.06, 0.88)
ambient_grey = (0.2, 0.2, 0.2, 1)
white_ambient = (1, 1, 1, 1)


# MODEL PATHS
office_model_path = model_path + level_two + "office_space/office_final.gltf"

office_room_model_path = model_path + level_two + "office_space/office_room.gltf"

lamp_model_path = model_path + level_two + "office_space/lamp.gltf"

cockroach_model_path = model_path + level_two + "cockroach/cockroach.gltf"

printer_model_path = model_path + level_two + "deskjet_printer/printer.gltf"

paper_model_path = model_path + level_two + "deskjet_printer/paper_anim.gltf"

ceiling_lamp_model_path = model_path + level_two + "office_space/ceiling_lamp/scene.gltf"
sphere_model_path = model_path + level_two + "sphere/sphere.gltf"
torch_model_path =  model_path + level_two + "office_space/minecraft_torch/scene.gltf"

hand_model_path =  model_path + level_two + "arm/arm.gltf"
office_model_path =   model_path + level_two + "office_space/office/untitled.gltf"

# orange_map_model_path = model_path + level_two + "orange_fruit/orange.gltf"
orange_map_model_path = model_path + level_two + "orange_fruit/orange.egg"
orange_model_path = model_path + level_two + "orange_fruit/orange.gltf"


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
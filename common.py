from enum import Enum

configVars = """
win-size 1280 720
show-frame-rate-meter 1
window-title Simulation Simulator
"""

# hand_model_path = "egg-models/hands/fps-hands.gltf"
hand_model_path = "egg-models/arm/arm.gltf"

# office_model_path = "egg-models/office_space/office.gltf"
office_model_path = "egg-models/office_space/office/untitled.gltf"

office_room_model_path = "egg-models/office_space/office_room.gltf"

cockroach_model_path = "egg-models/cockroach/cockroach.gltf"

printer_model_path = "egg-models/others/deskjet_printer/printer_v1.gltf"
paper_model_path = "egg-models/others/deskjet_printer/paper_anim_v2.gltf"

ceiling_lamp_model_path = "egg-models/office_space/ceiling_lamp/scene.gltf"
sphere_model_path = "egg-models/others/sphere/sphere.gltf"
torch_model_path = "egg-models/office_space/minecraft_torch/scene.gltf"

angler_ambient = (0.08, 0.08, 0.08, 1)
angler_p_light = (0.1, 0.5, 0.5, 1)
torch_yellow = (0.83137, 0.42353, 0.00784, 1)
office_ambient_black = (0.00, 0.03, 0.06, 0.88)


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
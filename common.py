from enum import Enum

configVars = """
win-size 1280 720
show-frame-rate-meter 1
window-title Simulation Simulator
"""

hand_model_path = "egg-models/hands/fps-hands.gltf"

office_model_path = "egg-models/office_space/office.gltf"

office_room_model_path = "egg-models/office_space/office_room.gltf"

cockroach_model_path = "egg-models/cockroach/cockroach.gltf"

lamp_model_path = "egg-models/office_space/lamp.gltf"

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
from enum import Enum

configVars = """
win-size 1280 720
show-frame-rate-meter 1
window-title Simulation Simulator
"""

hand_model_path = "egg-models/hands/fps-hands.gltf"

office_model_path = "egg-models/office_space/office.gltf"

key_map_3d = {
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False
}

def updateKeyMap(key, state):
    key_map_3d[key] = state
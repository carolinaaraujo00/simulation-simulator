from setuptools import setup

setup(
    name="simulation_simulator",
    version="1.0",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.gltf',
                '**/*.bin',
                '**/*.ogg',
                '**/*.wav',

            ],
            'gui_apps': {
                'simulation_simulator': 'main.py',
            },
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'platforms':['win_amd64']
        }
    }
)
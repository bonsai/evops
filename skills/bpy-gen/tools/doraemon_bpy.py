"""
Blender Python — Doraemon generator.
Usage:
    blender --background --python doraemon_bpy.py -- --output /tmp/doraemon.png
"""
import sys
import math
import argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import utils_bpy as u


def generate(output: str = "/tmp/doraemon.png"):
    u.clear_scene()

    blue = u.make_mat("Blue", (0.12, 0.42, 0.85))
    white = u.make_mat("White", (0.98, 0.98, 0.98))
    red = u.make_mat("Red", (0.95, 0.15, 0.15))
    yellow = u.make_mat("Yellow", (0.98, 0.85, 0.1))
    black = u.make_mat("Black", (0.05, 0.05, 0.05))

    u.add_sphere("Body", (0, 0, 1.1), 0.75, blue, (1.0, 1.0, 0.95))
    u.add_sphere("Belly", (0, 0.35, 1.0), 0.55, white, (1.0, 0.6, 1.0))

    u.add_sphere("Head", (0, 0, 2.15), 0.65, blue)
    u.add_sphere("Face", (0, 0.32, 2.2), 0.50, white, (1.0, 0.65, 1.0))

    u.add_sphere("EyeL", (-0.18, 0.55, 2.55), 0.14, white)
    u.add_sphere("EyeR", ( 0.18, 0.55, 2.55), 0.14, white)
    u.add_sphere("PupilL", (-0.18, 0.62, 2.62), 0.04, black)
    u.add_sphere("PupilR", ( 0.18, 0.62, 2.62), 0.04, black)

    u.add_sphere("Nose", (0, 0.75, 2.45), 0.07, red)
    u.add_cylinder("NoseLine", (0, 0.55, 2.2), 0.015, 0.45, black, (math.radians(90), 0, 0))

    for i, angle in enumerate([-30, 0, 30]):
        rad = math.radians(angle)
        ox = math.sin(rad) * 0.35
        oz = math.cos(rad) * 0.35
        u.add_cylinder(f"WhiskerL{i}", (-0.15 - abs(ox), 0.65, 2.2 + oz),
                       0.008, 0.22, black, (0, math.radians(-10 + angle/3), math.radians(80)))
        u.add_cylinder(f"WhiskerR{i}", (0.15 + abs(ox), 0.65, 2.2 + oz),
                       0.008, 0.22, black, (0, math.radians(10 - angle/3), math.radians(-80)))

    u.add_torus("Mouth", (0, 0.45, 2.05), 0.18, 0.025, red, (math.radians(70), 0, 0))
    u.add_torus("Collar", (0, 0, 2.0), 0.52, 0.04, red, (math.radians(90), 0, 0))
    u.add_sphere("Bell", (0, -0.05, 1.85), 0.10, yellow)
    u.add_cylinder("BellSlot", (0, -0.09, 1.85), 0.09, 0.015, black, (math.radians(90), 0, 0))
    u.add_cylinder("BellHole", (0, -0.13, 1.85), 0.02, 0.01, black, (math.radians(90), 0, 0))

    u.add_cylinder("ArmL", (-0.85, -0.05, 1.35), 0.10, 0.55, blue, (0, 0, math.radians(70)))
    u.add_cylinder("ArmR", ( 0.85, -0.05, 1.35), 0.10, 0.55, blue, (0, 0, math.radians(-70)))
    u.add_sphere("HandL", (-1.05, -0.05, 1.05), 0.13, white)
    u.add_sphere("HandR", ( 1.05, -0.05, 1.05), 0.13, white)

    u.add_sphere("FootL", (-0.30, 0, 0.35), 0.18, white, (0.8, 1.0, 0.5))
    u.add_sphere("FootR", ( 0.30, 0, 0.35), 0.18, white, (0.8, 1.0, 0.5))
    u.add_sphere("Tail", (0, -0.75, 1.1), 0.06, red)

    u.camera_fit(padding=1.6, direction=(1.0, -2.2, 0.6))
    u.setup_light(location=(3, -5, 6), energy=3.0)
    u.setup_ground(name="Ground", size=6, mat_color=(0.9, 0.9, 0.9), roughness=0.9)

    u.render(output)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/doraemon.png")
    args = parser.parse_args(argv)
    generate(args.output)

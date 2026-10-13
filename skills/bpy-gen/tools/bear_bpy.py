"""
Blender Python — low-poly wooden carved bear (木彫りクマ).
"""
import sys
import math
import argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import utils_bpy as u


def generate(output: str = "/tmp/bear.png"):
    u.clear_scene()

    wood = u.make_mat("Wood", (0.50, 0.35, 0.22), roughness=0.75)
    dark = u.make_mat("DarkWood", (0.35, 0.24, 0.15), roughness=0.85)
    black = u.make_mat("Black", (0.06, 0.06, 0.06), roughness=0.4)

    u.add_ico("Body", (0, 0, 0.55), 0.38, wood, subdiv=1, scale=(1.0, 0.85, 1.05))
    u.add_ico("Head", (0, 0.05, 1.05), 0.30, wood, subdiv=1, scale=(1.05, 0.95, 1.0))
    u.add_ico("Snout", (0, 0.28, 0.98), 0.12, dark, subdiv=1, scale=(1.0, 0.8, 0.7))
    u.add_ico("Nose", (0, 0.38, 1.02), 0.04, black, subdiv=1)

    u.add_ico("EyeL", (-0.10, 0.18, 1.10), 0.04, black, subdiv=1)
    u.add_ico("EyeR", ( 0.10, 0.18, 1.10), 0.04, black, subdiv=1)

    u.add_ico("EarL", (-0.22, -0.05, 1.30), 0.10, wood, subdiv=1)
    u.add_ico("EarR", ( 0.22, -0.05, 1.30), 0.10, wood, subdiv=1)
    u.add_ico("EarInnerL", (-0.22, -0.02, 1.30), 0.05, dark, subdiv=1)
    u.add_ico("EarInnerR", ( 0.22, -0.02, 1.30), 0.05, dark, subdiv=1)

    u.add_cylinder("ArmL", (-0.42, 0.05, 0.60), 0.09, 0.45, wood, (0, 0, math.radians(65)))
    u.add_cylinder("ArmR", ( 0.42, 0.05, 0.60), 0.09, 0.45, wood, (0, 0, math.radians(-65)))

    u.add_cylinder("LegL", (-0.20, 0, 0.18), 0.10, 0.35, wood)
    u.add_cylinder("LegR", ( 0.20, 0, 0.18), 0.10, 0.35, wood)

    u.add_ico("PawL", (-0.20, 0.08, 0.05), 0.10, dark, subdiv=1, scale=(1.0, 1.2, 0.6))
    u.add_ico("PawR", ( 0.20, 0.08, 0.05), 0.10, dark, subdiv=1, scale=(1.0, 1.2, 0.6))
    u.add_ico("Tail", (0, -0.35, 0.55), 0.08, wood, subdiv=1)

    gmat = u.make_mat("Ground", (0.85, 0.83, 0.80), roughness=0.95)
    u.add_plane("Ground", (0, 0, 0), 4, gmat)

    u.camera_fit(padding=1.4, direction=(1.2, -1.6, 0.7))
    u.setup_light(location=(3, -5, 5), energy=3.0)

    u.render(output)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/bear.png")
    args = parser.parse_args(argv)
    generate(args.output)

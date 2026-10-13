"""
Blender Python — bear catching a salmon (鮭をとる熊).
"""
import sys
import math
import argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import utils_bpy as u


def generate(output: str = "/tmp/salmon_bear.png"):
    u.clear_scene()

    bear_fur = u.make_mat("BearFur", (0.45, 0.30, 0.18), roughness=0.75)
    bear_dark = u.make_mat("BearDark", (0.30, 0.20, 0.12), roughness=0.85)
    bear_black = u.make_mat("BearBlack", (0.05, 0.05, 0.05), roughness=0.4)
    salmon_body = u.make_mat("Salmon", (0.82, 0.45, 0.30), roughness=0.35)
    salmon_belly = u.make_mat("SalmonBelly", (0.95, 0.75, 0.60), roughness=0.3)
    water = u.make_mat("Water", (0.25, 0.45, 0.65), roughness=0.15)
    foam = u.make_mat("Foam", (0.92, 0.95, 0.97), roughness=0.5)
    stone = u.make_mat("Stone", (0.50, 0.48, 0.45), roughness=0.9)

    # Bear body (angling forward)
    body = u.add_ico("Body", (0, 0, 1.0), 0.42, bear_fur, subdiv=1, scale=(1.0, 0.85, 1.1))
    body.rotation_euler = (math.radians(25), 0, 0)

    head = u.add_ico("Head", (0, 0.05, 1.55), 0.28, bear_fur, subdiv=1, scale=(1.05, 0.95, 1.0))
    head.rotation_euler = (math.radians(35), 0, 0)

    u.add_ico("Snout", (0, 0.42, 1.48), 0.10, bear_dark, subdiv=1, scale=(1.0, 0.8, 0.7))
    u.add_ico("Nose", (0, 0.50, 1.50), 0.035, bear_black, subdiv=1)
    u.add_ico("EyeL", (-0.09, 0.18, 1.60), 0.035, bear_black, subdiv=1)
    u.add_ico("EyeR", ( 0.09, 0.18, 1.60), 0.035, bear_black, subdiv=1)

    u.add_ico("EarL", (-0.20, -0.08, 1.78), 0.09, bear_fur, subdiv=1)
    u.add_ico("EarR", ( 0.20, -0.08, 1.78), 0.09, bear_fur, subdiv=1)

    # Left arm (balance)
    u.add_cylinder("ArmL", (-0.42, -0.20, 0.85), 0.08, 0.60, bear_fur, (math.radians(30), 0, math.radians(50)))
    # Right arm reaching down
    u.add_cylinder("ArmR_Upper", (0.38, 0.15, 0.95), 0.09, 0.40, bear_fur, (math.radians(55), 0, math.radians(-25)))
    u.add_cylinder("ArmR_Lower", (0.52, 0.30, 0.55), 0.08, 0.35, bear_fur, (math.radians(70), 0, math.radians(-15)))
    u.add_ico("PawR", (0.58, 0.38, 0.35), 0.10, bear_dark, subdiv=1, scale=(1.1, 1.2, 0.7))

    # Legs
    u.add_cylinder("LegL", (-0.22, -0.10, 0.35), 0.11, 0.70, bear_fur)
    u.add_cylinder("LegR", ( 0.22, -0.10, 0.35), 0.11, 0.70, bear_fur)
    u.add_ico("FootL", (-0.22, -0.10, 0.02), 0.12, bear_dark, subdiv=1, scale=(1.1, 1.3, 0.5))
    u.add_ico("FootR", ( 0.22, -0.10, 0.02), 0.12, bear_dark, subdiv=1, scale=(1.1, 1.3, 0.5))

    u.add_ico("Tail", (0, -0.38, 0.90), 0.08, bear_fur, subdiv=1)

    # Salmon leaping
    salmon = u.add_ico("SalmonBody", (0.55, 0.45, 0.42), 0.14, salmon_body, subdiv=1, scale=(2.2, 0.7, 0.6))
    salmon.rotation_euler = (math.radians(20), math.radians(15), math.radians(-40))
    belly = u.add_ico("SalmonBelly", (0.55, 0.43, 0.40), 0.11, salmon_belly, subdiv=1, scale=(2.0, 0.5, 0.4))
    belly.rotation_euler = (math.radians(20), math.radians(15), math.radians(-40))
    u.add_cone("SalmonTail", (0.82, 0.58, 0.50), 0.08, 0.0, 0.12, salmon_body, (0, math.radians(45), math.radians(-30)))
    u.add_cone("SalmonDorsal", (0.48, 0.42, 0.52), 0.04, 0.0, 0.08, salmon_body, (math.radians(-80), 0, math.radians(-40)))

    # Splash particles
    for i in range(6):
        x = 0.45 + (i % 3) * 0.12
        yy = 0.30 + (i // 3) * 0.12
        z = 0.28 + (i % 2) * 0.08
        u.add_ico(f"Splash_{i}", (x, yy, z), 0.04 + (i % 3) * 0.02, foam, subdiv=1)

    # Water surface
    water_plane = u.add_plane("WaterSurface", (0, 0, 0.15), 4, water)

    # Ripples
    for i, (wx, wy) in enumerate([(0.55, 0.38), (0.35, 0.25), (0.65, 0.45)]):
        u.add_cylinder(f"Ripple_{i}", (wx, wy, 0.18), 0.15 + i * 0.08, 0.01, foam)

    # Ground / rocks
    gmat = u.make_mat("Ground", (0.55, 0.50, 0.42), roughness=0.95)
    u.add_plane("Ground", (0, 0, -0.05), 8, gmat)
    u.add_ico("Rock1", (-0.6, 0.3, 0.08), 0.12, stone, subdiv=1, scale=(1.3, 1.0, 0.8))
    u.add_ico("Rock2", (0.8, -0.2, 0.06), 0.10, stone, subdiv=1, scale=(1.0, 1.2, 0.6))
    u.add_ico("Rock3", (-0.3, -0.5, 0.05), 0.08, stone, subdiv=1, scale=(0.9, 1.1, 0.5))

    u.camera_fit(padding=1.35, direction=(1.5, -2.2, 0.9))
    u.setup_light(location=(3, -5, 6), energy=4.0)
    u.setup_light("AREA", (-2, 2, 3), energy=2.0, color=(0.9, 0.95, 1.0))

    u.render(output)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/salmon_bear.png")
    args = parser.parse_args(argv)
    generate(args.output)

"""
Blender Python — procedural five-story pagoda (五重塔).
"""
import sys
import argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import utils_bpy as u


def generate(output: str = "/tmp/pagoda.png"):
    u.clear_scene()

    stone = u.make_mat("Stone", (0.55, 0.52, 0.48), roughness=0.85)
    wood = u.make_mat("Wood", (0.42, 0.18, 0.14), roughness=0.5)
    roof_mat = u.make_mat("Roof", (0.15, 0.18, 0.25), roughness=0.45)
    gold = u.make_mat("Gold", (0.85, 0.7, 0.2), roughness=0.25)

    # Stone base
    u.add_cube("Base1", (0, 0, 0.15), 1.0, stone, (2.0, 2.0, 0.3))
    u.add_cube("Base2", (0, 0, 0.38), 1.0, stone, (1.7, 1.7, 0.16))

    current_y = 0.46
    pillar_h = 0.55
    tier_widths = [1.5, 1.35, 1.2, 1.05, 0.9]
    tier_depths = [0.45, 0.42, 0.38, 0.34, 0.30]

    for i in range(5):
        w = tier_widths[i]
        h = tier_depths[i]
        floor_z = current_y
        off = w * 0.38

        u.add_cylinder(f"Pillar_{i}_FL", (-off, -off, floor_z + h/2), 0.04, h, wood)
        u.add_cylinder(f"Pillar_{i}_FR", ( off, -off, floor_z + h/2), 0.04, h, wood)
        u.add_cylinder(f"Pillar_{i}_BL", (-off,  off, floor_z + h/2), 0.04, h, wood)
        u.add_cylinder(f"Pillar_{i}_BR", ( off,  off, floor_z + h/2), 0.04, h, wood)

        u.add_cube(f"Wall_{i}_F", (0, -off, floor_z + h/2), 1.0, wood, (w*0.8, 0.04, h*0.9))
        u.add_cube(f"Wall_{i}_B", (0,  off, floor_z + h/2), 1.0, wood, (w*0.8, 0.04, h*0.9))
        u.add_cube(f"Wall_{i}_L", (-off, 0, floor_z + h/2), 1.0, wood, (0.04, w*0.8, h*0.9))
        u.add_cube(f"Wall_{i}_R", ( off, 0, floor_z + h/2), 1.0, wood, (0.04, w*0.8, h*0.9))

        u.add_cube(f"Floor_{i}", (0, 0, floor_z), 1.0, wood, (w*0.85, w*0.85, 0.04))

        roof_z = floor_z + h + 0.02
        roof_radius = w * 0.62
        u.add_cone(f"RoofCone_{i}", (0, 0, roof_z + 0.18), roof_radius, roof_radius*0.15, 0.35, roof_mat)
        u.add_torus(f"RoofEave_{i}", (0, 0, roof_z + 0.06), roof_radius*0.85, 0.025, roof_mat)

        current_y = roof_z + 0.20

    # Spire (sorin)
    spire_z = current_y
    u.add_cylinder("SorinPole", (0, 0, spire_z + 0.35), 0.04, 0.7, gold)
    for j in range(5):
        u.add_torus(f"SorinRing_{j}", (0, 0, spire_z + 0.1 + j*0.12), 0.12 - j*0.015, 0.018, gold)
    u.add_cone("SorinTip", (0, 0, spire_z + 0.75), 0.04, 0.0, 0.15, gold)

    # Ground
    gmat = u.make_mat("Ground", (0.88, 0.88, 0.85), roughness=0.95)
    u.add_plane("Ground", (0, 0, 0), 8, gmat)

    u.camera_fit(padding=1.4, direction=(1.2, -1.8, 0.9))
    u.setup_light(location=(4, -6, 8), energy=3.5)

    u.render(output)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/pagoda.png")
    args = parser.parse_args(argv)
    generate(args.output)

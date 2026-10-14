"""
Blender Python — Donpen-chan (ドン・キホーテ どんぺん) generator.
Usage:
    blender --background --python donpen_bpy.py -- --output /tmp/donpen.png
"""
import sys
import math
import argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import utils_bpy as u


def generate(output: str = "/tmp/donpen.png"):
    u.clear_scene()

    # ── Colors ──
    white    = u.make_mat("White",    (0.98, 0.98, 0.98), roughness=0.3)
    black    = u.make_mat("Black",    (0.08, 0.08, 0.12), roughness=0.4)
    yellow   = u.make_mat("Yellow",   (1.0,  0.85, 0.15), roughness=0.3)
    orange   = u.make_mat("Orange",   (1.0,  0.55, 0.10), roughness=0.35)
    pink     = u.make_mat("Pink",     (0.95, 0.30, 0.55), roughness=0.4)
    darkpink = u.make_mat("DarkPink", (0.75, 0.15, 0.35), roughness=0.5)
    red      = u.make_mat("Red",      (0.90, 0.15, 0.20), roughness=0.35)
    gold     = u.make_mat("Gold",     (1.0,  0.78, 0.25), roughness=0.25, metallic=0.9)
    sky      = u.make_mat("Sky",      (0.55, 0.80, 0.95), roughness=0.3)

    # ── Body (chubby penguin: white belly, black back) ──
    u.add_sphere("Belly",  (0,  0.18, 0.95), 0.52, white, (0.88, 0.72, 0.95))
    u.add_sphere("Back",   (0, -0.12, 1.05), 0.54, black, (0.92, 0.78, 0.98))

    # ── Head ──
    u.add_sphere("Head",   (0,  0.05, 1.72), 0.48, white, (0.90, 0.82, 0.95))
    u.add_sphere("HeadBack", (0, -0.10, 1.74), 0.46, black, (0.92, 0.80, 1.0))

    # ── Eyes (big & cute) ──
    u.add_sphere("EyeWhiteL", (-0.14, 0.28, 1.88), 0.13, white)
    u.add_sphere("EyeWhiteR", ( 0.14, 0.28, 1.88), 0.13, white)
    u.add_sphere("EyePupilL", (-0.14, 0.30, 1.95), 0.065, black)
    u.add_sphere("EyePupilR", ( 0.14, 0.30, 1.95), 0.065, black)
    # Catch-light
    u.add_sphere("EyeSparkL", (-0.12, 0.32, 1.99), 0.018, white)
    u.add_sphere("EyeSparkR", ( 0.16, 0.32, 1.99), 0.018, white)

    # ── Beak (yellow, small triangle-ish) ──
    u.add_cone("BeakTop",    (0, 0.40, 1.85), 0.06, 0.0, 0.08, yellow,  (math.radians(-80), 0, 0))
    u.add_cone("BeakBottom", (0, 0.38, 1.82), 0.05, 0.0, 0.06, orange, (math.radians(-75), 0, 0))

    # ── Cheeks (blush pink dots) ──
    u.add_sphere("CheekL", (-0.22, 0.22, 1.75), 0.04, pink)
    u.add_sphere("CheekR", ( 0.22, 0.22, 1.75), 0.04, pink)

    # ── Don Quijote Cap (pink cone + dark pink brim + star) ──
    # Main cone
    u.add_cone("CapTop",     (0, -0.05, 2.22), 0.28, 0.12, 0.35, pink, (math.radians(-12), 0, 0))
    # Brim
    u.add_torus("CapBrim",   (0,  0.05, 2.08), 0.32, 0.04, darkpink, (0, 0, 0))
    # Bell / pom-pom on top
    u.add_sphere("CapPom",   (0, -0.12, 2.48), 0.06, gold)
    # Star on front
    u.add_sphere("StarCenter", (0, 0.26, 2.12), 0.05, gold)
    u.add_cylinder("StarV",  (0, 0.30, 2.12), 0.012, 0.08, gold, (math.radians(90), 0, 0))
    u.add_cylinder("StarH",  (0, 0.30, 2.12), 0.012, 0.08, gold, (math.radians(90), 0, math.radians(90)))

    # ── Wings (short stubby) ──
    u.add_cylinder("WingL", (-0.52, 0.0, 1.05), 0.08, 0.35, black, (0, 0, math.radians(50)))
    u.add_cylinder("WingR", ( 0.52, 0.0, 1.05), 0.08, 0.35, black, (0, 0, math.radians(-50)))

    # ── Feet (yellow flippers) ──
    u.add_sphere("FootL", (-0.18, 0.0, 0.22), 0.10, yellow, (1.2, 0.6, 0.5))
    u.add_sphere("FootR", ( 0.18, 0.0, 0.22), 0.10, yellow, (1.2, 0.6, 0.5))

    # ── Scene ──
    u.camera_fit(padding=1.4, direction=(1.0, -2.3, 0.6))
    u.setup_light(type_="SUN", location=(3, -5, 6), energy=3.0)
    u.setup_light(type_="AREA", location=(-2, -2, 4), energy=1.2)
    u.setup_ground(name="Ground", size=5, mat_color=(0.90, 0.90, 0.92), roughness=0.9)

    u.render(output)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/donpen.png")
    args = parser.parse_args(argv)
    generate(args.output)

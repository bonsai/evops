"""
Blender Python — Don Quixote generator.
Usage:
    blender --background --python don_quixote_bpy.py -- --output /tmp/don_quixote.png
"""
import sys
import math
import argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import utils_bpy as u


def generate(output: str = "/tmp/don_quixote.png",
             thin_body=False,
             long_lance=False,
             tilted_helmet=False):
    u.clear_scene()

    skin = u.make_mat("Skin", (0.92, 0.82, 0.72), roughness=0.5)
    hair = u.make_mat("Hair", (0.7, 0.6, 0.5), roughness=0.7)
    beard = u.make_mat("Beard", (0.65, 0.55, 0.42), roughness=0.8)
    rust_armor = u.make_mat("RustArmor", (0.55, 0.40, 0.30), roughness=0.8, metallic=0.3)
    tin_helmet = u.make_mat("TinHelmet", (0.75, 0.78, 0.80), roughness=0.3, metallic=0.6)
    wood_lance = u.make_mat("WoodLance", (0.45, 0.32, 0.22), roughness=0.7)
    metal_shield = u.make_mat("MetalShield", (0.50, 0.45, 0.38), roughness=0.6, metallic=0.4)
    dark_cloth = u.make_mat("DarkCloth", (0.25, 0.22, 0.18), roughness=0.9)
    horse_body = u.make_mat("Horse", (0.45, 0.40, 0.35), roughness=0.6)

    body_radius = 0.18 if thin_body else 0.25
    u.add_cylinder("Body", (0, 0, 0.9), body_radius, 1.8, dark_cloth)
    u.add_sphere("Head", (0, 0, 2.0), 0.24, skin)

    # Beard
    u.add_cylinder("Beard", (0, -0.08, 1.82), 0.12, 0.18, beard,
                   (math.radians(20), 0, 0))
    u.add_cylinder("BeardLine", (0, -0.15, 1.78), 0.02, 0.15, beard,
                   (math.radians(70), 0, 0))

    # Helmet
    helmet_rot = (math.radians(15), 0, 0) if tilted_helmet else (0, 0, 0)
    u.add_cone("HelmetTop", (0, 0, 2.35), 0.22, 0.08, 0.20, tin_helmet, helmet_rot)
    u.add_torus("HelmetRim", (0, 0, 2.32), 0.18, 0.025, tin_helmet, helmet_rot)
    u.add_cylinder("HelmetVisor", (0, 0.12, 2.15), 0.08, 0.08,
                   u.make_mat("Visor", (0.3, 0.3, 0.3), roughness=0.4, metallic=0.7),
                   helmet_rot)

    # Armor
    u.add_cube("ChestPlate", (0, 0.08, 1.35), 0.45, rust_armor, (0.9, 0.5, 0.9))
    u.add_torus("ArmorRim", (0, 0.08, 1.15), 0.30, 0.02, rust_armor,
                (math.radians(90), 0, 0))

    # Lance
    lance_len = 4.0 if long_lance else 3.5
    u.add_cylinder("Lance", (0.55, 0, 1.5), 0.025, lance_len, wood_lance,
                   (0, 0, math.radians(5)))
    u.add_cone("LanceTip", (0.70, 0, 3.35), 0.04, 0.0, 0.15,
               u.make_mat("SteelTip", (0.6, 0.65, 0.7), roughness=0.2, metallic=0.8),
               (0, 0, math.radians(5)))

    # Shield
    u.add_cylinder("Shield", (-0.35, 0.30, 1.2), 0.35, 0.05, metal_shield,
                   (math.radians(90), 0, 0))
    u.add_torus("ShieldRim", (-0.35, 0.32, 1.2), 0.35, 0.015,
                u.make_mat("Rim", (0.4, 0.35, 0.3), roughness=0.5, metallic=0.5),
                (math.radians(90), 0, 0))

    # Arms
    u.add_cylinder("ArmL", (-0.45, -0.05, 1.4), 0.06, 0.7, dark_cloth,
                   (0, 0, math.radians(60)))
    u.add_cylinder("ArmR", (0.50, -0.05, 1.4), 0.06, 0.7, dark_cloth,
                   (0, 0, math.radians(-60)))
    u.add_sphere("HandL", (-0.72, -0.05, 1.05), 0.06, skin)
    u.add_sphere("HandR", (0.78, -0.05, 1.05), 0.06, skin)

    # Legs
    u.add_cylinder("LegL", (-0.12, 0, 0.4), 0.07, 0.8, dark_cloth)
    u.add_cylinder("LegR", (0.12, 0, 0.4), 0.07, 0.8, dark_cloth)
    u.add_sphere("BootL", (-0.12, 0, 0.08), 0.08, u.make_mat("Boot", (0.2, 0.15, 0.1), roughness=0.8))
    u.add_sphere("BootR", (0.12, 0, 0.08), 0.08, u.make_mat("Boot2", (0.2, 0.15, 0.1), roughness=0.8))

    # Horse (Rocinante)
    u.add_sphere("HorseBody", (0, 1.2, 0.6), 0.35, horse_body, (1.4, 0.6, 0.8))
    u.add_cylinder("HorseNeck", (0.15, 1.5, 1.0), 0.10, 0.5, horse_body,
                   (math.radians(-30), 0, 0))
    u.add_sphere("HorseHead", (0.25, 1.65, 1.35), 0.14, horse_body)
    u.add_cylinder("HorseLegFL", (0.15, 1.0, 0.3), 0.04, 0.6, horse_body)
    u.add_cylinder("HorseLegFR", (0.15, 1.4, 0.3), 0.04, 0.6, horse_body)
    u.add_cylinder("HorseLegBL", (-0.15, 1.0, 0.3), 0.04, 0.6, horse_body)
    u.add_cylinder("HorseLegBR", (-0.15, 1.4, 0.3), 0.04, 0.6, horse_body)
    u.add_cylinder("HorseTail", (-0.25, 1.0, 0.8), 0.02, 0.4, hair,
                   (math.radians(30), 0, 0))

    # Scene setup
    u.camera_fit(padding=1.6, direction=(1.2, -2.5, 0.5))
    u.setup_light(type_="SUN", location=(4, -6, 8), energy=3.0)
    u.setup_light(type_="AREA", location=(-3, -3, 5), energy=1.5)
    u.setup_ground(name="Ground", size=10, mat_color=(0.85, 0.80, 0.72), roughness=0.95)

    u.render(output)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/don_quixote.png")
    parser.add_argument("--thin-body", action="store_true")
    parser.add_argument("--long-lance", action="store_true")
    parser.add_argument("--tilted-helmet", action="store_true")
    args = parser.parse_args(argv)
    generate(
        args.output,
        thin_body=args.thin_body,
        long_lance=args.long_lance,
        tilted_helmet=args.tilted_helmet,
    )

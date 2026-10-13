"""Animate a light orbiting around a procedural egg.

The key light circles the egg, so the soft shadow sweeps around the floor.

Usage:
    blender --background --python egg_light_orbit.py

Outputs (next to this script):
    frames/frame_0001.png ...   rendered frames
    egg_light_orbit.mp4         H.264 loop
    egg_light_orbit_manifest.json  machine-readable scene/asset manifest
"""

import json
import math
import os

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(HERE, "frames")
MP4 = os.path.join(HERE, "egg_light_orbit.mp4")
MANIFEST = os.path.join(HERE, "egg_light_orbit_manifest.json")

FPS = 24
FRAME_START = 1
FRAME_END = 120
RES_X = 720
RES_Y = 540
LIGHT_RADIUS = 3.6
LIGHT_HEIGHT = 3.0
LIGHT_BOB = 0.8
EGG_HEIGHT = 2.0


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def _material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    base = mat.node_tree.nodes.get("Principled BSDF")
    if base:
        base.inputs["Base Color"].default_value = (*color, 1.0)
        base.inputs["Roughness"].default_value = roughness
    return mat


def create_egg():
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, ring_count=32, location=(0, 0, EGG_HEIGHT / 2)
    )
    egg = bpy.context.object
    egg.name = "Egg"
    egg.scale = (0.72, 0.72, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    egg.data.materials.append(_material("EggMat", (0.95, 0.92, 0.82), 0.45))
    return egg


def create_floor():
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"
    floor.data.materials.append(_material("FloorMat", (0.55, 0.56, 0.6), 0.85))
    return floor


def create_key_light():
    bpy.ops.object.light_add(type="AREA", location=(LIGHT_RADIUS, 0, LIGHT_HEIGHT))
    light = bpy.context.object
    light.name = "KeyLight"
    light.data.energy = 1200
    light.data.shape = "DISK"
    light.data.size = 1.6
    return light


def create_rim_light():
    bpy.ops.object.light_add(type="AREA", location=(-4.0, 4.5, 3.0))
    light = bpy.context.object
    light.name = "RimLight"
    light.data.energy = 220
    light.data.size = 4.0
    light.data.color = (0.6, 0.7, 1.0)
    return light


def create_camera():
    bpy.ops.object.camera_add(location=(4.6, -6.2, 3.1))
    camera = bpy.context.object
    camera.name = "Camera"
    target = Vector((0, 0, EGG_HEIGHT / 2))
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 50
    bpy.context.scene.camera = camera
    return camera


def animate_key_light(light):
    span = FRAME_END - FRAME_START
    try:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    except Exception:
        pass
    for frame in range(FRAME_START, FRAME_END + 1):
        t = (frame - FRAME_START) / span
        angle = 2.0 * math.pi * t
        light.location = (
            LIGHT_RADIUS * math.cos(angle),
            LIGHT_RADIUS * math.sin(angle),
            LIGHT_HEIGHT + LIGHT_BOB * math.sin(2.0 * angle),
        )
        light.rotation_euler = (
            Vector((0, 0, EGG_HEIGHT / 2)) - light.location
        ).to_track_quat("-Z", "Y").to_euler()
        light.keyframe_insert("location", frame=frame)
        light.keyframe_insert("rotation_euler", frame=frame)


def setup_scene():
    clear_scene()
    create_egg()
    create_floor()
    key = create_key_light()
    create_rim_light()
    create_camera()
    animate_key_light(key)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.fps = FPS
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.render.resolution_x = RES_X
    scene.render.resolution_y = RES_Y
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = os.path.join(FRAMES_DIR, "frame_")
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    scene.world.color = (0.03, 0.03, 0.05)
    return scene


def write_manifest():
    manifest = {
        "subject": "egg",
        "fps": FPS,
        "duration_seconds": (FRAME_END - FRAME_START + 1) / FPS,
        "frame_start": FRAME_START,
        "frame_end": FRAME_END,
        "resolution": [RES_X, RES_Y],
        "scene": {"egg": {"height": EGG_HEIGHT}, "floor": {"size": 12}},
        "assets": [
            {"id": "procedural:egg", "source": "blender", "type": "mesh"},
            {"id": "procedural:floor", "source": "blender", "type": "mesh"},
        ],
        "lighting": {
            "key": {
                "type": "area",
                "motion": "orbit",
                "radius": LIGHT_RADIUS,
                "height": LIGHT_HEIGHT,
                "bob": LIGHT_BOB,
                "revolutions": 1,
            },
            "rim": {"type": "area", "energy": 220},
        },
        "camera": {"location": [4.6, -6.2, 3.1], "lens": 50},
        "motion": [{"target": "KeyLight", "action": "orbit_around_subject", "frames": [FRAME_START, FRAME_END]}],
        "render": {"engine": "BLENDER_EEVEE", "output": "frames/frame_%04d.png"},
    }
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    os.makedirs(FRAMES_DIR, exist_ok=True)
    setup_scene()
    write_manifest()
    bpy.ops.render.render(animation=True)
    print("FRAMES:", FRAMES_DIR)
    print("MANIFEST:", MANIFEST)

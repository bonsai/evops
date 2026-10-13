"""Render a psychedelic rotating rainbow torus with bloom.

A trippy, colorful spiral sphere rendered in Blender EEVEE with glow/bloom.

Usage:
    blender --background --python psychedelic.py

Outputs (next to this script):
    frames/frame_0001.png ...   rendered frames
    psychedelic.mp4             H.264 loop
    psychedelic_manifest.json   machine-readable manifest
"""

import json
import math
import os

import numpy as np

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(HERE, "frames")
MP4 = os.path.join(HERE, "psychedelic.mp4")
MANIFEST = os.path.join(HERE, "psychedelic_manifest.json")

FPS = 24
FRAME_START = 1
FRAME_END = 96
RES_X = 720
RES_Y = 540


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def _rgb(r, g, b):
    return (r / 255.0, g / 255.0, b / 255.0, 1.0)


def _color_ramp():
    """Rainbow color ramp (red -> yellow -> green -> cyan -> blue -> magenta -> red)."""
    stops = [
        (0.00, _rgb(255, 0, 0)),
        (0.17, _rgb(255, 255, 0)),
        (0.33, _rgb(0, 255, 0)),
        (0.50, _rgb(0, 255, 255)),
        (0.67, _rgb(0, 0, 255)),
        (0.83, _rgb(255, 0, 255)),
        (1.00, _rgb(255, 0, 0)),
    ]
    return stops


def _material(name):
    mat = bpy.data.materials.new(name)
    tree = mat.node_tree
    tree.nodes.clear()
    out = tree.nodes.new("ShaderNodeOutputMaterial")
    out.location = (1000, 0)

    tex_coord = tree.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-700, 0)

    mapping = tree.nodes.new("ShaderNodeMapping")
    mapping.location = (-400, 0)
    mapping.inputs["Scale"].default_value = (6.0, 6.0, 6.0)

    noise = tree.nodes.new("ShaderNodeTexNoise")
    noise.location = (-120, 0)
    noise.inputs["Scale"].default_value = 4.0
    noise.inputs["Detail"].default_value = 2.0

    ramp = tree.nodes.new("ShaderNodeValToRGB")
    ramp.location = (160, 0)
    ramp.color_ramp.interpolation = "EASE"
    for pos, col in _color_ramp():
        elem = ramp.color_ramp.elements.new(pos)
        elem.color = col

    # Emission for glowing psychedelic feel
    emission = tree.nodes.new("ShaderNodeEmission")
    emission.location = (480, 140)
    emission.inputs["Strength"].default_value = 0.6
    emission.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)

    mix = tree.nodes.new("ShaderNodeMixShader")
    mix.location = (760, 0)
    mix.inputs["Fac"].default_value = 0.7

    base = tree.nodes.new("ShaderNodeBsdfPrincipled")
    base.location = (480, -140)
    base.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
    base.inputs["Metallic"].default_value = 0.0
    base.inputs["Roughness"].default_value = 0.3

    tree.links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
    tree.links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    tree.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    tree.links.new(ramp.outputs["Color"], base.inputs["Base Color"])
    tree.links.new(ramp.outputs["Color"], emission.inputs["Color"])
    tree.links.new(base.outputs["BSDF"], mix.inputs[1])
    tree.links.new(emission.outputs["Emission"], mix.inputs[2])
    tree.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    mat.use_nodes = True
    return mat


def create_psychedelic():
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.4, minor_radius=0.5, major_segments=64, minor_segments=64
    )
    torus = bpy.context.object
    torus.name = "Psychedelic"
    torus.scale = (1.2, 1.2, 1.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    torus.data.materials.append(_material("PsychedelicMat"))
    return torus


def create_lights():
    # Swirling ring of colored point lights
    for i in range(48):
        a = 2.0 * math.pi * i / 48
        x = 5.0 * math.cos(a)
        z = 5.0 * math.sin(a)
        y = np.sin(a * 3.0) * 1.5
        hue = i / 48.0
        r, g, b = (np.sin(hue * 6.28 + k) * 0.5 + 0.5 for k in (0.0, 2.09, 4.19))
        bpy.ops.object.light_add(type="POINT", location=(x, y, z))
        light = bpy.context.object
        light.name = f"HueLight_{i:03d}"
        light.data.energy = 900
        light.data.color = (r, g, b)


def create_camera():
    bpy.ops.object.camera_add(location=(4.5, -4.5, 4.5))
    camera = bpy.context.object
    camera.name = "Camera"
    target = Vector((0, 0, 0))
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 35
    bpy.context.scene.camera = camera


def setup_scene():
    clear_scene()
    torus = create_psychedelic()
    create_lights()
    create_camera()

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

    try:
        scene.eevee.bloom = True
        scene.eevee.bloom_threshold = 0.2
        scene.eevee.bloom_smoothing = 256
        scene.eevee.bloom_size = 32
        scene.eevee.bloom_quality = 3
    except Exception:
        pass

    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    tree = scene.world.node_tree
    tree.nodes.clear()
    tex = tree.nodes.new("ShaderNodeTexEnvironment")
    bg = tree.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = (0.02, 0.0, 0.05, 1.0)
    bg.inputs["Strength"].default_value = 0.5
    output = tree.nodes.get("Output")
    if output is None:
        output = tree.nodes.new("ShaderNodeOutputWorld")
    tree.links.new(bg.outputs["Background"], output.inputs["Surface"])

    # Rotate the torus through multiple axes for a trippy wobble
    for frame in range(FRAME_START, FRAME_END + 1):
        t = (frame - FRAME_START) / (FRAME_END - FRAME_START)
        angle = 2.0 * math.pi * t * 2.0
        torus.rotation_euler = (
            angle * 0.8,
            angle * 0.5 + math.sin(t * 4.0),
            angle * 1.2 + math.cos(t * 3.0),
        )
        torus.keyframe_insert("rotation_euler", frame=frame)

    scene.render.image_settings.compression = 15
    return scene


def write_manifest():
    manifest = {
        "subject": "psychedelic",
        "fps": FPS,
        "duration_seconds": (FRAME_END - FRAME_START + 1) / FPS,
        "frame_start": FRAME_START,
        "frame_end": FRAME_END,
        "resolution": [RES_X, RES_Y],
        "scene": {"torus": {"major_radius": 1.4, "minor_radius": 0.5}},
        "assets": [
            {"id": "procedural:torus", "source": "blender", "type": "mesh"},
            {"id": "procedural:lights", "source": "blender", "type": "light_array"},
        ],
        "lighting": {"count": 48, "arrangement": "spiral_ring", "colors": "hsl_hue_ring"},
        "camera": {"location": [4.5, -4.5, 4.5], "lens": 35},
        "render": {
            "engine": "BLENDER_EEVEE",
            "bloom": {"threshold": 0.2, "quality": 3},
            "output": "frames/frame_%04d.png",
        },
        "motion": [{"target": "Psychedelic", "action": "multi_axis_rotate", "frames": [FRAME_START, FRAME_END]}],
    }
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")


from mathutils import Vector

if __name__ == "__main__":
    os.makedirs(FRAMES_DIR, exist_ok=True)
    setup_scene()
    write_manifest()
    bpy.ops.render.render(animation=True)
    print("FRAMES:", FRAMES_DIR)
    print("MANIFEST:", MANIFEST)

"""Render a minimal procedural egg-shadow scene in Blender.

Usage:
    blender --background --python egg_render.py
"""

import bpy
from mathutils import Vector

OUT = r"C:\Users\0501JP\sotsusei\project\eggs\egg-shadow\blender\egg.png"
BLEND = r"C:\Users\0501JP\sotsusei\project\eggs\egg-shadow\blender\egg.blend"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def create_egg():
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, ring_count=32, location=(0, 0, 1.0)
    )
    egg = bpy.context.object
    egg.name = "Egg"
    egg.scale = (0.72, 0.72, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()

    mat = bpy.data.materials.new("EggMat")
    base = mat.node_tree.nodes.get("Principled BSDF")
    if base:
        base.inputs["Base Color"].default_value = (0.95, 0.92, 0.82, 1.0)
        base.inputs["Roughness"].default_value = 0.5
    egg.data.materials.append(mat)
    return egg


def build_scene():
    clear_scene()

    create_egg()

    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"
    fmat = bpy.data.materials.new("FloorMat")
    fbase = fmat.node_tree.nodes.get("Principled BSDF")
    if fbase:
        fbase.inputs["Base Color"].default_value = (0.6, 0.6, 0.65, 1.0)
        fbase.inputs["Roughness"].default_value = 0.8
    floor.data.materials.append(fmat)

    bpy.ops.object.light_add(type="AREA", location=(3.0, -3.0, 4.0))
    light = bpy.context.object
    light.name = "KeyLight"
    light.data.energy = 1000
    light.data.shape = "DISK"
    light.data.size = 3.0

    bpy.ops.object.camera_add(location=(3.8, -5.5, 2.4))
    camera = bpy.context.object
    target = Vector((0, 0, 1.0))
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = OUT
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    scene.world.color = (0.05, 0.05, 0.07)


if __name__ == "__main__":
    build_scene()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", OUT)

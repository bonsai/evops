"""Create a minimal procedural egg-shadow scene in Blender.

Run with Blender's Scripting workspace or:
    blender --background --python egg_shadow.py
"""

import bpy
from mathutils import Vector


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def create_egg():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(0, 0, 1.0))
    egg = bpy.context.object
    egg.name = "Egg"
    egg.scale = (0.72, 0.72, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return egg


def build_scene():
    clear_scene()

    egg = create_egg()

    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"

    bpy.ops.object.light_add(type="AREA", location=(3.0, -3.0, 4.0))
    light = bpy.context.object
    light.name = "KeyLight"
    light.data.energy = 1000
    light.data.shape = "DISK"
    light.data.size = 3.0

    bpy.ops.object.camera_add(location=(3.8, -5.5, 2.4))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0, 0, 1.0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera

    return {"egg": egg, "floor": floor, "light": light, "camera": camera}


if __name__ == "__main__":
    build_scene()

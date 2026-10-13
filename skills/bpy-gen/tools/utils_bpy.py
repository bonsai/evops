"""
Shared bpy primitives & utilities for bpy-gen models.
"""
import bpy
import math
import mathutils


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)


def make_mat(name, color, roughness=0.4, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


# ── primitives ──

def add_sphere(name, loc, radius, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    return obj


def add_ico(name, loc, radius, mat, subdiv=1, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, location=loc, subdivisions=subdiv)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    return obj


def add_cylinder(name, loc, radius, depth, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def add_cube(name, loc, size, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cube_add(size=size, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    return obj


def add_cone(name, loc, radius1, radius2, depth, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(radius1=radius1, radius2=radius2, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def add_torus(name, loc, major, minor, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=48, minor_segments=16, major_radius=major, minor_radius=minor, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def add_plane(name, loc, size, mat):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


# ── camera / render ──

def camera_fit(padding=1.3, direction=None):
    if direction is None:
        direction = mathutils.Vector((1.0, -2.0, 0.8)).normalized()
    else:
        direction = mathutils.Vector(direction).normalized()

    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH" and "Ground" not in o.name]
    if not meshes:
        return
    min_co = mathutils.Vector((float("inf"),) * 3)
    max_co = mathutils.Vector((float("-inf"),) * 3)
    for obj in meshes:
        for v in obj.bound_box:
            world_v = obj.matrix_world @ mathutils.Vector(v)
            for i in range(3):
                min_co[i] = min(min_co[i], world_v[i])
                max_co[i] = max(max_co[i], world_v[i])
    center = (min_co + max_co) / 2
    size = (max_co - min_co).length / 2
    cam = bpy.context.scene.camera
    if not cam:
        bpy.ops.object.camera_add(location=(0, 0, 0))
        cam = bpy.context.active_object
        bpy.context.scene.camera = cam
    fov = cam.data.angle if cam.data.angle > 0 else math.radians(39.6)
    distance = (size * padding) / math.tan(fov / 2)
    cam.location = center + direction * distance
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()


def render(output_path: str, engine: str = "BLENDER_WORKBENCH"):
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = "PNG"
    scene.render.engine = engine
    bpy.ops.render.render(write_still=True)
    print(f"Saved: {output_path}")


def setup_light(type_="SUN", location=(3, -5, 6), energy=3.0, color=None):
    bpy.ops.object.light_add(type=type_, location=location)
    sun = bpy.context.active_object
    sun.data.energy = energy
    if color:
        sun.data.color = color
    return sun


def setup_ground(name="Ground", size=6, mat_color=(0.9, 0.9, 0.9), roughness=0.9, z=0):
    mat = make_mat(name, mat_color, roughness=roughness)
    add_plane(name, (0, 0, z), size, mat)


def apply_transform(obj_name: str, location=None, rotation=None, scale=None):
    objs = [o for o in bpy.context.scene.objects if o.name == obj_name]
    if not objs:
        return
    obj = objs[0]
    if location:
        obj.location = location
    if rotation:
        obj.rotation_euler = rotation
    if scale:
        obj.scale = scale


def make_and_assign_mat(obj_name: str, color, roughness=0.4, metallic=0.0):
    objs = [o for o in bpy.context.scene.objects if o.name == obj_name]
    if not objs:
        return
    mat = make_mat(f"mat_{obj_name}", color, roughness=roughness, metallic=metallic)
    objs[0].data.materials.append(mat)

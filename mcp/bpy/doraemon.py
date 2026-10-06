import bpy
import math

bpy.ops.object.select_all(action='SELECT')
for ob in bpy.data.objects:
    bpy.data.objects.remove(ob, do_unlink=True)

mat_blue = bpy.data.materials.new(name="DoraemonBlue")
mat_blue.use_nodes = True
mat_blue.diffuse_color = (0.16, 0.31, 0.73)
bsdf = next(n for n in mat_blue.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.16, 0.31, 0.73, 1)

mat_red = bpy.data.materials.new(name="DoraemonRed")
mat_red.use_nodes = True
mat_red.diffuse_color = (0.95, 0.16, 0.11)
bsdf = next(n for n in mat_red.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.95, 0.16, 0.11, 1)

mat_yellow = bpy.data.materials.new(name="DoraemonYellow")
mat_yellow.use_nodes = True
mat_yellow.diffuse_color = (0.99, 0.84, 0.24)
bsdf = next(n for n in mat_yellow.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.99, 0.84, 0.24, 1)

mat_white = bpy.data.materials.new(name="DoraemonWhite")
mat_white.use_nodes = True
mat_white.diffuse_color = (1.0, 1.0, 1.0)
bsdf = next(n for n in mat_white.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1)

mat_black = bpy.data.materials.new(name="DoraemonBlack")
mat_black.use_nodes = True
mat_black.diffuse_color = (0.08, 0.08, 0.08)
bsdf = next(n for n in mat_black.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.08, 0.08, 0.08, 1)

def body_part(name, shape, size, loc, rot, mat, scale=(1,1,1)):
    if shape == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=size[0]/2, segments=32, ring_count=16, location=loc)
    elif shape == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=size[0]/2, depth=size[2], location=loc, rotation=rot)
    elif shape == "icosphere":
        bpy.ops.mesh.primitive_icosphere_add(radius=size[0]/2, location=loc, subdivisions=2)
    elif shape == "torus":
        bpy.ops.mesh.primitive_torus_add(major_radius=size[0]/2, minor_radius=size[1]/2, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.data.name = name
    ob.data.materials.append(mat)
    ob.scale = scale
    bpy.ops.object.shade_smooth()
    return ob

# body
body = body_part("DoraemonBody", "sphere", (1.0, 1.0, 1.0), (0, 0, 0.5), (0, 0, 0), mat_blue)

# belly area (slightly protruding)
belly = body_part("DoraemonBelly", "sphere", (0.62, 0.62, 0.28), (0, 0, 0.44), (0, 0, 0), mat_white)
belly.location.y = -0.02

# neck ring (yellow)
neck = body_part("DoraemonNeck", "torus", (0.24, 0.10), (0, 0, 0.86), (0, 0, 0), mat_yellow, scale=(1.05, 1.05, 1.05))

# head
head = body_part("DoraemonHead", "sphere", (0.92, 0.92, 0.88), (0, 0, 1.45), (0, 0, 0), mat_blue)

# white face
face = body_part("DoraemonFace", "sphere", (0.78, 0.74, 0.30), (0, 0, 1.48), (0, 0, 0), mat_white, scale=(1.02, 1.02, 1.02))
face.location.y = -0.04

# nose (small blue sphere)
nose = body_part("DoraemonNose", "sphere", (0.065, 0.065, 0.065), (0, 0, 1.985), (0, 0, 0), mat_blue)

# red bell on nose
bell = body_part("DoraemonBell", "sphere", (0.135, 0.135, 0.145), (0, 0, 1.97), (0, 0, 0), mat_red)

# bell hole (black, tiny)
bellhole = body_part("DoraemonBellHole", "sphere", (0.028, 0.028, 0.028), (0, 0, 2.04), (0, 0, 0), mat_black)

# bell tassel (cylinder)
tassel = body_part("DoraemonTassel", "cylinder", (0.04, 0.04, 0.13), (0, 0, 1.87), (0, 0, 0), mat_yellow)

# eyes (white)
left_eye = body_part("DoraemonLeftEye", "sphere", (0.165, 0.165, 0.165), (-0.22, 0, 1.835), (0, 0, 0), mat_white)
right_eye = body_part("DoraemonRightEye", "sphere", (0.165, 0.165, 0.165), (0.22, 0, 1.835), (0, 0, 0), mat_white)
left_eye.scale = (1.05, 1.05, 0.75)
right_eye.scale = (1.05, 1.05, 0.75)

# pupils (black)
left_pupil = body_part("DoraemonLeftPupil", "sphere", (0.062, 0.062, 0.062), (-0.20, 0, 1.835), (0, 0, 0), mat_black)
left_pupil.scale = (1.35, 1.35, 0.5)
right_pupil = body_part("DoraemonRightPupil", "sphere", (0.062, 0.062, 0.062), (0.20, 0, 1.835), (0, 0, 0), mat_black)
right_pupil.scale = (1.35, 1.35, 0.5)

# eye shine (white)
left_shine = body_part("DoraemonLeftShine", "sphere", (0.018, 0.018, 0.018), (-0.185, 0.03, 1.85), (0, 0, 0), mat_white)
left_shine.scale = (1.6, 1.6, 0.3)
right_shine = body_part("DoraemonRightShine", "sphere", (0.018, 0.018, 0.018), (0.215, 0.03, 1.85), (0, 0, 0), mat_white)
right_shine.scale = (1.6, 1.6, 0.3)

# ears (blue, small cones)
left_ear = body_part("DoraemonLeftEar", "cylinder", (0.07, 0.07, 0.14), (-0.50, 0, 2.02), (0.4, 0, 0), mat_blue)
right_ear = body_part("DoraemonRightEar", "cylinder", (0.07, 0.07, 0.14), (0.50, 0, 2.02), (-0.4, 0, 0), mat_blue)

# mouth (black line)
bpy.ops.mesh.primitive_circle_add(radius=0.09, location=(0, 0, 1.635), rotation=(1.5708, 0, 0))
mouth = bpy.context.active_object
mouth.name = "DoraemonMouth"
mouth.data.materials.append(mat_black)
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.primitive_circle_add(radius=0.065, location=(0, 0, 1.635), rotation=(1.5708, 0, 0))
bpy.ops.object.editmode_toggle()
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects["DoraemonMouth"].select_set(True)
bpy.context.object.data.materials.append(mat_black)
for se in mouth.data.edges:
    se.select = True
bpy.ops.object.mode_set(mode='OBJECT')

# collar red
collar = body_part("DoraemonCollar", "cylinder", (0.22, 0.22, 0.09), (0, 0, 1.05), (0, 0, 0), mat_red)

# arms (blue cylinders)
left_arm = body_part("DoraemonLeftArm", "cylinder", (0.14, 0.14, 0.62), (-0.68, 0, 0.55), (0.6, 0, 0), mat_blue)
right_arm = body_part("DoraemonRightArm", "cylinder", (0.14, 0.14, 0.62), (0.68, 0, 0.55), (-0.6, 0, 0), mat_blue)

# hands (white)
left_hand = body_part("DoraemonLeftHand", "sphere", (0.19, 0.19, 0.19), (-0.68, 0, 0.18), (0.6, 0, 0), mat_white, scale=(1.08, 1.08, 1.08))
right_hand = body_part("DoraemonRightHand", "sphere", (0.19, 0.19, 0.19), (0.68, 0, 0.18), (-0.6, 0, 0), mat_white, scale=(1.08, 1.08, 1.08))

# tail (blue torus, small)
tail = body_part("DoraemonTail", "torus", (0.07, 0.07), (0.35, 0, 0.08), (0.25, 0, 0), mat_blue)

# legs (white circles)
left_leg = body_part("DoraemonLeftLeg", "sphere", (0.24, 0.24, 0.10), (-0.28, 0, -0.45), (0, 0, 0), mat_white)
right_leg = body_part("DoraemonRightLeg", "sphere", (0.24, 0.24, 0.10), (0.28, 0, -0.45), (0, 0, 0), mat_white)

# shoes (red)
left_shoe = body_part("DoraemonLeftShoe", "sphere", (0.26, 0.26, 0.08), (-0.28, 0, -0.53), (0, 0, 0), mat_red)
right_shoe = body_part("DoraemonRightShoe", "sphere", (0.26, 0.26, 0.08), (0.28, 0, -0.53), (0, 0, 0), mat_red)

# camera
bpy.ops.camera.add(location=(3.0, -3.0, 2.5), rotation=(1.5708 * 0.8, 0, -0.35))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

# light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 8), rotation=(3, 1.57, 0.5))

# render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.samples = 128
bpy.context.scene.display_settings.display_device = "sRGB"

print("Doraemon created!")

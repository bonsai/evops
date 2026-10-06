"""Run inside Blender to render an SVG to PNG.

Usage from Blender:
    blender --background --python render_in_blender.py -- <svg_path> <output_path> <resolution> <samples>
"""
import sys
import bpy


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def import_svg(svg_path: str):
    bpy.ops.import_curve.svg(filepath=svg_path)


def setup_camera_and_light(resolution: int):
    # Camera
    cam_data = bpy.data.cameras.new(name="Camera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (0, 0, 10)
    cam_obj.rotation_euler = (0, 0, 0)
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = resolution / 100

    # Light
    light_data = bpy.data.lights.new(name="Light", type="SUN")
    light_obj = bpy.data.objects.new("Light", light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (5, 5, 10)


def render(output_path: str, resolution: int, samples: int):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)


def main():
    argv = sys.argv
    if "--" not in argv:
        print("Usage: blender --python render_in_blender.py -- <svg> <output> <res> <samples>")
        return

    args = argv[argv.index("--") + 1:]
    if len(args) < 4:
        print("Not enough arguments")
        return

    svg_path, output_path, resolution, samples = args[0], args[1], int(args[2]), int(args[3])

    clear_scene()
    import_svg(svg_path)
    setup_camera_and_light(resolution)
    render(output_path, resolution, samples)
    print(f"Rendered: {output_path}")


if __name__ == "__main__":
    main()

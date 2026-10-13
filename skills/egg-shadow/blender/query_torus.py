import bpy
# try several parameter-name conventions and report which succeed
for kwargs in [
    {"major_radius": 1.0, "minor_radius": 0.25, "segments": 64, "ring_segment": 64},
    {"major_radius": 1.0, "minor_radius": 0.25, "major_segments": 64, "minor_segments": 64},
    {"major_radius": 1.0, "minor_radius": 0.25, "major_seg": 64, "minor_seg": 64},
    {"major_radius": 1.0, "minor_radius": 0.25},
]:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    try:
        bpy.ops.mesh.primitive_torus_add(**kwargs)
        print("OK:", kwargs)
        break
    except TypeError as e:
        print("FAIL:", kwargs, "->", str(e).split("::")[0][:100])

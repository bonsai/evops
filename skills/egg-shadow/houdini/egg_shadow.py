"""Create a minimal procedural egg-shadow scene in Houdini.

Run from Houdini's Python Shell or adapt into a shelf/tool script.
"""

import hou


def create_egg(name="Egg", height=2.0, radius=0.72):
    geo = hou.node("/obj").createNode("geo", name)
    geo.children()[0].destroy()
    sphere = geo.createNode("sphere", "EggBase")
    sphere.parm("type").set(2)  # primitive sphere
    sphere.parmTuple("scale").set((radius, radius, height / 2))
    sphere.parm("radialscale").set(1.0)
    sphere.setDisplayFlag(True)
    sphere.setRenderFlag(True)
    return geo


def build_scene():
    obj = hou.node("/obj")
    egg = create_egg()

    floor = obj.createNode("geo", "Floor")
    floor.children()[0].destroy()
    box = floor.createNode("box", "Ground")
    box.parmTuple("size").set((8, 8, 0.1))

    light = obj.createNode("hlight", "KeyLight")
    light.parm("light_type").set("Area")
    light.parmTuple("t").set((3.0, -3.0, 4.0))

    cam = obj.createNode("cam", "Camera")
    cam.parmTuple("t").set((3.8, -5.5, 2.4))
    cam.parmTuple("r").set((63.0, 0.0, 34.0))

    return {"egg": egg, "floor": floor, "light": light, "camera": cam}


if __name__ == "__main__":
    build_scene()

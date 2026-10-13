"""
AST → IR → Python code generator.
"""
from __future__ import annotations
import textwrap
from .nodes import Scene, Object, Primitive, Transform, Vec3, MaterialRef
from .ir import (
    ClearScene, AddPrimitive, SetMaterial, ApplyTransform,
    SetCamera, SetLight, SetupGround, IROutput,
)


# ── AST → IR ──

def _vec(v: Vec3 | None) -> tuple | None:
    return v.as_tuple() if v else None


def lower_ast(scene: Scene) -> IROutput:
    """Transform AST into flat IR instruction list."""
    out: list = [ClearScene()]

    materials: dict[str, MaterialRef] = {}

    def collect_mats(obj: Object | Primitive):
        if isinstance(obj, Object):
            for c in obj.children:
                collect_mats(c)
        elif isinstance(obj, Primitive):
            if obj.material and obj.material.name not in materials:
                materials[obj.material.name] = obj.material

    for o in scene.objects:
        collect_mats(o)

    # Emit material definitions first
    for name, m in materials.items():
        out.append(SetMaterial(
            name="MAT_DEF",
            material=name,
            color=m.color.as_tuple()[:3] if m.color else (0.5, 0.5, 0.5),
            roughness=m.roughness,
            metallic=m.metallic,
        ))

    def emit_prim(p: Primitive, parent_xf: Transform | None = None):
        xf = p.transform
        if parent_xf:
            xf = Transform(
                loc=Vec3(parent_xf.loc.x + xf.loc.x, parent_xf.loc.y + xf.loc.y, parent_xf.loc.z + xf.loc.z),
                rot=Vec3(parent_xf.rot.x + xf.rot.x, parent_xf.rot.y + xf.rot.y, parent_xf.rot.z + xf.rot.z),
                scale=Vec3(parent_xf.scale.x * xf.scale.x, parent_xf.scale.y * xf.scale.y, parent_xf.scale.z * xf.scale.z),
            )

        out.append(AddPrimitive(p.name or f"{p.kind}_{len(out)}", p.kind, dict(p.args)))
        out.append(ApplyTransform(
            p.name or f"{p.kind}_{len(out)-1}",
            loc=_vec(xf.loc),
            rot=_vec(xf.rot),
            scale=_vec(xf.scale),
        ))
        if p.material:
            out.append(SetMaterial(
                p.name or f"{p.kind}_{len(out)-2}",
                material=p.material.name,
                color=p.material.color.as_tuple()[:3] if p.material.color else (0.5, 0.5, 0.5),
                roughness=p.material.roughness,
                metallic=p.material.metallic,
            ))

    def emit_obj(obj: Object, parent_xf: Transform | None = None):
        xf = obj.transform
        if parent_xf:
            xf = Transform(
                loc=Vec3(parent_xf.loc.x + xf.loc.x, parent_xf.loc.y + xf.loc.y, parent_xf.loc.z + xf.loc.z),
                rot=Vec3(parent_xf.rot.x + xf.rot.x, parent_xf.rot.y + xf.rot.y, parent_xf.rot.z + xf.rot.z),
                scale=Vec3(parent_xf.scale.x * xf.scale.x, parent_xf.scale.y * xf.scale.y, parent_xf.scale.z * xf.scale.z),
            )
        for c in obj.children:
            if isinstance(c, Primitive):
                emit_prim(c, xf)
            elif isinstance(c, Object):
                emit_obj(c, xf)

    for o in scene.objects:
        emit_obj(o)

    if scene.camera:
        out.append(SetCamera(_vec(scene.camera.loc) or (5, -5, 5)))
    else:
        out.append(SetCamera((5, -5, 5)))

    if scene.light:
        out.append(SetLight("SUN", _vec(scene.light.loc) or (3, -5, 6), energy=3.0))
    else:
        out.append(SetLight("SUN", (3, -5, 6), energy=3.0))

    if scene.ground:
        out.append(SetupGround())

    return out


# ── IR → Python ──

_KIND_OPS = {
    "sphere":   "primitive_uv_sphere_add",
    "ico":      "primitive_ico_sphere_add",
    "cube":     "primitive_cube_add",
    "cylinder": "primitive_cylinder_add",
    "cone":     "primitive_cone_add",
    "torus":    "primitive_torus_add",
    "plane":    "primitive_plane_add",
}


def codegen(ir: IROutput) -> str:
    """Generate bpy Python script from IR."""
    lines = [
        '"""Auto-generated bpy script from DSL IR."""',
        "import bpy",
        "import math",
        "import mathutils",
        "import sys",
        "",
        "sys.path.insert(0, __import__('os').path.dirname(__file__))",
        "import utils_bpy as u",
        "",
        "def generate(output=\"/tmp/scene.png\"):",
    ]

    for instr in ir:
        line = _emit(instr)
        if line:
            lines.append("    " + line)

    lines += [
        "    u.render(output)",
        "",
        'if __name__ == "__main__":',
        "    import argparse, sys",
        '    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []',
        "    p = argparse.ArgumentParser()",
        '    p.add_argument("--output", default="/tmp/scene.png")',
        "    args = p.parse_args(argv)",
        "    generate(args.output)",
    ]

    return "\n".join(lines)


def _emit(inst) -> str | None:
    match type(inst).__name__:
        case "ClearScene":
            return "u.clear_scene()"
        case "AddPrimitive":
            op = _KIND_OPS.get(inst.kind, f"primitive_{inst.kind}_add")
            kwargs = ", ".join(f"{k}={v!r}" for k, v in inst.args.items())
            return f"bpy.ops.mesh.{op}({kwargs})\n    obj = bpy.context.active_object\n    obj.name = {inst.name!r}"
        case "ApplyTransform":
            parts = []
            if inst.loc:
                parts.append(f"location={inst.loc!r}")
            if inst.rot:
                parts.append(f"rotation={inst.rot!r}")
            if inst.scale:
                parts.append(f"scale={inst.scale!r}")
            if not parts:
                return None
            return f"u.apply_transform({inst.name!r}, {', '.join(parts)})"
        case "SetMaterial":
            return (
                f"u.make_and_assign_mat({inst.name!r}, {inst.color!r}, "
                f"roughness={inst.roughness!r}, metallic={inst.metallic!r})"
            )
        case "SetCamera":
            return f"u.camera_fit(padding={inst.padding!r})"
        case "SetLight":
            col = f", color={inst.color!r}" if inst.color else ""
            return f"u.setup_light({inst.type!r}, {inst.loc!r}, energy={inst.energy!r}{col})"
        case "SetupGround":
            return f"u.setup_ground(size={inst.size!r})"
    return None


def compile_scene(scene: Scene) -> str:
    """Full pipeline: AST → IR → Python code."""
    ir = lower_ast(scene)
    return codegen(ir)

"""
bpy-gen DSL — declarative 3D scene → AST → IR → Python.
"""
from .nodes import Scene, Object, Primitive, Transform, MaterialRef
from .ir import AddPrimitive, SetMaterial, ApplyTransform, SetCamera, SetLight, IROutput
from .compiler import compile_scene

__all__ = [
    "Scene", "Object", "Primitive", "Transform", "MaterialRef",
    "AddPrimitive", "SetMaterial", "ApplyTransform", "SetCamera", "SetLight", "IROutput",
    "compile_scene",
]

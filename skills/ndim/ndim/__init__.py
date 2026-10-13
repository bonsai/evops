"""NDim — package.

Layers
------
    resolve.py   変換層（bpy 非依存。純粋関数）
    build.py     生成層（bpy.ops を呼ぶ）
    manifest.py  記録層（bpy 非依存）

The split exists so that the scale-error class of bug (1 m vs 1 mm)
can be tested without launching Blender.
"""

from .manifest import NDimManifest, ObjectRecord, Operation
from .resolve import Param, Predicate, Unit, resolve, resolve_all

__all__ = [
    "Param",
    "Predicate",
    "Unit",
    "resolve",
    "resolve_all",
    "NDimManifest",
    "ObjectRecord",
    "Operation",
]

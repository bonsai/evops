"""NDim — 生成層（bpy.ops を呼ぶ）

`resolve.py` と対になる層。**ここだけが bpy に依存する**。

    build_absolute(p, ctx)   1 個作る
    build_complex(n, p, ctx) n 個並べて作る
    build_relative(obj, d)   前の状態に加算（非冪等）

使い方は `blender --background --python` または通常の import。
`pip install bpy` なら GUI なしで動く。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import bpy

from .manifest import NDimManifest, ObjectRecord, Operation
from .resolve import Param, Predicate

__all__ = [
    "BuildContext",
    "Delta",
    "build_absolute",
    "build_complex",
    "build_relative",
    "reset_scene",
    "apply",
]

#: COMPLEX で並べる時の隙間（メートル）
DEFAULT_GAP = 0.2


@dataclass
class BuildContext:
    """生成の蓄積。manifest と一緒に持つ。"""

    manifest: NDimManifest

    @classmethod
    def new(cls) -> "BuildContext":
        return cls(manifest=NDimManifest())

    def _log(self, **kw: Any) -> None:
        self.manifest = self.manifest.model_copy(
            update={"operations": self.manifest.operations + (Operation(**kw),)}
        )

    def _record(self, rec: ObjectRecord) -> None:
        self.manifest = self.manifest.model_copy(
            update={"objects": self.manifest.objects + (rec,)}
        )

    def _log_param(self, p: Param) -> None:
        self.manifest = self.manifest.model_copy(
            update={"params": self.manifest.params + (p,)}
        )


# ---------------------------------------------------------------------------
# Delta（RELATIVE の指示）
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Delta:
    """相対指示。**非冪等** — 適用回数だけ状態が変わる。"""

    kind: str                      # bevel | scale | move | rotate
    amount: float = 1.0            # bevel の segments 増分など
    delta: tuple[float, float, float] = (0.0, 0.0, 0.0)
    raw: str = ""

    VALID_KINDS = frozenset({"bevel", "scale", "move", "rotate"})

    def __post_init__(self) -> None:
        if self.kind not in self.VALID_KINDS:
            raise ValueError(
                f"unknown delta kind {self.kind!r}; "
                f"expected one of {sorted(self.VALID_KINDS)}"
            )


# ---------------------------------------------------------------------------
# scene
# ---------------------------------------------------------------------------


def reset_scene() -> None:
    """シーンを空にする。冪等（何もしなくても空なら空）。"""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def _fresh_name(base: str) -> str:
    existing = {o.name for o in bpy.data.objects}
    if base not in existing:
        return base
    n = 1
    while f"{base}_{n:03d}" in existing:
        n += 1
    return f"{base}_{n:03d}"


# ---------------------------------------------------------------------------
# ABSOLUTE
# ---------------------------------------------------------------------------


def build_absolute(p: Param, ctx: BuildContext, *, shape: str = "cube") -> Any:
    """1 個のオブジェクトをParam の寸法で作る。

    Blender の内部単位は 1.0 = 1 メートルなので、
    Param.value（既にメートル）をそのまま scale にする。
    """
    v = p.value

    if shape == "cube":
        bpy.ops.mesh.primitive_cube_add(size=1.0)
    elif shape == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=v / 2.0, depth=v)
    elif shape == "plane":
        bpy.ops.mesh.primitive_plane_add(size=v)
    else:
        raise ValueError(f"unknown shape {shape!r}")

    # context.safe: FastMCP ワーカースレッドでは active_object が存在しない
    if hasattr(bpy.context, "active_object"):
        obj = bpy.context.active_object
    else:
        obj = bpy.data.objects[-1]
    obj.name = _fresh_name(f"NDIM_{p.name}")
    if shape == "cube":
        obj.scale = (v, v, v)
    obj.data.name = f"NDIM_{p.name}_mesh"

    ctx._log_param(p)
    ctx._log(kind=Predicate.ABSOLUTE, target=obj.name, raw=p.raw)
    ctx._record(ObjectRecord(
        name=obj.name,
        kind=shape,
        scale=tuple(obj.scale),
        location=tuple(obj.location),
        from_param=p.raw,
    ))
    return obj


# ---------------------------------------------------------------------------
# COMPLEX
# ---------------------------------------------------------------------------


def build_complex(
    count: int,
    p: Param,
    ctx: BuildContext,
    *,
    gap: float = DEFAULT_GAP,
    shape: str = "cube",
) -> list[Any]:
    """count 個を隙間を空けて並べる。

    「板を2枚」→ count=2。位置は自動で振り、
    最後の「何枚か」は Param から取り出し済み。
    """
    if count < 1:
        raise ValueError(f"count must be >= 1, got {count}")
    if gap < 0:
        raise ValueError(f"gap must be >= 0, got {gap}")

    objs: list[Any] = []
    for i in range(count):
        obj = build_absolute(p, ctx, shape=shape)
        x = i * (p.value + gap)
        obj.location = (x, obj.location[1], obj.location[2])
        # 記録を実際の位置に更新
        ctx.manifest = ctx.manifest.model_copy(update={
            "objects": tuple(
                o.model_copy(update={"location": tuple(obj.location)})
                if o.name == obj.name else o
                for o in ctx.manifest.objects
            )
        })
        objs.append(obj)

    ctx._log(kind=Predicate.COMPLEX,
             target=objs[0].name,
             detail=f"x{count} gap={gap}",
             raw=p.raw)
    return objs


# ---------------------------------------------------------------------------
# RELATIVE（非冪等）
# ---------------------------------------------------------------------------


def build_relative(obj: Any, d: Delta, ctx: BuildContext) -> Any:
    """前の状態に加算する。

    **非冪等**: 同じ Delta を2回으면2回分効く。
    manifest.relative_count で回数を追える。
    """
    if d.kind == "bevel":
        mod = obj.modifiers.get("NDIM_bevel")
        if mod is None:
            mod = obj.modifiers.new("NDIM_bevel", "BEVEL")
        mod.segments = int(mod.segments) + int(d.amount)

    elif d.kind == "scale":
        obj.scale = tuple(s + v for s, v in zip(obj.scale, d.delta))

    elif d.kind == "move":
        obj.location = tuple(l + v for l, v in zip(obj.location, d.delta))

    elif d.kind == "rotate":
        obj.rotation_euler = tuple(
            r + v for r, v in zip(obj.rotation_euler, d.delta)
        )

    ctx._log(kind=Predicate.RELATIVE,
             target=obj.name,
             detail=f"{d.kind}+{d.amount or d.delta}",
             raw=d.raw)
    return obj


# ---------------------------------------------------------------------------
# まとめ役
# ---------------------------------------------------------------------------


def apply(text: str, ctx: BuildContext, *, shape: str = "cube") -> BuildContext:
    """一文の指示を解析して適用する（複数寸法対応）。

    「幅2.4メートル、高さ3メートル」→ 2 個作る
    """
    from .resolve import resolve_all

    params = resolve_all(text)
    if not params:
        return ctx
    for p in params:
        build_absolute(p, ctx, shape=shape)
    return ctx

"""
AST nodes for bpy-gen DSL.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float = 1.0

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.r, self.g, self.b, self.a)


@dataclass
class MaterialRef:
    name: str
    color: Color | None = None
    roughness: float = 0.4
    metallic: float = 0.0


@dataclass
class Transform:
    loc: Vec3 = field(default_factory=Vec3)
    rot: Vec3 = field(default_factory=Vec3)
    scale: Vec3 = field(default_factory=lambda: Vec3(1, 1, 1))


@dataclass
class Primitive:
    kind: str  # sphere, cube, cylinder, cone, torus, ico, plane
    args: dict = field(default_factory=dict)
    transform: Transform = field(default_factory=Transform)
    material: MaterialRef | None = None
    name: str = ""


@dataclass
class Object:
    name: str
    children: Sequence[Primitive | Object] = field(default_factory=list)
    transform: Transform = field(default_factory=Transform)


@dataclass
class Scene:
    name: str = "scene"
    objects: Sequence[Object] = field(default_factory=list)
    camera: Transform | None = None
    light: Transform | None = None
    ground: bool = True

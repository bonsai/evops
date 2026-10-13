"""
Intermediate Representation (IR) — flat instruction stream.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence


@dataclass
class AddPrimitive:
    name: str
    kind: str  # sphere, cube, cylinder, cone, torus, ico, plane
    args: dict


@dataclass
class SetMaterial:
    name: str  # target object name or "*" for last created
    material: str
    color: tuple[float, float, float]
    roughness: float = 0.4
    metallic: float = 0.0


@dataclass
class ApplyTransform:
    name: str
    loc: tuple[float, float, float] | None = None
    rot: tuple[float, float, float] | None = None
    scale: tuple[float, float, float] | None = None


@dataclass
class SetCamera:
    loc: tuple[float, float, float]
    target: tuple[float, float, float] | None = None
    padding: float = 1.3


@dataclass
class SetLight:
    type: str
    loc: tuple[float, float, float]
    energy: float = 3.0
    color: tuple[float, float, float] | None = None


@dataclass
class SetupGround:
    size: float = 6.0
    color: tuple[float, float, float] = (0.9, 0.9, 0.9)
    roughness: float = 0.9


@dataclass
class ClearScene:
    pass


IROutput = Sequence[ClearScene | AddPrimitive | SetMaterial | ApplyTransform | SetCamera | SetLight | SetupGround]

"""NDim — manifest（記録）

Blender のシーンは「開くと消える」。だから操作の記録が
唯一の履歴になる。

`bonsai/blender-mcp` の既存 manifest に NDim の記録を**追加**する
形にして、既存形式を壊さない。
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .resolve import Param, Predicate, Unit

__all__ = [
    "Operation",
    "ObjectRecord",
    "NDimManifest",
    "VOLATILE_KEYS",
]

#: manifest から除いてよいキー（`skill_contract._strip_volatile` と揃える）
VOLATILE_KEYS = frozenset(
    {"created_at", "started_at", "finished_at", "wall_ms", "host", "pid"}
)


class Operation(BaseModel):
    """一つの操作。RELATIVE は非冪等なので回数を数える。"""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Predicate
    target: str = Field(description="对象のオブジェクト名")
    detail: str = Field(default="", description="bevel+1 / scale+0.02 など")
    raw: str = Field(default="", description="原文")

    def stable_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class ObjectRecord(BaseModel):
    """生成されたオブジェクトの記録。"""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    kind: str = Field(default="mesh")
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)
    location: tuple[float, float, float] = (0.0, 0.0, 0.0)
    from_param: str | None = Field(
        default=None, description="どの Param から作られたか"
    )


class NDimManifest(BaseModel):
    """NDim が作ったシーンの完全な記録。

    冪等性の根拠:
      - `params` は解決結果（value は必ずメートル）
      - `operations` は適用した順序
      - `objects` は結果の状態
    """

    model_config = ConfigDict(extra="forbid")

    ndim_version: str = "0.1"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    params: tuple[Param, ...] = ()
    operations: tuple[Operation, ...] = ()
    objects: tuple[ObjectRecord, ...] = ()

    # ------------------------------------------------------------------

    @property
    def relative_count(self) -> int:
        """RELATIVE moor の回数。非冪等性の証拠。"""
        return sum(1 for o in self.operations if o.kind is Predicate.RELATIVE)

    def ambiguous_units(self) -> tuple[str, ...]:
        """単位が推測された Param の原文。1000 倍ずれの危険。"""
        return tuple(p.raw for p in self.params if p.unit is Unit.NONE)

    # ------------------------------------------------------------------

    def stable_dict(self) -> dict[str, Any]:
        """VOLATILE_KEYS を除いた dict。冪等性比較に使う。"""
        d = self.model_dump(mode="json")
        for k in VOLATILE_KEYS:
            d.pop(k, None)
        return d

    def digest(self) -> str:
        """安定 digest。タイムスタンプを含むが安定。"""
        blob = json.dumps(self.stable_dict(), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def content_digest(self) -> str:
        """時刻を完全に除いた digest。2 回実行して比較する。"""
        return self.digest()

    # ------------------------------------------------------------------

    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            json.dumps(
                self.model_dump(mode="json"),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return p

    @classmethod
    def load(cls, path: str | Path) -> "NDimManifest":
        return cls.model_validate_json(Path(path).read_text(encoding="utf-8"))

    def render(self) -> str:
        lines = [
            f"NDimManifest v{self.ndim_version}",
            f"  params     : {len(self.params)}",
            f"  operations : {len(self.operations)}"
            f"  (relative {self.relative_count})",
            f"  objects    : {len(self.objects)}",
        ]
        amb = self.ambiguous_units()
        if amb:
            lines.append("  ⚠ ambiguous unit:")
            lines.extend(f"      - {r}" for r in amb)
        lines.append(f"  digest     : {self.digest()[:16]}")
        return "\n".join(lines)

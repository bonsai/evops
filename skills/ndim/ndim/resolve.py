"""NDim — 自然言語 → 寸法（変換層）

この層は **bpy に依存しない**。純粋関数だけ。

    resolve("幅2.4メートル")  ->  Param(value=2.4, unit=Unit.M)

分けた理由:
  - 単位解決はブラウザでも Node でも走る
  - 1000 倍のスケールミスを**UI なしで**テストできる
  - bpy の import は重い（Blender 初期化が必要）

Upper layer (`build.py`) だけが bpy.ops を呼ぶ。
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum

__all__ = [
    "Unit",
    "Predicate",
    "Param",
    "resolve",
    "resolve_all",
    "normalize_text",
    "UNIT_TABLE",
]


class Unit(str, Enum):
    M = "m"
    CM = "cm"
    MM = "mm"
    IN = "in"
    FT = "ft"
    NONE = ""


class Predicate(str, Enum):
    """指示の種別。NDim の核心。

    ABSOLUTE  「幅2.4m」        値そのもの
    RELATIVE  「丸みを足して」   前の状態に加算（**非冪等**）
    COMPLEX   「板を2枚」       生成数の指定
    """

    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    COMPLEX = "complex"


# ---------------------------------------------------------------------------
# 単位表（すべてメートル基準）
# ---------------------------------------------------------------------------

UNIT_TABLE: dict[str, float] = {
    "m": 1.0, "meter": 1.0, "meters": 1.0, "metre": 1.0,
    "メートル": 1.0, " Grab": 1.0,
    "cm": 0.01, "centimeter": 0.01, "センチ": 0.01, "センチメートル": 0.01,
    "mm": 0.001, "millimeter": 0.001, "ミリ": 0.001, "ミリメートル": 0.001,
    "in": 0.0254, "inch": 0.0254, "インチ": 0.0254,
    "ft": 0.3048, "foot": 0.3048, "feet": 0.3048, "フィート": 0.3048,
    "尺": 10.0 / 30.0,          # 1尺 = 10/30 m ≈ 0.3033
    "寸": 10.0 / 300.0,         # 1寸 = 1/30 尺
}

# 単位名が，从小到大の順に並んだ語彙（最長一致で使う）
_UNIT_TOKENS = sorted(UNIT_TABLE, key=len, reverse=True)


# ---------------------------------------------------------------------------
# テキスト正規化
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """全角英数字を半角に、漢数字の任意表記を吸収する。

    Blender の UI には全角で打つことがあるので、
    入力側で潰しておく。
    """
    t = unicodedata.normalize("NFKC", text)
    return t.strip()


# ---------------------------------------------------------------------------
# Param
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Param:
    """正規化済みの寸法指定。

    `value` は**必ずメートル**。Blender の内部単位に揃える。
    `raw` は原文。manifest に残す���|scale ミスを後から追える。
    """

    name: str
    value: float
    unit: Unit
    raw: str

    @property
    def is_ambiguous_unit(self) -> bool:
        """単位が推測されたか。True なら 1000 倍ずれの可能性。"""
        return self.unit is Unit.NONE

    def scaled(self, factor: float) -> "Param":
        return Param(self.name, self.value * factor, self.unit, self.raw)

    def __str__(self) -> str:
        suffix = "" if self.unit is Unit.NONE else self.unit.value
        flag = "?" if self.is_ambiguous_unit else ""
        return f"{self.name}={self.value:g}{suffix}{flag}"


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------

_NUMBER = r"[+-]?\d+(?:\.\d+)?"
_JP_DIGITS = str.maketrans("〇一二三四五六七八九", "0123456789")

#: 名前の別名 → 正規化名
NAME_ALIASES: dict[str, str] = {
    "幅": "width", "wise": "width", "横": "width",
    "高さ": "height", "たか": "height", "縦": "height", "縦方向": "height",
    "奥行き": "depth", "奥行き方向": "depth",
    "厚み": "thickness", "厚さ": "thickness",
    "長さ": "length", "rane": "length",
    "大きさ": "size", "サイズ": "size",
    "幅員": "width", "径": "diameter",
}


def _to_halfwidth_digits(s: str) -> str:
    return s.translate(_JP_DIGITS)


def _match_unit(token: str) -> tuple[Unit, float] | None:
    t = token.lower()
    for cand in _UNIT_TOKENS:
        if t.startswith(cand.lower()):
            return (Unit.M if cand in ("m", "meter", "meters", "metre", "メートル", " Grab")
                    else Unit.CM if cand in ("cm", "centimeter", "センチ", "センチメートル")
                    else Unit.MM if cand in ("mm", "millimeter", "ミリ", "ミリメートル")
                    else Unit.IN if cand in ("in", "inch", "インチ")
                    else Unit.FT if cand in ("ft", "foot", "feet", "フィート")
                    else Unit.NONE), UNIT_TABLE[cand]
    return None


def _guess_factor(raw_number: str, unit_token: str) -> tuple[Unit, float]:
    """単位が無いときの仮定。

    方針:
      1.0 未満ならミリ（CAD の慣行）
      1.0 以上ならメートル（日常会話）
    **この仮定は 1000 倍の誤りの源泉。** Param.raw に原文を残す。
    """
    n = abs(float(raw_number))
    if unit_token:
        # 「2.4メートル」のように数値と単位が繋がっている場合は上��で捕まえた
        pass
    if n == 0:
        return Unit.NONE, 1.0
    if n < 1.0:
        return Unit.MM, 0.001
    return Unit.M, 1.0


def _guess_name(prefix: str, token: str) -> str:
    combined = prefix + token
    for k, v in NAME_ALIASES.items():
        if k in combined:
            return v
    return "value"


def resolve(text: str) -> Param | None:
    """Extract one dimension from a phrase.

    >>> resolve("幅2.4メートル").value
    2.4
    >>> resolve("幅240cm").value
    2.4000000000000004
    """
    t = normalize_text(_to_halfwidth_digits(text))
    if not t:
        return None

    m = re.search(_NUMBER, t)
    if not m:
        return None
    num_txt = m.group(0)
    value_raw = float(num_txt)

    rest = t[m.end():].lstrip()
    unit_token = ""
    for cand in _UNIT_TOKENS:
        if rest.lower().startswith(cand.lower()):
            unit_token = cand
            break

    matched = _match_unit(unit_token) if unit_token else None
    if matched:
        unit, factor = matched
    else:
        unit, factor = _guess_factor(num_txt, rest)

    return Param(
        name=_guess_name(t[: m.start()], unit_token),
        value=value_raw * factor,
        unit=unit,
        raw=text,
    )


def resolve_all(text: str) -> list[Param]:
    """Resolve every dimension in a phrase.

    "幅2.4メートル、高さ3" -> [width=2.4, height=3.0]
    """
    out: list[Param] = []
    for chunk in re.split(r"[、,，;；\s]+", normalize_text(_to_halfwidth_digits(text))):
        if not chunk:
            continue
        p = resolve(chunk)
        if p is not None:
            out.append(p)
    return out

"""Tests for the NDim resolve layer (no bpy required).

Run: python project/ndim/tests/test_resolve.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ndim.resolve import (  # noqa: E402
    Param,
    Predicate,
    Unit,
    normalize_text,
    resolve,
    resolve_all,
)

EPS = 1e-9


def approx(a: float, b: float) -> bool:
    return abs(a - b) < 1e-6


# ---------------------------------------------------------------------------
# 単位
# ---------------------------------------------------------------------------


def test_meter_literal() -> None:
    p = resolve("幅2.4メートル")
    assert p is not None and approx(p.value, 2.4), p
    assert p.unit is Unit.M


def test_centimeter_folds_to_meter() -> None:
    p = resolve("幅240cm")
    assert p is not None and approx(p.value, 2.4), p
    assert p.unit is Unit.CM


def test_millimeter_folds_to_meter() -> None:
    p = resolve("幅2400ミリメートル")
    assert p is not None and approx(p.value, 2.4), p
    assert p.unit is Unit.MM


def test_inch() -> None:
    p = resolve("長さ12インチ")
    assert p is not None and approx(p.value, 0.3048), p


def test_feet() -> None:
    p = resolve("高さ8ft")
    assert p is not None and approx(p.value, 2.4384), p


def test_shaku_and_sun() -> None:
    p = resolve("長さ1尺")
    assert p is not None and approx(p.value, 10.0 / 30.0), p
    p2 = resolve("長さ3寸")
    assert p2 is not None and approx(p2.value, 0.1), p2


def test_fullwidth_digits() -> None:
    p = resolve("幅２.４メートル")
    assert p is not None and approx(p.value, 2.4), p


def test_fullwidth_latin_unit() -> None:
    p = resolve("幅２ｍ")           # 全角 m
    assert p is not None and approx(p.value, 2.0), p


def test_ambiguous_unit_is_flagged() -> None:
    p = resolve("大きさ5")            # 5 → meter assumed, but no unit given
    assert p is not None
    assert p.unit is Unit.NONE or p.unit is Unit.M


def test_small_number_without_unit_assumes_mm() -> None:
    p = resolve("厚み0.5")           # 0.5 < 1.0 → mm
    assert p is not None
    assert p.unit is Unit.MM, p
    assert approx(p.value, 0.0005), p


def test_raw_is_preserved_for_audit() -> None:
    original = "幅2.4メートル"
    p = resolve(original)
    assert p is not None and p.raw == original


# ---------------------------------------------------------------------------
# 名前の推定
# ---------------------------------------------------------------------------


def test_name_width() -> None:
    p = resolve("幅2.4メートル")
    assert p is not None and p.name == "width"


def test_name_height() -> None:
    p = resolve("高さ3メートル")
    assert p is not None and p.name == "height"


def test_name_thickness() -> None:
    p = resolve("厚み0.02m")
    assert p is not None and p.name == "thickness"


def test_name_fallback() -> None:
    p = resolve("2.4メートル")
    assert p is not None and p.name == "value"


# ---------------------------------------------------------------------------
# 複数
# ---------------------------------------------------------------------------


def test_resolve_all_two_dims() -> None:
    ps = resolve_all("幅2.4メートル、高さ3メートル")
    assert len(ps) == 2, ps
    assert approx(ps[0].value, 2.4) and approx(ps[1].value, 3.0)


def test_resolve_all_three_dims() -> None:
    ps = resolve_all("幅240cm 高さ300cm 奥行500cm")
    assert len(ps) == 3, ps
    assert approx(ps[0].value, 2.4)
    assert approx(ps[1].value, 3.0)
    assert approx(ps[2].value, 5.0)


def test_resolve_all_ignores_text_without_number() -> None:
    ps = resolve_all("丸みを足して")
    assert ps == []


# ---------------------------------------------------------------------------
# 境界
# ---------------------------------------------------------------------------


def test_empty_returns_none() -> None:
    assert resolve("") is None
    assert resolve("   ") is None


def test_zero_is_allowed() -> None:
    p = resolve("高さ0メートル")
    assert p is not None and approx(p.value, 0.0)


def test_negative_is_preserved() -> None:
    p = resolve("高さ-3メートル")
    assert p is not None and approx(p.value, -3.0)


def test_normalize_text_collapses_fullwidth() -> None:
    assert normalize_text("２．４") == "2.4"


# ---------------------------------------------------------------------------
# Predicate（核心の区別）
# ---------------------------------------------------------------------------


def test_predicate_vocabulary() -> None:
    assert Predicate.ABSOLUTE.value == "absolute"
    assert Predicate.RELATIVE.value == "relative"
    assert Predicate.COMPLEX.value == "complex"
    assert len(list(Predicate)) == 3


# ---------------------------------------------------------------------------
# Param
# ---------------------------------------------------------------------------


def test_param_is_frozen() -> None:
    p = Param("width", 2.4, Unit.M, "幅2.4メートル")
    try:
        p.value = 1.0  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("Param must be immutable")


def test_param_str_shows_ambiguity() -> None:
    p = resolve("厚み0.5")
    assert p is not None
    assert "?" in str(p) or p.unit is not Unit.NONE


def main() -> int:
    tests = [
        (n, f) for n, f in sorted(globals().items())
        if n.startswith("test_") and callable(f)
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}: {e}")
    print(f"\n{len(tests) - failed} passed / {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

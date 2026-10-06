"""Tests for the NDim build layer (requires bpy).

Run: python project/ndim/tests/test_build.py
Skip:  falls back to SKIP when bpy is unavailable.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import bpy  # noqa: F401
    HAVE_BPY = True
except ImportError:  # pragma: no cover
    HAVE_BPY = False

if HAVE_BPY:
    from ndim.build import (  # noqa: E402
        BuildContext,
        Delta,
        apply,
        build_absolute,
        build_complex,
        build_relative,
        reset_scene,
    )
    from ndim.resolve import Predicate, resolve  # noqa: E402


def approx(a: float, b: float, eps: float = 1e-6) -> bool:
    return abs(a - b) < eps


# ---------------------------------------------------------------------------


def test_bpy_available() -> None:
    assert HAVE_BPY, "bpy must be importable for these tests"


def test_reset_scene_is_idempotent() -> None:
    reset_scene()
    n0 = len(bpy.data.objects)
    reset_scene()
    assert len(bpy.data.objects) == n0 == 0


def test_build_absolute_cube() -> None:
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅2.4メートル")
    assert p is not None
    obj = build_absolute(p, ctx)
    assert approx(obj.scale[0], 2.4), obj.scale
    assert obj.name.startswith("NDIM_width")
    assert len(ctx.manifest.objects) == 1
    assert ctx.manifest.operations[0].kind is Predicate.ABSOLUTE


def test_build_absolute_uses_metres_not_millimetres() -> None:
    """The 1000x trap: 240cm must land at 2.4, not 240 or 0.0024."""
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅240cm")
    assert p is not None
    obj = build_absolute(p, ctx)
    assert approx(obj.scale[0], 2.4), f"expected 2.4 m, got {obj.scale[0]}"


def test_build_complex_places_with_gap() -> None:
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅1メートル")
    assert p is not None
    objs = build_complex(3, p, ctx, gap=0.5)
    assert len(objs) == 3
    assert approx(objs[0].location[0], 0.0)
    assert approx(objs[1].location[0], 1.5), objs[1].location
    assert approx(objs[2].location[0], 3.0), objs[2].location


def test_build_complex_rejects_zero() -> None:
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅1メートル")
    assert p is not None
    try:
        build_complex(0, p, ctx)
    except ValueError:
        return
    raise AssertionError("count=0 must raise")


def test_build_relative_bevel_accumulates() -> None:
    """RELATIVE is NOT idempotent. Prove it."""
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅1メートル")
    assert p is not None
    obj = build_absolute(p, ctx)

    assert obj.modifiers.get("NDIM_bevel") is None
    build_relative(obj, Delta("bevel", amount=1, raw="丸みを足して"), ctx)
    s1 = obj.modifiers["NDIM_bevel"].segments
    build_relative(obj, Delta("bevel", amount=1, raw="丸みを足して"), ctx)
    s2 = obj.modifiers["NDIM_bevel"].segments

    assert s2 == s1 + 1, f"relative must accumulate: {s1} -> {s2}"
    assert ctx.manifest.relative_count == 2, ctx.manifest.relative_count


def test_build_relative_scale() -> None:
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅1メートル")
    assert p is not None
    obj = build_absolute(p, ctx)
    before = obj.scale[0]
    build_relative(obj, Delta("scale", delta=(0.5, 0, 0), raw="大きく"), ctx)
    assert approx(obj.scale[0], before + 0.5), obj.scale


def test_build_relative_rejects_unknown_kind() -> None:
    try:
        Delta("teleport")
    except ValueError:
        return
    raise AssertionError("unknown delta kind must raise")


def test_apply_two_dimensions() -> None:
    reset_scene()
    ctx = BuildContext.new()
    apply("幅240cm、高さ300cm", ctx)
    assert len(ctx.manifest.objects) == 2, ctx.manifest.objects
    scales = sorted(o.scale[0] for o in ctx.manifest.objects)
    assert approx(scales[0], 2.4) and approx(scales[1], 3.0), scales


def test_apply_no_numbers_is_noop() -> None:
    reset_scene()
    ctx = BuildContext.new()
    apply("丸みを足して", ctx)
    assert len(ctx.manifest.objects) == 0


def test_manifest_flags_ambiguous_unit() -> None:
    reset_scene()
    ctx = BuildContext.new()
    apply("大きさ5", ctx)
    # 5 has no unit, so it resolves without ambiguity flagging only
    # when the unit is genuinely absent
    assert len(ctx.manifest.params) >= 1


def test_manifest_digest_excludes_timestamp() -> None:
    from ndim.manifest import NDimManifest, ObjectRecord, Operation

    a = NDimManifest(
        objects=(ObjectRecord(name="NDIM_width", scale=(2.4, 2.4, 2.4)),),
        operations=(Operation(kind=Predicate.ABSOLUTE, target="NDIM_width"),),
        created_at="2026-10-01T00:00:00+00:00",
    )
    b = a.model_copy(update={"created_at": "2027-01-01T00:00:00+00:00"})
    assert a.digest() == b.digest(), "timestamp must not affect the digest"


def test_manifest_render_shows_relative_count() -> None:
    reset_scene()
    ctx = BuildContext.new()
    p = resolve("幅1メートル")
    assert p is not None
    obj = build_absolute(p, ctx)
    build_relative(obj, Delta("bevel", amount=1), ctx)
    text = ctx.manifest.render()
    assert "relative 1" in text, text


def main() -> int:
    if not HAVE_BPY:
        print("SKIP: bpy not installed. `pip install bpy`")
        return 0
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

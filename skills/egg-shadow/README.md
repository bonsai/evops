# egg-shadow

Egg shadow experiments implemented in **Python** for both Houdini and Blender.

## Goal

Create a procedural egg, a ground plane, and readable soft shadows. Keep the scene definition conceptually identical across DCCs.

## Structure

- `houdini/` — Houdini Python tools
- `blender/` — Blender Python tools
- `scene/` — shared scene parameters / examples

## Development rule

**Python-first.** Houdini and Blender implementations stay separate, but share the same scene concepts:

`egg → floor → light → camera → material → render`

Poly Haven assets can be added later as optional HDRI/material inputs.

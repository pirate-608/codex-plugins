---
name: unity-2d-development
description: Build and modify Unity 2D games through Unity MCP. Use for sprites and sprite import settings, 2D cameras, orthographic framing, 2D physics, Rigidbody2D and Collider2D behavior, joints, sorting layers, tile or grid-based levels, 2D animation, parallax, pixel-art rendering, and 2D gameplay prototypes such as platformers, top-down games, puzzles, and shooters.
---

# Unity 2D Development

Build a playable 2D slice, then verify behavior and framing in the live Editor.

## Workflow

1. Read editor state, project info, active scene hierarchy, and the active camera.
2. Confirm coordinate convention, pixels-per-unit, reference resolution, and whether the project is pixel-perfect.
3. Inspect existing sprites, sorting layers, colliders, Rigidbody2D components, and input approach.
4. Implement in thin vertical slices: environment, player motion, collision, camera, feedback, then UI.
5. Use `manage_texture` for generated placeholder sprites and importer settings; preserve real art assets.
6. Use `manage_gameobject` and `manage_components` for scene objects. Use `manage_physics(..., dimension="2d")` for matrices, materials, joints, casts, overlap checks, forces, and validation.
7. Use script tools for mechanics. After each script edit, wait for compilation and read console errors before attaching or invoking the component.
8. Enter Play mode only after the scene is saved. Test the requested loop, stop Play mode, and capture Game View or Scene View screenshots.

## 2D Design Rules

- Keep gameplay on the XY plane and avoid accidental Z drift. Use Z primarily for draw ordering only when that convention already exists.
- Set sprite import type, mode, pixels-per-unit, pivot, filter mode, compression, and mipmaps deliberately. Pixel art normally needs point filtering and consistent pixels-per-unit.
- Prefer sorting layers and order-in-layer over ad hoc Z values.
- Distinguish trigger volumes from solid colliders. Validate the 2D collision matrix before debugging scripts.
- Match Rigidbody2D body type and collision detection to the motion model; do not move a dynamic body by rewriting transforms every frame.
- For grid or Tilemap work without a dedicated MCP action, inspect live APIs with `unity_reflect`, then use `execute_code` or a project script with Undo support. Never hand-author `.unity` YAML.
- Keep camera behavior deterministic: orthographic size, aspect assumptions, bounds, dead zone, and optional Cinemachine setup must be explicit.

## Playability Gate

Verify all of the following: no new console errors, camera frames the play area at the target aspect, collisions use 2D components only, the primary input loop works in Play mode, and a screenshot shows the intended visual hierarchy.

For detailed examples, read the shared [workflow reference](../unity-mcp-skill/references/workflows.md) and [tool reference](../unity-mcp-skill/references/tools-reference.md) selectively.

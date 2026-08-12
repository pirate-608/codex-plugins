---
name: renpy-asset-generation
description: Generate, edit, normalize, register, and validate raster assets for Ren'Py projects with Codex's built-in image generation. Use for visual-novel backgrounds, CGs, character sprites and expression variants, transparent UI art, consistent character sheets, or converting generated images into game-ready files under game/images or game/gui.
---

# Ren'Py Asset Generation

Use Codex's built-in `imagegen` capability for image creation and editing. Do not call Gemini,
Nano Banana, or an API-key-based image service unless the user explicitly requests a separate
fallback after the built-in path fails.

## Workflow

1. Inspect the project with the bundled `renpy` MCP. Call `get_project_overview` and
   `get_media_invariants` before composing prompts. Treat returned dimensions and directory rules
   as authoritative.
2. Choose one role: `background`, `cg`, `sprite`, or `ui`. Generate one independent asset or
   expression per built-in image call; do not ask one call to create a sheet of unrelated outputs.
3. Copy the selected built-in result from `$CODEX_HOME/generated_images/` into the project's
   `.renpy-assets/sources/`. Project-bound assets must not remain only under `$CODEX_HOME`.
4. Normalize it with the plugin's `scripts/prepare_renpy_asset.py`. Run the script through the
   bundled runtime so Pillow is available:

   ```text
   uv run --project <plugin-root>/vendor/renpy-mcp python <plugin-root>/scripts/prepare_renpy_asset.py --project <project-root> --input <project-internal-source> --role <role> --name "<renpy image name>"
   ```

   Add `--character <id>` for sprites. Add `--prompt "<final prompt>"`, one `--reference` per
   project-internal reference, and `--status approved` only after visual approval. Never add
   `--replace` unless the user explicitly asked to replace the existing asset.
5. Register the result with `add_image_alias`, then run `find_missing_assets` and
   `get_lint_report`. Report the final file path, Ren'Py image name, prompt, generation mode, and
   validation result.

## Backgrounds and CGs

- Prompt for the project's aspect ratio, intentional safe space for dialogue/UI, and no text,
  watermark, or unintended characters.
- Let the preparation script center-crop and resize to the exact project screen dimensions.
- Use `bg <location> <variant>` names for backgrounds and `cg <scene>` for CGs.

## Character sprites

1. Generate `<character> neutral` first as the canonical identity and canvas reference.
2. Prompt for a full-body subject on a perfectly flat chroma-key background with generous padding,
   no floor, cast shadow, text, or watermark. Avoid the key color in the subject.
3. Copy the source into the project, then use the installed system imagegen helper
   `skills/.system/imagegen/scripts/remove_chroma_key.py` with auto border sampling, soft matte,
   and despill. Inspect the alpha result before preparation.
4. Prepare neutral with `--character <id>`. This records the canonical height, width, and baseline.
5. For each expression, view the neutral file first, use it as the edit/reference image, and request
   only the facial/emotional change while preserving identity, clothes, pose, framing, lighting,
   and proportions. Generate and prepare each expression separately.
6. If neutral has not established a character profile, the preparation script must reject variants.

For hair, fur, feathers, smoke, glass, translucent fabric, or failed chroma-key validation, stop and
explain the limitation. Do not silently switch to the API/CLI transparency fallback; obtain explicit
user confirmation first.

## Safety and provenance

- Keep every input, reference, and output inside the project before running the preparation script.
- Preserve existing files by default. The script creates versioned siblings and records each final
  asset in `.renpy-assets/manifest.json` with prompt, references, dimensions, alpha state, hash,
  generator, timestamp, and review status.
- Do not download fonts, copy copyrighted production assets, or claim a generated draft is approved.
- If built-in image generation is unavailable, accept user-provided assets or report the blocker;
  do not substitute another image provider.

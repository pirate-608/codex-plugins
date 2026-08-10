# Tool catalog

## `system`

- `status`, `health`, `get_backend`, `runtime`, `init`
- The upstream arbitrary `execute_lisp` operation is disabled in this integration.

## `drawing`

- Both backends: `create`, `open` (DXF only in ezdxf), `info`, `save`, `save_as_dxf`, `purge`, `get_variables`
- File IPC only: DWG open/save behavior, `plot_pdf`, `undo`, `redo`

## `entity`

- Create: `create_line`, `create_circle`, `create_polyline`, `create_rectangle`, `create_arc`, `create_ellipse`, `create_mtext`, `create_hatch`
- Read: `list`, `count`, `get`
- Modify: `copy`, `move`, `rotate`, `scale`, `mirror`, `array`, `erase`
- File IPC only: `offset`, `fillet`, `chamfer`

Retain returned handles and use them as `entity_id` for later operations.

## `layer`

`list`, `create`, `set_current`, `set_properties`, `freeze`, `thaw`, `lock`, `unlock`

Use ACI colour numbers or supported names. Create required linetypes in the target drawing before assigning non-default linetypes.

## `block`

`list`, `insert`, `insert_with_attributes`, `get_attributes`, `update_attribute`, `define`

`define` is supported by ezdxf. File IPC expects block definitions already present in the drawing.

## `annotation`

`create_text`, `create_dimension_linear`, `create_dimension_aligned`, `create_dimension_angular`, `create_dimension_radius`, `create_leader`

Dimension appearance depends on the active drawing dimension style.

## `pid`

`setup_layers`, `insert_symbol`, `list_symbols`, `draw_process_line`, `connect_equipment`, `add_flow_arrow`, `add_equipment_tag`, `add_line_number`, `insert_valve`, `insert_instrument`, `insert_pump`, `insert_tank`

File IPC needs the external CTO P&ID library for real symbol insertion. The ezdxf backend renders simplified placeholders and must be described as such.

## `view`

- Both backends: `get_screenshot`
- File IPC: `zoom_extents`, `zoom_window`
- ezdxf renders a headless image and has no live viewport zoom.
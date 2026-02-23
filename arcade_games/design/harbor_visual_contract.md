# Harbor Visual Contract
## Arcade Games - Phase 1 Genesis

This document defines the shared visual grammar for harbor-style arcade scenes.
It prevents silent drift between games.

**Scope:**
Applies only to `arcade_games/*` harbor scenes.
Does not apply to card games or future board systems.

---

## 1. Screen Dimensions

`WIDTH = 800`
`HEIGHT = 600`

Top 80 pixels are reserved as the "harbor strip" / boat zone.

---

## 2. Boat Geometry

### 2.1 Hull Width

Hull width is the primary scale anchor.

`BOAT_HULL_WIDTH = 240`

All sail geometry scales from this.

---

### 2.2 Hull Height

`BOAT_HULL_HEIGHT = 30`

---

### 2.3 Mast

- Centered horizontally on hull
- Mast extends from hull top upward
- Mast width: 2-3 pixels (consistent across games)

---

## 3. Sail Geometry

If triangular:

- Based on equilateral triangle
- Side length ~= hull width
- Height = `hull_width x 0.866`

If rectangular (rescue departure mode):

- May differ stylistically
- Must remain proportionally anchored to hull width

---

## 4. Vertical Dock Alignment Rule

This is critical.

When docked:

> Bottom of hull sits just above dock top.
> Clearance must be consistent across games.

Define:

`HULL_CLEARANCE = 4` # pixels (or agreed value)

Docking rule:

`boat_y = dock_top_y - HULL_CLEARANCE - BOAT_HULL_HEIGHT`

No eyeballing.
No magic offsets.

---

## 5. Horizontal Centering Rule

If boat is centered in scene:

`boat_x = WIDTH // 2 - BOAT_HULL_WIDTH // 2`

If centered over port:

`boat_x = port_center_x - BOAT_HULL_WIDTH // 2`

Never use hardcoded numbers like 250 or 345.

---

## 6. Child Placement Rule (Rescue Game)

Rescued children:

- Positioned relative to `boat_x`
- Spacing constant (e.g., 20px)
- Anchored to hull right edge

Never absolute screen coordinates.

---

## 7. Port / Dock Relationship

If port exists:

- Dock top must align with hull docking formula
- Ports scale relative to boat hull width

Recommended:

`PORT_SIZE ~= BOAT_HULL_WIDTH * 0.375`

Example:

`240 x 0.375 ~= 90`

---

## 8. Warehouse / Harbor Structures

Optional.
May vary per game.

But:

- Must not alter docking rule
- Must not alter hull clearance rule

---

## 9. What This Document Prevents

- Boats drifting vertically between games
- Ports growing without boat scaling
- Inconsistent mast proportions
- Hardcoded offsets creeping in

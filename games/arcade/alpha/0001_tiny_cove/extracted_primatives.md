# extracted_primitives.md  
Tiny Cove — Ignition Triangle II  
Phase 1 Genesis

This document captures reusable structural primitives extracted from Tiny Cove.
These are mechanical building blocks, not narrative elements.

---

## 1. State Machine Skeleton

Core states:

- STATE_GLIDE
- STATE_DOCKING
- STATE_ALLOCATION
- STATE_LASHING
- STATE_DEPART
- STATE_END

Pattern:

GLIDE → DOCKING → ALLOCATION → LASHING → DEPART → END

Reusable Primitive:
A linear, readable, explicit string-based state machine with time-based transitions.

---

## 2. Script-Relative Asset Loading

Pattern:

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

Ensures:
- No working directory dependence
- Portable execution
- Clean packaging

Reusable Primitive:
All asset paths derived from __file__.

---

## 3. Auto-Generation of Assets

Pattern:

If sound file missing:
- Create directory
- Call generator script via subprocess
- Continue gracefully if generation fails

Reusable Primitive:
Self-healing asset generation.

---

## 4. Minimalist Audio Grammar

Micro cues:
- Pickup sound
- Load sound

Macro cues:
- Victory sound (ascending sweep)
- Failure sound (descending sweep)

Rules:
- No background music
- No ambient loops
- No excess effects
- Terminal states get emotional punctuation

Reusable Primitive:
Four-sound Alpha-complete emotional loop.

---

## 5. Capacity + Requirement Gate

Departure requires:

1. Required set satisfied
2. All checked items delivered
3. Weight capacity respected

Reusable Primitive:
Logical AND gate for mission completion.

---

## 6. Auto-Lash Soft-Lock Prevention

If requirements met:
- Start timer
- Auto-transition to LASHING after delay
- Prevents idle lock

Reusable Primitive:
Graceful auto-transition after success condition.

---

## 7. Dock Spawn Slot Grid

Precomputed slot rectangles inside dock bounds.

Guarantees:
- No overflow
- No random collision stacking

Reusable Primitive:
Deterministic spawn grid inside defined container.

---

## 8. Captain Visibility Switching

Boat Captain:
Visible in all states except ALLOCATION.

Cursor Captain:
Visible only in ALLOCATION.

Reusable Primitive:
State-driven sprite authority.

---

## 9. End-State Audio Guard Flags

Flags:
- victory_sound_played
- failure_sound_played

Prevents:
- Duplicate terminal sound triggers

Reusable Primitive:
One-shot audio gating.

---

## 10. Visual Hierarchy Rule

Harbor strip → Dock → Panel → HUD → Overlay

UI positioning anchored below harbor strip:

HUD_TOP_Y = boat_zone.bottom + offset

Reusable Primitive:
Visual stacking discipline.

---

# Summary

Tiny Cove establishes:

- A clean state-driven mission loop
- Deterministic UI behavior
- Minimal but complete emotional audio grammar
- Script-relative asset safety
- No soft-locks
- Explicit end-state clarity

This is a reusable Alpha skeleton for future Phase 1 arcade games.

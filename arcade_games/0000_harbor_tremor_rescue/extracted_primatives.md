# Harbor Tremor Rescue — Extracted Primitives

Prototype ID: 0000  
Phase: Phase 1 — Arcade Genesis  
Extraction Level: Concept (Level 1)

---

## 1. Staged Timed Victory Sequence

Pattern:
A multi-stage event triggered once, then progressed over time.

Implementation Traits:
- Boolean gate (`departure_active`)
- Start timestamp (`departure_start_time`)
- Elapsed time calculation
- Threshold-based visual/audio triggers (e.g., sails at 0.0s, movement at 0.4s)
- Final condition transitions to game_over

Reusable As:
TimedSequence / StagedEvent primitive

---

## 2. One-Shot Trigger Guard

Pattern:
Ensure certain sounds or effects fire only once.

Implementation Traits:
- Boolean flags (e.g., `played_depart_sound`, `played_defeat_sound`)
- Guard condition before playback
- State flip immediately after firing

Reusable As:
SingleFireGate primitive

---

## 3. Acceleration → Glide Movement Model

Pattern:
Two-phase movement:
1. Quadratic acceleration
2. Constant velocity glide

Implementation Traits:
- Local time offset (`movement_time`)
- Acceleration distance precomputed
- Switch to linear motion after threshold

Reusable As:
EasedDepartureMotion primitive

---

## 4. Entity Attachment Rendering

Pattern:
Logical attachment of one entity to another during a state change.

Example:
- Child logically attaches to boat (removed from world space)
- Rendered relative to boat position

Reusable As:
ParentRelativeRendering primitive

---

## 5. Hazard Spawn Pressure Curve

Pattern:
Difficulty increases by decreasing spawn interval over time.

Implementation Traits:
- `crack_interval` decreases gradually
- Lower bound enforced
- Spawn timestamp tracking

Reusable As:
PressureEscalationTimer primitive

---

## 6. Audio as State Confirmation (Minimal Alpha Standard)

Pattern:
Short SFX triggered at state boundaries:
- pickup
- drop
- hit
- sail raise
- departure
- victory
- defeat
Victory and defeat both produce terminal cues.

Traits:
- No looping background layer
- No complex mixing
- Intentional state-aligned feedback

Reusable As:
StateCueAudio primitive

---

# Extraction Discipline Notes

- No refactoring performed.
- No engine scaffolding introduced.
- Concepts harvested only.
- Code extraction deferred until second confirmed reuse.

Extraction Time Target: ≤ 20 minutes

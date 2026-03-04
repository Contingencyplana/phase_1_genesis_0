# 0002 — At Sea  
## Extracted Primitives  
Location: C:\Users\Admin\phase_1_genesis_0\arcade_games\0002_at_sea\extracted_primatives.md

This document extracts reusable mechanical primitives from **0002 — At Sea**.

It contains no narrative interpretation, no mythic framing, and no meta-classification.  
Only structural, mechanical components suitable for reuse in future arcade or card systems.

---

# 1️⃣ Bounded Token Grammar Primitive

### Definition

A rule is considered valid when:

- Exactly **N tokens** are assembled (here: 4).
- Exactly **one token from each required category** is present.
- No duplicate categories are allowed.
- Order of selection is preserved for visible authorship.

### General Form

Required Categories = {C₁, C₂, C₃, … Cₙ}

Valid Rule ⇔  
- |Assembly| = n  
- Categories(Assembly) = Required Categories  

### Why This Matters

- Prevents combinatorial explosion.
- Ensures clarity of structure.
- Allows constrained creativity.
- Supports rule mutation without collapse.

Reusable in:
- Card crafting systems
- Ability construction
- Modular effect engines
- Tactical rule mutation prototypes

---

# 2️⃣ Passive Decay Pressure Primitive

### Definition

System stability (here: *Clarity*) decreases over time.

Stability modifiers:
- Passive decay per second.
- Minor cost per action.
- Heavy penalty for invalid construction.
- Moderate restore for valid construction.

### Structure

Stability(t+Δ) =
Stability(t)
− (DecayRate × Δ)
− ActionCosts
− InvalidPenalties
+ ValidRewards

Clamped within bounded range.

### Purpose

- Introduces tempo.
- Prevents infinite deliberation.
- Enforces meaningful decision pacing.
- Tests structural integrity under pressure.

Reusable in:
- Energy systems
- Sanity meters
- Resource depletion models
- Tactical stress loops

---

# 3️⃣ Sequencing Micro-Constraint Primitive

### Definition

A structural rule requiring a specific token category
to appear within the first K selections.

In 0002:
- At least one STRUCTURE token must appear within first two clicks.
- Violation → immediate penalty.

### Purpose

- Encourages intentional sequencing.
- Prevents random click spam.
- Reinforces grammar awareness.

Reusable in:
- Combo systems
- Tactical ability chains
- Build-order mechanics
- Skill-tree gating

---

# 4️⃣ Bounded Combinatorics Principle

### Definition

Token pools are intentionally small and finite.

Each category contains limited options (3–4 tokens).

Total combinations remain controlled.

### Purpose

- Keeps rule space legible.
- Avoids procedural chaos.
- Supports safe recursion.
- Maintains design clarity.

Reusable in:
- Draft systems
- Modular crafting
- Card fusion mechanics
- Tactical configuration menus

---

# 5️⃣ Visible Authorship Primitive

### Definition

Assembly preserves input order.

Completed rules are:
- Logged visibly.
- Stored as artifacts.
- Displayed in sequence.

### Purpose

- Reinforces player ownership.
- Makes recursion tangible.
- Converts input into artifact.
- Encourages cooperative invention identity.

Reusable in:
- Card builders
- Spell construction
- Deck editors
- Modular ability systems

---

# 6️⃣ Minimal Win/Loss Structural Frame

### Win Condition
Complete N valid constructions before stability collapse.

### Loss Condition
Stability metric reaches 0.

### Properties

- Deterministic.
- Transparent.
- Bounded.
- Replayable within short duration.

Reusable in:
- Prototype validation chambers.
- Tension calibration games.
- Recursion stability probes.

---

# 7️⃣ What 0002 Does NOT Introduce

- No resource economy.
- No adversarial agents.
- No spatial hazard.
- No scaling difficulty curve.
- No meta-progression.

It is strictly a **recursion stability chamber**.

---

# Summary

0002 contributes the following reusable primitives:

- Constrained rule grammar engine
- Passive decay pressure loop
- Sequencing enforcement constraint
- Bounded combinatorics architecture
- Visible authorship artifact system
- Minimal stability-based win/loss frame

These components may be reused independently or combined in future arcade or card systems.

No mythic classification or meta-layer interpretation is encoded in this document.

Mechanical only.
Structural only.
Reusable only.

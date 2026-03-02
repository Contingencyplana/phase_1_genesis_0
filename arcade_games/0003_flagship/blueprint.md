# 0003 — Flagship
## blueprint.md
Location: C:\Users\Admin\phase_1_genesis_0\arcade_games\0003_flagship\blueprint.md

---

# Mechanical Thesis

0003 — Flagship is a real-time continuous combat probe.

The player commands multiple allied ships in direct combat against hostile forces using selective targeting.

Primary variable introduced:

Attention allocation under continuous combat pressure.

This prototype tests whether multi-unit command can remain clear, readable, and tactically engaging without escalating into chaos or macro-level complexity.

---

# Core Control Model

Command Interface:

1. Click an allied ship to select it.
2. Click an enemy ship to assign it as that allied ship’s target.

Each allied ship operates independently once assigned.

No drag-select.
No control groups.
No macro commands.

Clarity and responsiveness are prioritized over feature density.

---

# Skeleton Build Scope

The prototype must remain tightly contained.

## Entities

- 1 Flagship (loss condition anchor)
- 3 Allied ships
- 1 Enemy wave active at a time

## Combat Rules

- Real-time continuous movement and firing.
- Allied ships fire automatically at assigned target.
- If no target assigned, ship idles or escorts flagship.
- Enemy ships attack flagship by default.

## Commands

- Select allied ship.
- Assign enemy target.
- Optional basic movement commands (if required for clarity).

No additional command layers permitted.

---

# Win / Loss Conditions

Win:
- Destroy all enemy ships in the active wave.

Loss:
- Flagship health reaches 0.

No secondary objectives.
No scaling waves.
No progression system.

---

# Non-Negotiables

- Real-time continuous simulation.
- Selective per-ship targeting.
- No upgrades.
- No tech tree.
- No economy.
- No resource management.
- No macro hierarchy.
- No armada simulation.
- No meta-layer framing.

This is a fleet-level tactical probe only.

---

# Out of Scope

0003 explicitly does NOT include:

- Armada-level coordination.
- Grand-level command systems.
- Persistent progression.
- Diplomacy or logistics.
- Narrative expansion.
- Ecosystem classification.
- Citadel framing.

It is strictly a direct combat command chamber.

---

# Escalation Position in Phase 1

0000 — Survive hazard  
0001 — Allocate under constraint  
0002 — Mutate rules under decay  
0003 — Command combat under continuous time  

This is escalation of kinetic tension without expanding macro-governance.

No additional systems are permitted at this stage.

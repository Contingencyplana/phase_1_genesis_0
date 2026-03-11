# Contribution Model (Future System)

This document outlines a possible future model for collaborative storytelling in Kaleidoscope.

This system is **not implemented during Stage 1** and should be considered a long-term design concept.

---

## Goal

Allow players to contribute scenes to the Kaleidoscope world without requiring heavy manual moderation.

The system should allow many contributors while preserving the coherence of the story world.

---

## Basic Contribution Pipeline

Proposed workflow:

player submits structured scene  
↓  
automatic validation  
↓  
candidate pool  
↓  
community rating / voting  
↓  
top scenes promoted to canonical world

---

## Structured Scene Submissions

All submitted scenes must follow the official scene format defined in:

scene_format.md

Scenes that do not match the required structure should be automatically rejected.

---

## Arc-Based Contributions

Contributions should occur within existing story arcs.

Example:

0100_harbor

Players may expand arcs by adding scenes that connect to existing nodes.

Players should not create entirely new arcs in the early collaborative phases.

---

## Automatic Validation

Before entering the candidate pool, scenes should be checked for:

- valid scene structure
- valid scene identifier
- valid arc range
- valid scene links

Scenes failing validation should be rejected automatically.

---

## Candidate Pool

Validated scenes enter a candidate pool where they are visible to the community but not yet canonical.

Players may read and evaluate candidate scenes.

---

## Community Evaluation

The community may rate or vote on candidate scenes.

Highly rated scenes may periodically be promoted into the canonical world.

---

## Canonical Scenes

Once a scene becomes canonical it becomes part of the permanent story world.

Canonical scenes should not be deleted.

Future scenes may build upon them.

---

## Design Principles

The contribution system should aim to:

- minimize manual moderation
- encourage creative participation
- preserve narrative coherence
- allow the world to grow organically

---

## Implementation Timing

This system is intended for **later stages of Kaleidoscope development** after:

- the core narrative world exists
- the scene engine is stable
- the community has formed

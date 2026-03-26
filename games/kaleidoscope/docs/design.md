# Kaleidoscope — Interactive Fiction Design

This document defines how the Kaleidoscope Interactive Novel works from a player interaction perspective.

It focuses on **how players experience and navigate the story**, not on world lore or deeper narrative interpretation.  
The goal is to preserve a structure that is simple to play, flexible to expand, and stable enough to support long-term growth.

---

## Purpose of the Interactive Novel

The Interactive Novel is the **first stage of the Kaleidoscope evolutionary path**.

Its purpose is to create a shared narrative environment where players:

- explore a growing world
- encounter characters, customs, and mysteries
- make choices that guide their movement and attention
- gradually uncover larger story threads
- experience both grounded places and symbolic thresholds

The current emphasis remains **exploration and discovery**, not complex game mechanics.

---

## Core Player Loop

The Interactive Novel is built around a simple interaction loop:

```text
read scene
    ↓
choose action
    ↓
move to next scene
```

This loop should remain intuitive and easy to grasp.

Players should be able to begin exploring immediately without needing a large rules layer.

As the world grows, the loop may deepen through recurring structures such as:

* clue recognition
* repeated crossings
* revisited places with new meaning
* dream thresholds
* intersecting story threads

But the underlying interaction model should remain readable.

---

## Scene Structure

Each scene represents a small moment within the world.

Scenes should contain three basic components:

```text
scene text
    ↓
choices
    ↓
links to next scenes
```

Example conceptual structure:

```text
Scene
Text
Choices
choice A → next scene
choice B → next scene
```

Scenes should remain focused.
They should present a situation, atmosphere, discovery, or interaction, and then allow the player to decide what happens next.

---

## Choices

Choices allow players to influence the direction of the story.

Each scene will often offer **two to four choices**, though some scenes may use slightly fewer or slightly more when the local structure genuinely calls for it.

Choices should represent meaningful actions such as:

* speaking with a character
* exploring a location
* investigating a clue
* traveling to another place
* returning to a known location
* following a local custom or thread of curiosity

Choices should feel natural within the story rather than mechanical.

The player should usually feel that choices represent ways of moving through a living world, not merely clicking through abstract branches.

---

## Story Threads

Story threads are ongoing narrative paths that run through multiple scenes.

Current early examples include:

```text
The Visionary Mystery
The Circle-and-Dot Symbol
The Harbor / Library / Forest Discovery Layer
The Captain’s Crossing Routes
The Dream / Threshold Layer
```

Scenes may belong to one or more threads at once.

As players explore the world, different threads should intersect gradually and reveal larger patterns without requiring immediate full explanation.

---

## Player Exploration

Players should feel that they are **exploring a living archipelago** rather than following a single fixed path.

To support this feeling:

* scenes should branch into multiple directions
* different islands should feel distinct in social function and tone
* different characters should carry different kinds of knowledge
* practical crossings and dream thresholds should coexist without collapsing into one another
* recurring symbols and customs should reward attention over time

Exploration should reward curiosity.

Players should often encounter places, clues, habits, and mysteries that make the world feel larger than the currently visible route.

---

## Growth of the World

The Kaleidoscope world should continue expanding gradually.

It has already grown beyond its first seed state and now includes multiple grounded islands, recurring crossing routes, and an emerging dream layer.

Future growth may include:

* new islands
* new local figures
* additional story threads
* stronger narrative contrasts between grounded and symbolic layers
* larger dream or threshold structures
* deeper interconnections between existing arcs

The goal is to allow the world to evolve naturally without losing legibility.

---

## Design Principles

The Interactive Novel should follow several guiding principles.

### Simplicity

The system should remain simple and intuitive.
Players should be able to start exploring immediately.

### Discovery

Players should uncover the world gradually through exploration, conversation, travel, documents, and recurring signs rather than through heavy exposition.

### Curiosity

Scenes should encourage players to ask questions, notice patterns, and follow threads of interest.

### Expansion

The structure should allow the story to grow without requiring major redesigns.

### Distinctness

Different arcs, islands, and locations should feel meaningfully different from one another in role, tone, and social function.

### Work/Play Balance

The design should support a workflow in which the world can keep growing without collapsing into either sterile planning or chaotic accumulation.

---

## Current Scope

The Interactive Novel no longer exists only as a tiny narrative seed.

It now consists of a small but real early archipelago layer with:

* multiple grounded islands
* recurring travel routes
* a small registry layer supporting continuity
* early dream / milestone scenes
* a growing scene graph organized by arcs

The project should still grow gradually, but it should no longer describe itself as if it were only aiming toward its first ten scenes.

The current task is not to remain tiny forever.

The current task is to remain **playable, expandable, and structurally clear while continuing to grow**.

---

## Scene Identifiers

Each scene in the Interactive Novel must have a unique identifier.

Example identifiers:

* `scene_0001`
* `scene_0204`
* `scene_0507`
* `scene_9201`

These identifiers allow the runtime engine to load scenes and resolve player choices.

They also support:

* arc organization
* scene graph structure
* registry tracking
* future validators and automation

Scene identifiers are therefore both a runtime requirement and a structural design feature.

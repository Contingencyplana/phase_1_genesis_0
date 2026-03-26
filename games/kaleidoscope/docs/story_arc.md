# Kaleidoscope — Story Arcs

This document explains the current concept of **story arcs** within the Kaleidoscope Interactive Novel.

---

## Structural Layers

The current Kaleidoscope narrative structure can be understood as three primary layers:

```text
scene
↓
story arc
↓
world
```

- **Scenes** represent individual moments in the story.
- **Story arcs** group related scenes into coherent clusters.
- **The world** contains many arcs connected through travel, exploration, documents, symbols, and dreams.

This layered structure allows the narrative to expand without collapsing into shapeless accumulation.

## What Is a Story Arc

A story arc is a collection of scenes that belong to the same narrative zone, function, or thematic cluster.

Some arcs are organized around:

- a physical place
- a local social role
- a recurring mystery
- a dream threshold
- a transitional route

An arc does not need to be large to matter.

An arc only needs to gather related scenes into a structure that is readable, expandable, and playable.

## Current Early Arc Structure

The current early Interactive Novel includes several grounded arcs and a small dream layer.

### Grounded Arcs

```text
0000_start              arrival, docks, captain routes
0100_harbor             harbor village and market exploration
0200_library            library investigation and Visionary documents
0300_forest             forest path, old stones, and stone circle
0400_brinehook          domestic island life and family rhythm
0500_lantern_key        beacon duty, weather watch, and public infrastructure
0600_saint_elmos_rest   refuge, sailor custom, and coastal folklore
```

### Dream / Threshold Arcs

```text
9000_waypoint           waypoint dream scenes
9200_milestone          milestone dream scenes
```

These arcs already show that the world is growing through a mixture of:

- grounded island expansion
- recurring symbol logic
- dream thresholds
- practical archipelago life

## Scene Ranges

Story arcs are organized using scene identifier ranges.

Each arc typically occupies a block of one hundred scene identifiers.

Example:

```text
0000–0099   arrival / dockside / captain access
0100–0199   harbor village
0200–0299   library
0300–0399   forest
0400–0499   Brinehook Island
0500–0599   Lantern Key
0600–0699   Saint Elmo’s Rest
9000–9099   waypoint dream layer
9200–9299   milestone dream layer
```

This structure allows each arc to grow without requiring widespread scene renumbering.

It also makes it easier to reason about the world in clear expandable blocks.

## Folder Organization

Story arcs correspond directly to folders inside the scenes directory.

Example structure:

```text
games/kaleidoscope/story/scenes/

0000_start/
0100_harbor/
0200_library/
0300_forest/
0400_brinehook/
0500_lantern_key/
0600_saint_elmos_rest/
9000_waypoint/
9200_milestone/
```

Each folder contains scenes belonging to a specific arc.

This keeps the scene tree readable while allowing the world to expand arc by arc.

## Relationship to the Scene Graph

The scene graph connects scenes across arcs through player choices.

For example, the player may move from:

```text
arrival scene
    ↓
harbor scene
    ↓
captain scene
    ↓
outer island scene
    ↓
dream scene
```

This means story arcs and scene graph are related but not identical.

- Story arcs organize scenes into readable clusters.
- The scene graph defines how the player actually moves between them.

The graph may cross arc boundaries often. That is expected.

## Current Arc Pattern

At the current stage, arcs are beginning to perform different world functions.

For example:

- Harbor Island introduces the opening mystery and first social world
- Brinehook introduces family and domestic interdependence
- Lantern Key introduces public duty and navigational infrastructure
- Saint Elmo’s Rest introduces refuge, caution, and inherited sailor custom
- dream arcs mark thresholds, recurrence, and the deeper pressure beneath the grounded world

This is important because future arcs do not need to repeat the same narrative function.

They can widen the world by adding new kinds of places, pressures, and meanings.

## Expansion of Story Arcs

As the Kaleidoscope world grows, additional arcs may be added.

Future arcs may include:

- additional inhabited islands
- outer crossing routes
- public or civic islands
- ruins or old structures
- stronger symbolic or mythic zones
- larger dream or threshold sequences

New arcs should be added when they improve either:

- playability
- world depth
- narrative clarity
- structural survivability

They should not be added only for the sake of multiplying folders.

## Design Philosophy

Story arcs should remain:

- readable
- expandable
- distinct
- structurally useful

Their purpose is not merely to store scenes.

Their purpose is to help the world grow in a way that remains legible to players, builders, and future automation.

A good arc should make the world feel larger while keeping the current layer of growth coherent.

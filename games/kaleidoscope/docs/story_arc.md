# Kaleidoscope — Story Arcs

This document explains the concept of **story arcs** within the Kaleidoscope Interactive Novel.

A story arc is a **cluster of related scenes** that together explore a location, narrative thread, or discovery within the world.

Story arcs provide a middle layer of organization between **individual scenes** and the **overall world**.

---

## Structural Layers

The Kaleidoscope narrative structure can be understood as three layers:

```
scene
↓
story arc
↓
world
```

- **Scenes** represent individual moments in the story.
- **Story arcs** group related scenes together.
- **The world** contains many story arcs connected through exploration.

This layered structure allows the narrative to expand while remaining organized.

---

## What Is a Story Arc

A story arc is a **collection of scenes that belong to the same narrative area or theme**.

Examples of early story arcs include:

```
0000_start     starting island introduction
0100_harbor    harbor village exploration
0200_library   library investigation
0300_forest    forest expedition
```

Each arc contains multiple scenes that explore the location or storyline in greater depth.

---

## Scene Ranges

Story arcs are organized using **scene identifier ranges**.

Each arc typically occupies a block of **one hundred scene identifiers**.

Example:

```
0000–0099   starting region
0100–0199   harbor region
0200–0299   library region
0300–0399   forest region
```

This structure allows each arc to grow without requiring scene renumbering.

---

## Folder Organization

Story arcs correspond directly to folders inside the scenes directory.

Example structure:

```
games/kaleidoscope/story/scenes/

0000_start/
    scene_0001.md
    scene_0002.md

0100_harbor/
    scene_0101.md
    scene_0102.md

0200_library/
    scene_0201.md
    scene_0202.md

0300_forest/
    scene_0301.md
    scene_0302.md
```

Each folder contains scenes belonging to a specific arc.

---

## Relationship to the Scene Graph

The **scene graph** connects scenes across arcs through player choices.

Example:

```
scene_0001
   ↓
scene_0101
   ↓
scene_0201
```

This allows the story to move between different arcs as the player explores the world.

Story arcs organize scenes, while the scene graph defines how those scenes connect.

---

## Expansion of Story Arcs

As the Kaleidoscope world grows, additional arcs may be added.

Examples might include:

```
0400_ruins
0500_outer_islands
0600_visionary_mystery
```

Each arc introduces new scenes, characters, and discoveries while remaining compatible with the existing scene structure.

---

## Design Philosophy

Story arcs should remain:

- simple
- readable
- expandable

The purpose of arcs is to keep large collections of scenes organized while allowing the world to grow naturally through exploration and discovery.

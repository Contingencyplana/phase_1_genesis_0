# Kaleidoscope — Scene Graph

This document describes how scenes connect to one another within the Kaleidoscope Interactive Novel.

While individual scene files define narrative moments, the **scene graph** defines how those scenes connect to form a navigable story world.

The scene graph allows the Kaleidoscope world to grow naturally while remaining organized and understandable.

---

## What Is a Scene Graph

A **scene graph** is a network of scenes connected through player choices.

Each scene represents a node in the network.  
Each player choice creates a link from one scene to another.

Example structure:

```
scene_0001
   ↓
 ├─ scene_0002
 ├─ scene_0003
 └─ scene_0004
```

In this example:

- `scene_0001` is the starting scene
- the player can travel to three different scenes
- each of those scenes may branch further

---

### Nodes and Connections

In the Kaleidoscope system:

- **Scenes** act as nodes
- **Choices** act as connections between nodes

Example:

```
Scene: scene_0001
Choice: Visit the library → scene_0003
```

This creates a connection from:

```
scene_0001 → scene_0003
```

These connections form the overall story network.

---

### Graph Integrity Rules

To keep the Kaleidoscope scene network stable as the story grows, the following basic rules should be followed.

### No Broken Links

Every scene reference must point to a valid scene identifier.

Example:

```
- Visit the library → scene_0003
```

The referenced scene file must exist.

---

### All Scenes Must Be Reachable

Every scene should be reachable from the starting scene (`scene_0001`) through one or more choices.

Scenes that cannot be reached from the starting scene are considered **orphan scenes** and should normally be avoided.

---

### Avoid Unintentional Dead Ends

Most scenes should provide at least one choice leading to another scene.

Dead ends may be used intentionally for special narrative moments, but they should be rare.

---

### Stable Connections

Scene links should remain stable once published.

Changing scene identifiers or removing heavily referenced scenes can break the story graph.

---

### Gradual Expansion

The scene graph should grow gradually.

Writers should add small clusters of connected scenes rather than large isolated branches.

---

### Early Scene Network

The first scenes of the Kaleidoscope story should remain very small.

Example early structure:

```
scene_0001  Arrival at Harbor
     ↓
 ├─ scene_0002  Harbor Village
 ├─ scene_0003  Library Entrance
 └─ scene_0004  Forest Path
```

Each of these scenes may then branch into additional discoveries.

---

### Branching and Exploration

Branching allows players to explore the world in different ways.

Good scene graphs encourage exploration by offering multiple directions.

Example:

```
scene_0002 Harbor Village
   ↓
 ├─ scene_0005 Talk to sailor
 ├─ scene_0006 Visit market
 └─ scene_0007 Walk along docks
```

Branching structures help the world feel alive and open.

---

### Story Threads

Scenes may belong to larger narrative threads.

Examples of early threads:

```
The Visionary Mystery
The Library Secrets
The Forest Expedition
```

A single scene may contribute to one or more threads.

Over time, these threads may intersect and reveal larger parts of the story.

---

### Expanding the Scene Graph

As the story grows, the scene graph will naturally expand.

New scenes may introduce:

- new characters
- new locations
- new discoveries
- new story threads

The graph may grow from a handful of scenes to hundreds or thousands.

The scene format defined in `scene_format.md` ensures that this growth remains manageable.

---

### Design Guidelines

When expanding the scene graph, follow these principles.

### Keep Early Networks Small

Begin with a very small number of scenes and expand gradually.

### Encourage Exploration

Scenes should offer multiple meaningful directions when possible.

### Avoid Dead Ends

Most scenes should lead to at least one new scene.

### Reveal the World Gradually

Players should discover new parts of the world through exploration rather than exposition.

---

### Long-Term Growth

The Kaleidoscope scene graph should support gradual expansion of the world.

Over time the graph may connect:

```
islands
archipelagos
distant regions
new characters
new mysteries
```

Despite this growth, the core principle remains simple:

```
scene
↓
choice
↓
next scene
```

This simple structure allows the Kaleidoscope world to grow naturally without requiring major changes to the underlying system.

---

### Design Philosophy

The scene graph should remain:

- simple
- readable
- expandable

The goal is to support a living story world where new paths, discoveries, and narratives can be added indefinitely.

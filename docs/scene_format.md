# Kaleidoscope — Scene Format

This document defines the standard format used for scene files in the Kaleidoscope Interactive Novel.

Scenes are stored as Markdown files in:

```
games/kaleidoscope/story/scenes/
```

Each scene file represents a single moment in the story and provides the text and choices that allow players to navigate the world.

The purpose of this document is to ensure that all scenes follow a **consistent structure** that can be easily written by humans and later parsed by the Kaleidoscope engine.

---

## Scene File Naming

Each scene must be stored in a file named using the following pattern:

```
scene_0001.md
scene_0002.md
scene_0003.md
```

Rules:

- Scene identifiers must be **unique**.
- Scene identifiers should increase sequentially.
- Scene identifiers are used by the engine to resolve player choices.

---

### Scene Structure

Every scene file follows the same basic structure:

```
# Scene: scene_0001

## Title
Scene title

## Location
Location name

---

## Scene Text

Narrative description of the scene.

---

## Choices

- Choice description → scene_target
- Choice description → scene_target
```

Each section is described below.

---

### Scene Header

The first line identifies the scene.

Example:

```
# Scene: scene_0001
```

This identifier must match the filename.

Example:

```
scene_0001.md
```

---

### Title

The title gives the scene a human-readable name.

Example:

```
## Title
Arrival at Harbor Island
```

Titles help writers and designers navigate the story structure.

---

### Location

The location identifies where the scene takes place.

Example:

```
## Location
Harbor Village
```

Locations help organize the world and may later be used by the engine for navigation systems or maps.

---

### Scene Text

The scene text contains the narrative description presented to the player.

Example:

```
## Scene Text

Your ship arrives at Harbor Island just after dawn.
The harbor is already awake with sailors and merchants moving along the docks.
```

Guidelines:

- Keep scenes relatively short.
- Focus on atmosphere and discovery.
- Avoid long exposition.

Scenes should encourage the player to explore the world.

---

### Choices

The choices section defines the actions available to the player.

Example:

```
## Choices

- Walk through the harbor village → scene_0002
- Visit the library on the hill → scene_0003
- Follow the forest path → scene_0004
```

Rules:

- Each choice must link to another scene.
- Use the arrow symbol `→` to indicate the target scene.
- Target scenes must reference valid scene identifiers.

Choices represent meaningful actions such as:

- exploring a location
- speaking with a character
- investigating something unusual
- traveling to another place

---

### Design Guidelines

Scenes should follow several simple design principles.

### Simplicity

Scenes should remain easy to read and write.

### Exploration

Scenes should encourage players to explore different paths.

### Atmosphere

Scene text should help establish the tone of the world.

### Expansion

The scene format should remain stable even as the story grows to include hundreds or thousands of scenes.

---

### Minimal Example

```
# Scene: scene_0001

## Title
Arrival at Harbor Island

## Location
Harbor Village

---

## Scene Text

Your ship arrives at Harbor Island just after dawn.  
The harbor is already busy with sailors unloading cargo and merchants shouting across the docks.

---

## Choices

- Walk through the harbor village → scene_0002
- Visit the library on the hill → scene_0003
- Follow the forest path → scene_0004
```

---

### Design Philosophy

The scene format should remain:

- simple
- readable
- stable

The goal is to allow Kaleidoscope stories to grow naturally over time without requiring major structural changes to the scene system.

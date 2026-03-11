# Kaleidoscope — Scene ID Specification

This document defines the rules governing **scene identifiers** used in the Kaleidoscope Interactive Novel.

Scene identifiers act as the **permanent addresses** of scenes within the story graph.  
They allow scenes to link to one another and allow the Kaleidoscope engine to load and navigate scenes reliably.

Establishing clear rules early prevents structural problems as the story grows to include many scenes.

---

## Purpose of Scene IDs

Scene IDs serve several important functions:

- uniquely identify each scene
- allow scenes to link to other scenes
- allow the engine to load scene files
- allow external tools to analyze the scene graph

Because of this, scene IDs must remain **stable and predictable**.

---

### Scene ID Format

All scene identifiers must follow this format:

```
scene_0001
scene_0002
scene_0003
```

Structure:

```
scene_####
```

Where:

- `scene_` is the fixed prefix
- `####` is a four-digit numeric identifier

Examples:

```
scene_0001
scene_0002
scene_0100
scene_1250
```

Four digits allow the system to support **up to 9,999 scenes** without changing the format.

---

### Scene File Naming

Each scene must be stored in a file named using its scene identifier.

Example:

```
scene_0001.md
scene_0002.md
scene_0003.md
```

The scene identifier inside the file must match the filename.

Example:

```
# Scene: scene_0001
```

File:

```
scene_0001.md
```

---

### Scene ID Rules

The following rules must always be followed.

### Scene IDs are Unique

No two scenes may share the same scene identifier.

---

### Scene IDs Are Permanent

Once assigned, a scene ID should **never be changed**.

Changing scene IDs would break links from other scenes.

---

### Scene IDs Are Never Reused

If a scene is removed from the project, its ID should **not be reused** for a new scene.

This prevents confusion in version history and external references.

---

### Scene IDs Must Match Filenames

The identifier declared inside the file must match the filename.

Example:

```
# Scene: scene_0001
```

File name:

```
scene_0001.md
```

---

### Scene Linking

Scenes connect to one another using scene IDs.

Example:

```
- Visit the library → scene_0003
```

This creates a link from the current scene to the target scene.

The target scene must exist as a valid scene file.

---

### Starting Scene

By convention, the Kaleidoscope story begins with:

```
scene_0001
```

This scene acts as the **default entry point** into the story world unless the engine specifies a different starting scene.

---

### Future Expansion

The current system assumes a single namespace for scene identifiers.

Future expansions of Kaleidoscope may introduce:

- additional story modules
- separate narrative worlds
- parallel story systems

If that occurs, scene ID namespaces may be extended while maintaining compatibility with the existing format.

---

### Design Philosophy

Scene identifiers should remain:

- simple
- stable
- predictable

The goal is to ensure that Kaleidoscope scenes can expand to **hundreds or thousands of nodes** without requiring structural changes to the scene system.

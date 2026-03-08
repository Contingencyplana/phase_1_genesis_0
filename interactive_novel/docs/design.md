# Kaleidoscope — Interactive Fiction Design

This document defines how the Kaleidoscope Interactive Novel works from a player interaction perspective.

It focuses on **how players experience and navigate the story**, not on world lore or narrative details.  
The goal is to establish a simple structure that allows the story to grow organically over time.

---

# Purpose of the Interactive Novel

The Interactive Novel is the **first stage of the Kaleidoscope evolutionary path**.

Its purpose is to create a shared narrative environment where players:

- explore a growing world
- encounter characters and mysteries
- make choices that guide their journey
- gradually uncover larger story threads

The early focus is **exploration and discovery**, not complex game mechanics.

---

# Core Player Loop

The Interactive Novel is built around a very simple interaction loop:


read scene
↓
choose action
↓
move to next scene


This loop should remain simple and intuitive.

Players should be able to understand the interaction immediately without instructions.

Future versions may expand this loop to include additional elements such as discoveries or branching narrative paths.

Example expanded loop:


read scene
↓
choose action
↓
discover clue
↓
branch story


However, the first version should remain minimal.

---

# Scene Structure

Each scene represents a small moment within the world.

Scenes should contain three basic components:


scene text
↓
choices
↓
links to next scenes


Example conceptual structure:


Scene
Text
Choices
choice A → next scene
choice B → next scene


Scenes should be short and focused.  
They should present a situation and allow the player to decide what happens next.

---

# Choices

Choices allow players to influence the direction of the story.

Each scene should normally offer **two to four choices**.

Choices should represent meaningful actions such as:

- speaking with a character
- exploring a location
- investigating a clue
- traveling to another place

Choices should feel natural within the story rather than mechanical.

---

# Story Threads

Story threads are ongoing narrative paths that run through multiple scenes.

Examples of early threads might include:


The Visionary Mystery
The Library Secrets
The Forest Expedition


Scenes can belong to one or more threads.

As players explore the world, different threads gradually intersect and reveal larger parts of the story.

---

# Player Exploration

Players should feel that they are **exploring a living world** rather than following a single fixed path.

To support this feeling:

- scenes should branch into multiple directions
- different characters should provide different information
- locations should lead to new discoveries
- story threads should intersect over time

Exploration should reward curiosity.

Players should often encounter clues or mysteries that encourage them to continue exploring.

---

# Growth of the World

The Kaleidoscope world should expand gradually.

Early stages begin with a small set of scenes and locations.

Over time the story may grow to include:

- new characters
- new regions of the world
- additional story threads
- larger narrative arcs

The goal is to allow the world to evolve naturally as more content is added.

---

# Design Principles

The Interactive Novel should follow several guiding principles.

### Simplicity

The system should remain simple and intuitive.  
Players should be able to start exploring immediately.

### Discovery

Players should uncover the world gradually through exploration rather than receiving long explanations.

### Curiosity

Scenes should encourage players to ask questions and seek answers within the story.

### Expansion

The structure should allow the story to grow without needing major redesigns.

---

# Initial Scope

The first playable version of the Interactive Novel should remain extremely small.

Initial targets:

- one world region
- three characters
- ten scenes

This small starting point provides a narrative seed that can expand over time.

Once the core structure works, new scenes, threads, and locations can be added gradually.

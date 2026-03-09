# Kaleidoscope - Architecture

This document describes the core architectural structure of the Kaleidoscope ecosystem.

Kaleidoscope is designed as a small experimental platform for building, publishing, and playing games. The architecture separates three fundamental roles:

- creation
- publishing
- playing

These roles are implemented by three systems.

---

## Core Systems

### Kaleidoscope

Kaleidoscope is the core creation system.

It functions as both:

- a **game maker**
- a **game room maker**

Kaleidoscope can create:

- games
- game rooms
- tools
- experimental systems

The goal of Kaleidoscope is to allow developers and participants to construct playable spaces and mechanics.

---

### Alpha Dreaming

Alpha Dreaming is the publishing bridge.

It allows developers to package and upload games created in Kaleidoscope.

Responsibilities include:

- uploading games
- packaging builds
- managing game metadata
- publishing games to Alpha TestBed

Alpha Dreaming is primarily a **developer tool**.

---

### Alpha TestBed

Alpha TestBed is the play environment.

It functions as:

- a game room
- a library of experimental games
- a playtesting space

Players can browse available games and launch them instantly.

Alpha TestBed intentionally remains simple to avoid unnecessary complexity.

Its purpose is to enable:

- quick experimentation
- easy playtesting
- rapid feedback loops

---

## System Relationships

The three systems interact as follows:

Kaleidoscope builds both Alpha Dreaming and Alpha TestBed.

Alpha Dreaming is used to publish games.

Alpha TestBed hosts and launches those games.

Conceptually:

```text
Kaleidoscope
builds
↓
Alpha Dreaming (publishing tool)
↓
publishes to
↓
Alpha TestBed (game room)
↓
hosts
↓
Games created with Kaleidoscope
```

---

## Bootstrapping Phase (Initial Workflow)

During the early phase of the project, Kaleidoscope is used to construct the initial infrastructure.

```text
Kaleidoscope
↓ builds
Alpha TestBed
and
Alpha Dreaming
↓ publishes to
Alpha TestBed
↓ hosts
Initial Kaleidoscope games
```

The first games appearing in Alpha TestBed may include:

- Kaleidoscope
- Alpha Dreaming
- Trichess
- Tricheckers
- early experimental prototypes

---

## Mature Workflow

Once the ecosystem is established, the normal development loop emerges.

```text
Developer creates game in Kaleidoscope
↓
Uploads game via Alpha Dreaming
↓
Game appears in Alpha TestBed
↓
Players play and test the game
```

This loop allows continuous experimentation and improvement.

---

## Architectural Principles

The architecture follows several key principles.

### Separation of Roles

Creation, publishing, and playing are handled by separate systems.

This keeps the ecosystem modular and easier to evolve.

---

### Simplicity of the Test Environment

Alpha TestBed should remain extremely simple.

It functions as a game room or experimental arcade rather than a complex platform.

Complexity belongs in Kaleidoscope, not in the TestBed.

---

### Self-Improving Ecosystem

The ecosystem is designed to improve itself over time.

New tools and games created in Kaleidoscope can be published through Alpha Dreaming and tested in Alpha TestBed.

This allows the platform to gradually evolve.

---

## Summary

The Kaleidoscope architecture separates the ecosystem into three systems:

- Kaleidoscope - creation
- Alpha Dreaming - publishing
- Alpha TestBed - playing

This structure supports rapid experimentation while allowing the system to grow into a larger creative ecosystem.

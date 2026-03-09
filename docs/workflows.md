# Kaleidoscope — Workflows

This document describes the operational workflows of the Kaleidoscope ecosystem.

Kaleidoscope supports two primary workflows:

1. **Initial Workflow (Bootstrapping Phase)**
2. **Mature Workflow (Normal Operation)**

The Initial Workflow describes how the first infrastructure is created.
The Mature Workflow describes how developers and players interact with the system once it is established.

---

# Initial Workflow (Bootstrapping Phase)

At the beginning of the project, Kaleidoscope is used to construct the core systems of the ecosystem.

Kaleidoscope functions as both:

- a **game maker**
- a **game room maker**

Using these capabilities, Kaleidoscope builds the first two systems:

- **Alpha TestBed**
- **Alpha Dreaming**

Conceptually:

```text
Kaleidoscope
    ↓ builds
Alpha TestBed (game room / library)
```

```text
Kaleidoscope
    ↓ builds
Alpha Dreaming (upload / publishing tool)
```

Once Alpha Dreaming exists, it can be used to publish games to Alpha TestBed.

```text
Kaleidoscope
    ↓ creates games
Alpha Dreaming
    ↓ publishes
Alpha TestBed
    ↓ hosts
Initial Kaleidoscope games
```

The first games hosted in Alpha TestBed may include:

- Kaleidoscope
- Alpha Dreaming
- Trichess
- Tricheckers
- early experimental prototypes

The goal of the Initial Workflow is to establish the infrastructure required for ongoing experimentation.

# Mature Workflow (Normal Operation)

Once the ecosystem is established, developers and players interact with the system through a stable development loop.

```text
Developer creates game in Kaleidoscope
    ↓
Uploads game via Alpha Dreaming
    ↓
Game appears in Alpha TestBed
    ↓
Players play and test the game
```

This loop enables:

- rapid experimentation
- easy playtesting
- continuous improvement

Developers iterate on their games in Kaleidoscope and publish updates through Alpha Dreaming.

Players provide feedback through gameplay in Alpha TestBed.

# Developer Workflow

The developer workflow focuses on creating and improving games.

Typical steps include:

1. Create or modify a game using Kaleidoscope.
2. Package the game using Alpha Dreaming.
3. Upload the game to Alpha TestBed.
4. Observe player feedback and playtesting results.
5. Improve the game and repeat the process.

# Player Workflow

Players interact with the ecosystem through Alpha TestBed.

Typical steps include:

1. Enter Alpha TestBed.
2. Browse available Alpha games.
3. Select a game to play.
4. Play and explore the game.
5. Return to Alpha TestBed to try other games.

Alpha TestBed should remain simple so that players can quickly launch experimental games without unnecessary friction.

# Continuous Evolution

As the ecosystem grows, the workflow becomes self-reinforcing.

```text
Developers create games
    ↓
Players test games
    ↓
Feedback improves games
    ↓
Improved tools enhance Kaleidoscope
```

This cycle supports the long-term evolution of the platform.

# Summary

The Kaleidoscope ecosystem operates through two workflows:

## Initial Workflow

Kaleidoscope builds Alpha TestBed and Alpha Dreaming.

Alpha Dreaming publishes initial games to Alpha TestBed.

## Mature Workflow

Developers create games in Kaleidoscope.

Games are uploaded through Alpha Dreaming.

Players test games in Alpha TestBed.

Together these workflows enable an evolving ecosystem of experimental games.

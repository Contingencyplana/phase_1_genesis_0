# Flagship Arcade Game — Core Mechanical Primitives

Source: 0003_flagship (Junk Arcade Skeleton)

This document extracts reusable gameplay primitives from the Flagship prototype.

These primitives may later be reused in:
- other arcade games
- card games
- debugging tools
- contractor/polisher tool games
- Creative Assembly Line simulations

---

# 1. Spatial Arena

A bounded 2D combat space.

Properties:
- fixed rectangular arena
- no wraparound
- entities clamped to arena bounds

Primitive functions:

clamp(value, min, max)

distance(pointA, pointB)

normalize(dx, dy)

---

# 2. Entity Core Model

All ships share a base structure.

Core attributes:

position (x, y)
radius
color
hp
max_hp

movement_speed

fire_range
fire_cooldown
fire_timer

damage

attack_range

pulse_visual_effect

Core methods:

alive()

take_damage(amount)

update_fire_timer(dt)

can_fire()

reset_fire()

move_toward(target_x, target_y, dt)

draw()

---

# 3. Ship Types

## Flagship

Purpose:
Central defensive objective.

Properties:

high health
no attack capability
slow movement
acts as enemy target anchor

Failure condition:

flagship_hp == 0 → defeat

---

## Ally Ships

Purpose:
Player-controlled combat units.

Properties:

moderate speed
moderate fire range
moderate damage

State Machine:

FOLLOW
TARGET

Behaviour:

FOLLOW
    maintain position near flagship
    separation behaviour from nearby allies

TARGET
    pursue assigned enemy
    attack when in range
    revert to FOLLOW if target destroyed

Player interaction:

select ally
assign enemy target

---

## Enemy Ships

Purpose:
Pressure generators.

Properties:

spawn at arena edges
slow movement
low damage
moderate fire cooldown

Behaviour:

move toward flagship
attack when in range

---

# 4. Target Assignment Mechanic

Player attention mechanic.

Interaction loop:

click ally
↓
ally selected
↓
click enemy
↓
ally assigned target
↓
ally enters TARGET state

This tests:

attention allocation
command clarity under pressure

---

# 5. Combat Model

Combat is cooldown based.

Rules:

if distance <= fire_range
and fire_timer == 0
then attack

Attack result:

target_hp -= damage

Projectile model:

none

Damage type:

instant

Visual feedback:

pulse halo effect

---

# 6. Movement Model

Movement is deterministic.

Characteristics:

no inertia
constant velocity
direct vector movement toward target

Movement function:

move_toward(target_position)

---

# 7. Separation Behaviour

Allies avoid stacking.

Mechanism:

detect nearby allies within separation radius
compute push vector
offset target position

Purpose:

visual clarity
formation spread

---

# 8. Enemy Spawning

Enemies spawn at arena edges.

Edge selection:

top
bottom
left
right

Wave generator:

spawn_wave(n)

Guarantee:

first enemies distributed across edges

Purpose:

prevent spawn clustering

---

# 9. Game Loop Structure

Frame update order:

input
↓
update allies
↓
update enemies
↓
remove dead enemies
↓
check win/lose condition
↓
render

---

# 10. Victory / Defeat Conditions

Victory:

all enemies destroyed

Defeat:

flagship destroyed

---

# 11. HUD Primitives

Status Panel:

flagship health
enemy count
kill count

Message system:

temporary player prompts

End screen overlay:

victory / defeat messaging

---

# 12. Player Input Model

Mouse:

select ally
assign enemy target

Keyboard:

R = restart
ESC = quit

---

# 13. Attention Pressure Mechanic

Core gameplay test:

continuous battlefield
multiple friendly units
player must allocate attention

Key loop:

observe battlefield
↓
select ally
↓
assign enemy
↓
monitor damage
↓
reassign if needed

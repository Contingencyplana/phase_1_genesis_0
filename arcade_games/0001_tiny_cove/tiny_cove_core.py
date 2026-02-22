# tiny_cove_core.py
# Allocation engine for Tiny Cove (Phase 1 — Ignition Triangle II)

import random

CHILDREN_COUNT = 8
CHILD_WEIGHT = 1
MAX_WEIGHT = 12

CARGO_CATALOG = [
    {"key": "Food", "weight": 1},
    {"key": "Water", "weight": 1},
    {"key": "Repair Kit", "weight": 1},
    {"key": "Medicine", "weight": 1},
    {"key": "Blanket", "weight": 1},
    {"key": "Ballast", "weight": 1},
    {"key": "Extra Sail", "weight": 1},
]


# -------------------------
# Manifest Generation
# -------------------------

def make_required_set():
    core = ["Food", "Water", "Repair Kit", "Medicine"]
    return random.sample(core, 3)


def make_supply_keys(required_keys):
    extras_pool = [c["key"] for c in CARGO_CATALOG if c["key"] not in required_keys]
    extras = random.sample(extras_pool, k=3)
    supply = required_keys + extras
    random.shuffle(supply)
    return supply


# -------------------------
# Weight Logic
# -------------------------

def cargo_weight(key):
    for c in CARGO_CATALOG:
        if c["key"] == key:
            return c["weight"]
    return 1


def children_weight():
    return CHILDREN_COUNT * CHILD_WEIGHT


def current_cargo_weight(loaded):
    return sum(cargo_weight(k) for k in loaded)


def total_weight(loaded):
    return children_weight() + current_cargo_weight(loaded)


def remaining_capacity(loaded):
    return MAX_WEIGHT - total_weight(loaded)


def has_required_loaded(loaded, required):
    loaded_set = set(loaded)
    return all(r in loaded_set for r in required)

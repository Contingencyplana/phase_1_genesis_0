
# tiny_cove.py
# Tiny Cove — Ignition Triangle II (Split Version, v0.1.1 patch)
#
# Fixes:
# - Timer clamp at 0 (no negative display)
# - No soft-lock: auto-lash after requirements met
# - Clear capacity display (used + remaining)
# - Dock spawn grid (no overflow)
# - Carry HUD fixed location
# - Disable toggling checkboxes for already-loaded items

import pygame
import sys
import time

from tiny_cove_core import *

pygame.init()

WIDTH, HEIGHT = 900, 600
FPS = 60

FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 36)

PLAYER_SIZE = 26
PLAYER_SPEED = 4.2
CARRY_SPEED_MULT = 0.7

COUNTDOWN_SECONDS = 45
DOCK_SECONDS = 1.6
LASH_SECONDS = 1.2

AUTO_LASH_DELAY = 2.0  # seconds after requirements met -> auto depart (prevents soft-lock)

COLOR_BG = (26, 34, 52)
COLOR_WATER = (55, 105, 150)
COLOR_DOCK = (85, 60, 40)
COLOR_PANEL = (20, 22, 28)
COLOR_TEXT = (240, 240, 240)
COLOR_DIM = (160, 160, 160)
COLOR_CHECK = (105, 215, 120)
COLOR_BAD = (230, 90, 90)

STATE_DOCKING = "docking"
STATE_ALLOCATION = "allocation"
STATE_LASHING = "lashing"
STATE_DEPART = "depart"
STATE_END = "end"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Cove")
clock = pygame.time.Clock()

boat_zone = pygame.Rect(0, 0, WIDTH, 95)
dock_rect = pygame.Rect(80, 230, 320, 260)
panel_rect = pygame.Rect(0, 0, 260, HEIGHT)


def draw_boat(x, y, children, loaded):
    # Simple hull
    pygame.draw.rect(screen, (120, 70, 30), (x, y, 280, 34))

    # Children (fixed)
    for i in range(children):
        pygame.draw.circle(screen, (255, 220, 180), (x + 250 - i * 18, y - 6), 6)

    # Cargo stack (simple)
    for i, _key in enumerate(loaded):
        pygame.draw.rect(screen, (195, 170, 110), (x + 20 + i * 22, y - 6, 18, 12))


def dock_spawn_slots():
    """
    Precompute a grid of spawn slots inside dock_rect.
    Ensures we never spawn outside the dock.
    """
    slots = []
    left = dock_rect.x + 20
    top = dock_rect.y + 80
    cell_w = 52
    cell_h = 48
    cols = max(1, (dock_rect.w - 40) // cell_w)
    rows = max(1, (dock_rect.h - 120) // cell_h)
    for r in range(rows):
        for c in range(cols):
            x = left + c * cell_w
            y = top + r * cell_h
            slots.append(pygame.Rect(x, y, 46, 36))
    return slots


def reset():
    required = make_required_set()
    supply = make_supply_keys(required)

    return {
        "state": STATE_DOCKING,
        "boat_x": -300,
        "boat_target_x": 300,
        "boat_y": 54,

        "player": pygame.Rect(120, 420, PLAYER_SIZE, PLAYER_SIZE),
        "carrying": None,

        "required": required,
        "supply": supply,
        "clipboard": {k: False for k in supply},  # ticked -> spawn on dock
        "dock_items": {},  # key -> rect
        "loaded": [],

        "countdown_start": None,
        "state_time": time.time(),

        "requirements_met_at": None,  # when reqs first became true (for auto-lash)

        "won": False,
        "failed": False,
    }


game = reset()
SLOTS = dock_spawn_slots()


def spawn_from_clipboard():
    """
    Ensure every checked (and not loaded) item exists on the dock,
    and unchecked items are removed from dock.

    Uses fixed grid slots so items never overflow dock bounds.
    """
    # Remove dock items that were unchecked
    for key in list(game["dock_items"].keys()):
        if not game["clipboard"].get(key, False):
            del game["dock_items"][key]

    # Determine which keys need to spawn
    want = [k for k, checked in game["clipboard"].items() if checked and k not in game["loaded"]]
    have = set(game["dock_items"].keys())

    # Fill empty slots with missing keys
    empty_slots = [s for s in SLOTS if all(not s.colliderect(r) for r in game["dock_items"].values())]

    for key in want:
        if key in have:
            continue
        if not empty_slots:
            # No space left — refuse to spawn more
            game["clipboard"][key] = False
            continue
        slot = empty_slots.pop(0)
        game["dock_items"][key] = pygame.Rect(slot.x, slot.y, slot.w, slot.h)


def is_checkbox_disabled(key: str) -> bool:
    # Already loaded items cannot be toggled
    return key in game["loaded"]


while True:
    dt = clock.tick(FPS) / 1000.0
    now = time.time()

    # ----------------------------
    # EVENTS
    # ----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if game["state"] == STATE_ALLOCATION and event.key == pygame.K_SPACE:
                if has_required_loaded(game["loaded"], game["required"]):
                    game["state"] = STATE_LASHING
                    game["state_time"] = now

            if game["state"] == STATE_END and event.key == pygame.K_r:
                game = reset()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game["state"] == STATE_ALLOCATION:
                mx, my = event.pos
                y = 200
                for key in game["clipboard"]:
                    box = pygame.Rect(20, y, 18, 18)
                    if box.collidepoint(mx, my) and not is_checkbox_disabled(key):
                        game["clipboard"][key] = not game["clipboard"][key]
                    y += 26
                spawn_from_clipboard()

    # ----------------------------
    # STATE LOGIC
    # ----------------------------
    if game["state"] == STATE_DOCKING:
        t = (now - game["state_time"]) / DOCK_SECONDS
        if t >= 1.0:
            game["state"] = STATE_ALLOCATION
            game["countdown_start"] = now
            game["requirements_met_at"] = None
        else:
            # Boat sails in from left
            game["boat_x"] = -300 + (game["boat_target_x"] + 300) * t

    elif game["state"] == STATE_ALLOCATION:
        # Timer (clamp at 0 to prevent negative display)
        elapsed = now - game["countdown_start"]
        remaining = max(0.0, COUNTDOWN_SECONDS - elapsed)

        # If requirements met, start/maintain a met timestamp for auto-lash
        if has_required_loaded(game["loaded"], game["required"]):
            if game["requirements_met_at"] is None:
                game["requirements_met_at"] = now

            # Prevent soft-lock: auto-lash after short delay OR when timer hits 0
            if (now - game["requirements_met_at"]) >= AUTO_LASH_DELAY or remaining <= 0.0:
                game["state"] = STATE_LASHING
                game["state_time"] = now
        else:
            # If timer expires and requirements are NOT met: fail
            if remaining <= 0.0:
                game["failed"] = True
                game["state"] = STATE_END

        # Movement
        keys = pygame.key.get_pressed()
        speed = PLAYER_SPEED * (CARRY_SPEED_MULT if game["carrying"] else 1.0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game["player"].x -= int(speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game["player"].x += int(speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game["player"].y -= int(speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game["player"].y += int(speed)

        game["player"].clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Pick up one dock item
        if not game["carrying"]:
            for key, rect in list(game["dock_items"].items()):
                if game["player"].colliderect(rect):
                    game["carrying"] = key
                    del game["dock_items"][key]
                    break

        # Deliver to boat zone
        if game["carrying"] and game["player"].colliderect(boat_zone):
            key = game["carrying"]
            if remaining_capacity(game["loaded"]) - cargo_weight(key) >= 0:
                game["loaded"].append(key)
                game["carrying"] = None
                # Keep checkbox checked but effectively disabled now
                game["clipboard"][key] = True
            else:
                # Drop it back: re-check it and respawn to an empty slot
                game["carrying"] = None
                game["clipboard"][key] = True
                spawn_from_clipboard()

        # Keep dock synced to clipboard
        spawn_from_clipboard()

    elif game["state"] == STATE_LASHING:
        if now - game["state_time"] >= LASH_SECONDS:
            game["state"] = STATE_DEPART

    elif game["state"] == STATE_DEPART:
        game["boat_x"] += 220 * dt
        if game["boat_x"] > WIDTH + 50:
            game["won"] = True
            game["state"] = STATE_END

    # ----------------------------
    # DRAW
    # ----------------------------
    screen.fill(COLOR_BG)
    pygame.draw.rect(screen, COLOR_WATER, boat_zone)
    pygame.draw.rect(screen, COLOR_DOCK, dock_rect)
    pygame.draw.rect(screen, COLOR_PANEL, panel_rect)

    # Boat
    draw_boat(game["boat_x"], game["boat_y"], CHILDREN_COUNT, game["loaded"])

    # HUD common
    title = FONT.render("Tiny Cove — Port B (Allocation)", True, COLOR_TEXT)
    screen.blit(title, (280, 12))

    # Allocation UI
    if game["state"] in (STATE_ALLOCATION, STATE_LASHING, STATE_DEPART, STATE_END):
        # Timer / capacity display
        if game["countdown_start"] is not None:
            elapsed = now - game["countdown_start"]
            remaining = max(0.0, COUNTDOWN_SECONDS - elapsed)
        else:
            remaining = COUNTDOWN_SECONDS

        used = total_weight(game["loaded"])
        rem = remaining_capacity(game["loaded"])

        screen.blit(FONT.render(f"Time: {remaining:0.1f}s", True, COLOR_TEXT), (20, 520))
        screen.blit(FONT.render(f"Load: {used}/{MAX_WEIGHT}  (Remaining: {rem})", True, COLOR_TEXT), (20, 545))

        # Required list
        screen.blit(FONT.render("Required to Depart:", True, COLOR_TEXT), (14, 84))
        ry = 110
        for r in game["required"]:
            loaded = (r in game["loaded"])
            mark = "✓" if loaded else "☐"
            col = COLOR_CHECK if loaded else COLOR_TEXT
            screen.blit(FONT.render(f"{mark} {r}", True, col), (18, ry))
            ry += 22

        # Clipboard list
        screen.blit(FONT.render("Available Supplies:", True, COLOR_TEXT), (14, 200))
        y = 226
        for key in game["clipboard"]:
            pygame.draw.rect(screen, (40, 40, 50), (20, y, 18, 18))
            if game["clipboard"][key]:
                pygame.draw.line(screen, COLOR_CHECK, (22, y + 9), (28, y + 15), 3)
                pygame.draw.line(screen, COLOR_CHECK, (28, y + 15), (36, y + 5), 3)

            label_col = COLOR_DIM if is_checkbox_disabled(key) else COLOR_TEXT
            label = key + (" (LOADED)" if is_checkbox_disabled(key) else "")
            screen.blit(FONT.render(label, True, label_col), (45, y))
            y += 26

        # Dock items
        for _key, rect in game["dock_items"].items():
            pygame.draw.rect(screen, (195, 170, 110), rect)
            pygame.draw.rect(screen, (120, 100, 60), rect, 2)

        # Player
        if game["state"] == STATE_ALLOCATION:
            pygame.draw.rect(screen, (200, 200, 200), game["player"])

            # Carry status (fixed HUD)
            carry_text = f"Carrying: {game['carrying']}" if game["carrying"] else "Carrying: (nothing)"
            screen.blit(FONT.render(carry_text, True, COLOR_TEXT), (280, 42))

            # Depart prompt
            if has_required_loaded(game["loaded"], game["required"]):
                # Show whether it's auto-lashing soon
                if game["requirements_met_at"] is not None:
                    auto_in = max(0.0, AUTO_LASH_DELAY - (now - game["requirements_met_at"]))
                else:
                    auto_in = AUTO_LASH_DELAY
                screen.blit(FONT.render(f"Requirements met! Auto-depart in {auto_in:0.1f}s (or press SPACE).",
                                        True, COLOR_CHECK), (280, 66))
            else:
                screen.blit(FONT.render("Load all REQUIRED items to depart.", True, COLOR_DIM), (280, 66))

    # Docking / lashing / depart feedback
    if game["state"] == STATE_DOCKING:
        msg = FONT.render("Arriving at Port B...", True, COLOR_TEXT)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 140))

    if game["state"] == STATE_LASHING:
        msg = FONT.render("Lashing cargo...", True, COLOR_TEXT)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 140))

    if game["state"] == STATE_DEPART:
        msg = FONT.render("Departing...", True, COLOR_TEXT)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 140))

    # End overlay
    if game["state"] == STATE_END:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        msg = "All Secured! Departure!" if game["won"] else "Too Late — Manifest Incomplete"
        screen.blit(BIG_FONT.render(msg, True, COLOR_TEXT), (WIDTH // 2 - 260, HEIGHT // 2 - 60))
        screen.blit(FONT.render("Press R to Restart", True, COLOR_TEXT), (WIDTH // 2 - 100, HEIGHT // 2))

        req_line = FONT.render(f"Required: {', '.join(game['required'])}", True, COLOR_DIM)
        load_line = FONT.render(f"Loaded: {', '.join(game['loaded']) if game['loaded'] else '(none)'}", True, COLOR_DIM)
        screen.blit(req_line, (WIDTH // 2 - req_line.get_width() // 2, HEIGHT // 2 + 40))
        screen.blit(load_line, (WIDTH // 2 - load_line.get_width() // 2, HEIGHT // 2 + 64))

    pygame.display.flip()
    
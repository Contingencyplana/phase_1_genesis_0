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
import pygame.mixer
import sys
import os
import time
import subprocess

# Add parent directory to path for shared modules

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harbor_geometry import HULL_CLEARANCE, HARBOR_STRIP_HEIGHT, docked_boat_y
from harbor_art import draw_docked_boat_with_children

from tiny_cove_core import *

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

# Generate pickup sound if it doesn't exist
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "assets", "audio")
PICKUP_SOUND_PATH = os.path.join(AUDIO_DIR, "sfx_spell_pickup.wav")
LOAD_SOUND_PATH = os.path.join(AUDIO_DIR, "sfx_load_soft.wav")

if not os.path.exists(PICKUP_SOUND_PATH):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    script_path = os.path.join(os.path.dirname(__file__), "create_pickup_sound.py")
    try:
        subprocess.run([sys.executable, script_path], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # Continue anyway if sound generation fails

if not os.path.exists(LOAD_SOUND_PATH):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    script_path = os.path.join(os.path.dirname(__file__), "create_load_sound.py")
    try:
        subprocess.run([sys.executable, script_path], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # Continue anyway if sound generation fails

# Load pickup sound effect
sfx_pickup = None
if os.path.exists(PICKUP_SOUND_PATH):
    try:
        sfx_pickup = pygame.mixer.Sound(PICKUP_SOUND_PATH)
    except pygame.error:
        pass  # Continue if sound fails to load

# Load load sound effect
sfx_load = None
if os.path.exists(LOAD_SOUND_PATH):
    try:
        sfx_load = pygame.mixer.Sound(LOAD_SOUND_PATH)
    except pygame.error:
        pass  # Continue if sound fails to load

FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 36)

PLAYER_SIZE = 26
PLAYER_SPEED = 4.2
CARRY_SPEED_MULT = 0.7

COUNTDOWN_SECONDS = 45
DOCK_SECONDS = 1.6
DOCK_PAUSE_SECONDS = 0.1
LASH_SECONDS = 1.2

AUTO_LASH_DELAY = 2.0  # seconds after requirements met -> auto depart (prevents soft-lock)

# Glide scene scale hierarchy
PORT_SIZE = 90
PORT_GAP = PORT_SIZE // 3
GLIDE_BOAT_WIDTH = int(PORT_SIZE * 0.9)
GLIDE_BOAT_HEIGHT = int(PORT_SIZE * 0.5)

BOAT_WIDTH = 240
BOAT_HULL_HEIGHT = 30

COLOR_BG = (26, 34, 52)
COLOR_WATER = (55, 105, 150)
COLOR_DOCK = (85, 60, 40)
COLOR_PANEL = (20, 22, 28)
COLOR_TEXT = (240, 240, 240)
COLOR_DIM = (160, 160, 160)
COLOR_CHECK = (105, 215, 120)
COLOR_BAD = (230, 90, 90)

# Cove scene colors
COLOR_BEACH = (210, 180, 140)
COLOR_COAST = (100, 150, 80)
COLOR_OCEAN = (30, 70, 110)
COLOR_PORT_INTACT = (100, 75, 50)
COLOR_PORT_DAMAGED = (70, 40, 30)
COLOR_PORT_CRACK = (180, 60, 60)

STATE_GLIDE = "glide"
STATE_DOCKING = "docking"
STATE_ALLOCATION = "allocation"
STATE_LASHING = "lashing"
STATE_DEPART = "depart"
STATE_END = "end"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Cove")
clock = pygame.time.Clock()

boat_zone = pygame.Rect(0, 0, WIDTH, 80)
dock_rect = pygame.Rect(80, 230, 320, 260)
panel_rect = pygame.Rect(0, 0, 260, HEIGHT)

# HUD positioning anchor: below harbor strip to avoid boat mast/sails
HUD_TOP_Y = boat_zone.bottom + 12


def draw_boat(x, y, children, loaded):
    # Draw boat with children and captain using shared harbor art
    draw_docked_boat_with_children(
        screen, x, y, children,
        show_captain=True,
        boat_width=BOAT_WIDTH,
        boat_height=BOAT_HULL_HEIGHT
    )
    
    # Cargo stack (simple visual indicator below children)
    for i, _key in enumerate(loaded):
        pygame.draw.rect(screen, (195, 170, 110), (x + 20 + i * 22, y + BOAT_HULL_HEIGHT + 2, 18, 12))


def draw_cove_background():
    """
    Draw the curved C-shaped cove establishing shot background using ellipses.
    - Open ocean at top (north entrance)
    - Curved beach forming the C shape
    - Water inside the C
    - Green coast surrounding the cove
    """
    # Fill entire screen with green coast (default terrain)
    screen.fill(COLOR_COAST)
    
    # Cove dimensions - ellipse centered higher, slightly larger
    cove_center_x = 450
    cove_center_y = 260
    beach_outer_width = 750
    beach_outer_height = 450
    water_width = 590
    water_height = 330
    
    # Draw beach as curved C using outer ellipse
    beach_rect = pygame.Rect(
        cove_center_x - beach_outer_width // 2,
        cove_center_y - beach_outer_height // 2,
        beach_outer_width,
        beach_outer_height
    )
    pygame.draw.ellipse(screen, COLOR_BEACH, beach_rect)
    
    # Draw water as curved interior using inner ellipse
    water_rect = pygame.Rect(
        cove_center_x - water_width // 2,
        cove_center_y - water_height // 2,
        water_width,
        water_height
    )
    pygame.draw.ellipse(screen, COLOR_WATER, water_rect)
    
    # Draw open ocean at the north opening (top of screen) LAST
    # so it erases the top of beach and water ellipses to create the C mouth
    pygame.draw.rect(screen, COLOR_OCEAN, (0, 0, WIDTH, 140))


def draw_port(x, y, is_intact):
    """
    Draw a port square.
    is_intact: True for Port B, False for Port A (damaged)
    """
    port_size = PORT_SIZE
    
    if is_intact:
        # Port B: intact, neutral dock color (no border)
        pygame.draw.rect(screen, COLOR_PORT_INTACT, (x, y, port_size, port_size))
    else:
        # Port A: damaged, dark with red undertone
        pygame.draw.rect(screen, COLOR_PORT_DAMAGED, (x, y, port_size, port_size))
        pygame.draw.rect(screen, COLOR_PORT_CRACK, (x, y, port_size, port_size), 2)
        
        # Stress blotches (darker areas showing structural damage)
        s = port_size
        blotch_color = (50, 25, 20)
        pygame.draw.rect(screen, blotch_color, (x + int(s*0.12), y + int(s*0.15), int(s*0.18), int(s*0.12)))
        pygame.draw.rect(screen, blotch_color, (x + int(s*0.65), y + int(s*0.35), int(s*0.15), int(s*0.20)))
        pygame.draw.rect(screen, blotch_color, (x + int(s*0.30), y + int(s*0.70), int(s*0.22), int(s*0.14)))
        
        # Distributed crack lines (proportional to port size)
        crack_col = COLOR_PORT_CRACK
        # Diagonal crack from upper-left toward center
        pygame.draw.line(screen, crack_col, (x + int(s*0.08), y + int(s*0.15)), (x + int(s*0.45), y + int(s*0.52)), 1)
        # Diagonal crack from upper-right toward left-center
        pygame.draw.line(screen, crack_col, (x + int(s*0.85), y + int(s*0.10)), (x + int(s*0.38), y + int(s*0.48)), 1)
        # Vertical crack on left side
        pygame.draw.line(screen, crack_col, (x + int(s*0.18), y + int(s*0.25)), (x + int(s*0.22), y + int(s*0.65)), 1)
        # Horizontal crack near middle
        pygame.draw.line(screen, crack_col, (x + int(s*0.25), y + int(s*0.50)), (x + int(s*0.72), y + int(s*0.48)), 1)
        # Diagonal from bottom-left toward right
        pygame.draw.line(screen, crack_col, (x + int(s*0.15), y + int(s*0.78)), (x + int(s*0.68), y + int(s*0.62)), 1)
        # Short crack near bottom-right
        pygame.draw.line(screen, crack_col, (x + int(s*0.72), y + int(s*0.82)), (x + int(s*0.88), y + int(s*0.75)), 1)
        # Cross pattern near center
        pygame.draw.line(screen, crack_col, (x + int(s*0.42), y + int(s*0.38)), (x + int(s*0.58), y + int(s*0.55)), 1)
        # Diagonal on right side
        pygame.draw.line(screen, crack_col, (x + int(s*0.78), y + int(s*0.30)), (x + int(s*0.82), y + int(s*0.58)), 1)


def dock_spawn_slots():
    """
    Precompute a grid of spawn slots inside dock_rect.
    Ensures we never spawn outside the dock.
    """
    slots = []
    left = dock_rect.x + dock_rect.width - 124  # Position on right side of dock_rect
    top = dock_rect.y + 52
    cell_w = 60
    cell_h = 60
    cols = 2
    rows = 3
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
        "state": STATE_GLIDE,
        "boat_x": 0,  # Will be computed in STATE_GLIDE
        "boat_target_x": 0,  # Computed during docking
        "boat_y": 54,

        "glide_duration": 2.5,  # seconds

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
    Spawn new items onto the dock based on clipboard checks.
    
    The dock is an independent staging surface that retains items
    until they are picked up or delivered.
    """
    for index, (key, checked) in enumerate(game["clipboard"].items()):
        if checked and key not in game["dock_items"] and key not in game["loaded"] and key != game["carrying"]:
            slot = SLOTS[index]
            game["dock_items"][key] = pygame.Rect(slot.x, slot.y, slot.w, slot.h)


def is_checkbox_disabled(key: str) -> bool:
    # Already loaded items cannot be toggled
    return key in game["loaded"]


def ready_to_depart():
    ticked_count = sum(1 for v in game["clipboard"].values() if v)
    return has_required_loaded(game["loaded"], game["required"]) and len(game["loaded"]) == ticked_count


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
                if ready_to_depart():
                    game["state"] = STATE_LASHING
                    game["state_time"] = now

            if game["state"] == STATE_END and event.key == pygame.K_r:
                game = reset()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game["state"] == STATE_ALLOCATION:
                mx, my = event.pos
                y = 226
                for key in game["clipboard"]:
                    box = pygame.Rect(20, y, 18, 18)
                    if box.collidepoint(mx, my) and not is_checkbox_disabled(key):
                        game["clipboard"][key] = not game["clipboard"][key]
                    y += 26
                spawn_from_clipboard()

    # ----------------------------
    # STATE LOGIC
    # ----------------------------
    if game["state"] == STATE_GLIDE:
        # Establishing shot: boat glides from Port A to Port B over 2-3 seconds
        elapsed = now - game["state_time"]
        t = min(1.0, elapsed / game["glide_duration"])
        
        # Compute glide positions dynamically based on port centers
        cove_center_x = 450
        total_port_width = PORT_SIZE * 2 + PORT_GAP
        left_port_x = cove_center_x - total_port_width // 2
        right_port_x = left_port_x + PORT_SIZE + PORT_GAP
        
        left_port_center = left_port_x + PORT_SIZE // 2
        right_port_center = right_port_x + PORT_SIZE // 2
        
        glide_start = left_port_center - GLIDE_BOAT_WIDTH // 2
        glide_end = right_port_center - GLIDE_BOAT_WIDTH // 2
        
        # Smooth interpolation from Port A to Port B
        game["boat_x"] = glide_start + (glide_end - glide_start) * t

        cove_center_y = 260
        water_height = 330
        port_y = cove_center_y + water_height // 2 - PORT_SIZE

        hull_height = int(GLIDE_BOAT_HEIGHT * 0.35)
        hull_top_offset = int(GLIDE_BOAT_HEIGHT * 0.5)
        hull_total_height = hull_top_offset + hull_height
        vertical_gap = 6  # small visual clearance
        boat_y = port_y - hull_total_height - vertical_gap

        game["boat_y"] = boat_y
        
        # When glide is complete, transition to docking scene
        if t >= 1.0:
            game["state"] = STATE_DOCKING
            game["state_time"] = now
            game["boat_target_x"] = 0

    elif game["state"] == STATE_DOCKING:
        elapsed = now - game["state_time"]
        boat_width = BOAT_WIDTH
        boat_target_x = WIDTH // 2 - boat_width // 2
        boat_start_x = -boat_width - int(boat_width * 0.1)
        hull_height = BOAT_HULL_HEIGHT
        boat_y = docked_boat_y(boat_zone.bottom)

        if elapsed < DOCK_SECONDS:
            t = elapsed / DOCK_SECONDS
            game["boat_x"] = boat_start_x + (boat_target_x - boat_start_x) * t
            game["boat_y"] = boat_y
        elif elapsed < DOCK_SECONDS + DOCK_PAUSE_SECONDS:
            game["boat_x"] = boat_target_x
            game["boat_y"] = boat_y
        else:
            game["state"] = STATE_ALLOCATION
            game["countdown_start"] = now
            game["requirements_met_at"] = None

    elif game["state"] == STATE_ALLOCATION:
        # Timer (clamp at 0 to prevent negative display)
        elapsed = now - game["countdown_start"]
        remaining = max(0.0, COUNTDOWN_SECONDS - elapsed)

        # If requirements met, start/maintain a met timestamp for auto-lash
        if ready_to_depart():
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
                    game["clipboard"][key] = False
                    # Play pickup sound
                    if sfx_pickup:
                        sfx_pickup.play()
                    break

        # Deliver to boat zone
        if game["carrying"] and game["player"].colliderect(boat_zone):
            key = game["carrying"]
            if remaining_capacity(game["loaded"]) - cargo_weight(key) >= 0:
                game["loaded"].append(key)
                game["carrying"] = None
                # Play load sound on successful delivery
                if sfx_load:
                    sfx_load.play()
                # Keep checkbox checked but effectively disabled now
                game["clipboard"][key] = True
            else:
                # Drop it back: re-check it and respawn to an empty slot
                game["carrying"] = None
                game["clipboard"][key] = True
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
    if game["state"] == STATE_GLIDE:
        # Establishing shot: C-shaped cove with ports
        draw_cove_background()
        
        # Vertical embedding: southern beach arc
        # Water ellipse southern edge: cove_center_y + water_height // 2
        # Port top edge aligns to water boundary, bottom half in beach
        cove_center_y = 260
        water_height = 330
        port_y = cove_center_y + water_height // 2 - PORT_SIZE
        
        # Port positioning calculations
        # Horizontal centering within cove
        cove_center_x = 450
        total_port_width = PORT_SIZE * 2 + PORT_GAP
        left_port_x = cove_center_x - total_port_width // 2
        right_port_x = left_port_x + PORT_SIZE + PORT_GAP
        
        # Port A (left, damaged) and Port B (right, intact)
        draw_port(left_port_x, port_y, is_intact=False)
        draw_port(right_port_x, port_y, is_intact=True)
        
        # Draw stylized sailboat gliding over water
        boat_glide_y = game["boat_y"]
        boat_center_x = game["boat_x"] + GLIDE_BOAT_WIDTH // 2
        
        # Trapezoid hull
        hull_height = int(GLIDE_BOAT_HEIGHT * 0.35)
        hull_y = boat_glide_y + int(GLIDE_BOAT_HEIGHT * 0.5)
        hull_top_width = GLIDE_BOAT_WIDTH
        hull_bottom_width = int(GLIDE_BOAT_WIDTH * 0.7)
        
        hull_points = [
            (boat_center_x - hull_top_width // 2, hull_y),
            (boat_center_x + hull_top_width // 2, hull_y),
            (boat_center_x + hull_bottom_width // 2, hull_y + hull_height),
            (boat_center_x - hull_bottom_width // 2, hull_y + hull_height),
        ]
        pygame.draw.polygon(screen, (120, 70, 30), hull_points)
        
        # Equilateral triangle sail geometry
        side_length = GLIDE_BOAT_WIDTH
        triangle_height = int(side_length * 0.866)  # sqrt(3)/2
        
        mast_top_y = hull_y - triangle_height
        base_y = hull_y
        
        # Triangle vertices
        left_base = (boat_center_x - side_length // 2, base_y)
        right_base = (boat_center_x + side_length // 2, base_y)
        apex = (boat_center_x, mast_top_y)
        
        # Draw left sail (left half of triangle)
        left_sail_points = [apex, left_base, (boat_center_x, base_y)]
        pygame.draw.polygon(screen, (255, 255, 255), left_sail_points)
        
        # Draw right sail (right half of triangle)
        right_sail_points = [apex, (boat_center_x, base_y), right_base]
        pygame.draw.polygon(screen, (255, 255, 255), right_sail_points)
        
        # Draw mast (white, 2 pixels wide)
        pygame.draw.line(screen, (255, 255, 255), apex, (boat_center_x, base_y), 2)
        
        # Title
        title = FONT.render("Tiny Cove — Opening: Cove at Dawn", True, COLOR_TEXT)
        screen.blit(title, (280, 12))
        
    elif game["state"] == STATE_DOCKING:
        # Cinematic arrival: no panel or allocation HUD
        screen.fill(COLOR_BG)
        pygame.draw.rect(screen, COLOR_WATER, boat_zone)
        # Draw dock lip at harbor strip bottom
        pygame.draw.rect(screen, COLOR_DOCK, (0, boat_zone.bottom, WIDTH, 6))
        pygame.draw.rect(screen, COLOR_DOCK, dock_rect)
        draw_boat(game["boat_x"], game["boat_y"], CHILDREN_COUNT, game["loaded"])

    else:
        # Normal allocation scene background
        screen.fill(COLOR_BG)
        pygame.draw.rect(screen, COLOR_WATER, boat_zone)
        # Draw dock lip at harbor strip bottom
        pygame.draw.rect(screen, COLOR_DOCK, (0, boat_zone.bottom, WIDTH, 6))
        pygame.draw.rect(screen, COLOR_DOCK, dock_rect)
        pygame.draw.rect(screen, COLOR_PANEL, panel_rect)

        # Boat
        draw_boat(game["boat_x"], game["boat_y"], CHILDREN_COUNT, game["loaded"])

        # HUD common - title below harbor strip
        title = FONT.render("Tiny Cove — Port B (Allocation)", True, COLOR_TEXT)
        screen.blit(title, (280, HUD_TOP_Y))

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

            # Carry status (fixed HUD) - positioned below harbor strip
            carry_text = f"Carrying: {game['carrying']}" if game["carrying"] else "Carrying: (nothing)"
            screen.blit(FONT.render(carry_text, True, COLOR_TEXT), (280, HUD_TOP_Y + 24))

            # Depart prompt - positioned below carry status
            if ready_to_depart():
                # Show whether it's auto-lashing soon
                if game["requirements_met_at"] is not None:
                    auto_in = max(0.0, AUTO_LASH_DELAY - (now - game["requirements_met_at"]))
                else:
                    auto_in = AUTO_LASH_DELAY
                screen.blit(FONT.render(f"Requirements met! Auto-depart in {auto_in:0.1f}s (or press SPACE).",
                                        True, COLOR_CHECK), (280, HUD_TOP_Y + 48))
            else:
                screen.blit(FONT.render("Load all required items and every checked supply to depart.", True, COLOR_DIM), (280, HUD_TOP_Y + 48))

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
    
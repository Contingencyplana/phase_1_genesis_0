import sys
import random
import pygame

# ============================================================
# 0002 — AT SEA (Craft Table Recursion Chamber)
# Mechanical Probe: Can cooperative inputs assemble a coherent
# rule-card under clarity constraint using bounded token categories?
#
# Mouse-only input.
# Click hands to contribute tokens.
# Build a rule with exactly 4 tokens: STRUCTURE + ACTION + TARGET + CONDITION.
# Micro-constraint: At least one STRUCTURE must appear in the first 2 clicks.
#
# Win: complete 3 valid rules before clarity hits 0.
# Lose: clarity reaches 0.
#
# Controls:
#   Mouse Click: choose a hand (adds a token)
#   Backspace:   undo last token (small clarity cost)
#   C:           clear current assembly (small clarity cost)
#   R:           restart
#   ESC:         quit
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1100, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("0002 — At Sea (Recursion via Craft Table)")
clock = pygame.time.Clock()

# -----------------------------
# Bounded token pools
# -----------------------------
TOKEN_POOLS = {
    "STRUCTURE": ["Each Turn", "When", "If", "Whenever"],
    "ACTION": ["Draw", "Swap", "Block", "Discard"],
    "TARGET": ["One Card", "Opponent", "All Players", "Your Hand"],
    "CONDITION": ["On Hit", "After Loss", "At Start", "On Success"],
}

CATEGORIES = ["STRUCTURE", "ACTION", "TARGET", "CONDITION"]
REQUIRED = set(CATEGORIES)

# -----------------------------
# Tuning knobs (pressure system)
# -----------------------------
MAX_CLARITY = 100.0
CLARITY_DRAIN_PER_SEC = 1.6          # slow decay
CLARITY_COST_PER_CLICK = 2.0         # slight penalty
CLARITY_RESTORE_ON_VALID = 18.0      # moderate restore
CLARITY_PENALTY_ON_INVALID = 22.0    # heavy penalty
MICRO_CONSTRAINT_PENALTY = 10.0      # penalty if no STRUCTURE in first two clicks
UNDO_COST = 2.5
CLEAR_COST = 3.5

WIN_TARGET = 3

# -----------------------------
# Layout
# -----------------------------
TABLE_RECT = pygame.Rect(220, 170, 660, 360)
ASSEMBLY_RECT = pygame.Rect(260, 230, 580, 240)

NOTEPAD_RECT = pygame.Rect(WIDTH - 305, 30, 275, 320)
CLARITY_RECT = pygame.Rect(30, 30, 280, 22)
STATUS_RECT = pygame.Rect(30, HEIGHT - 120, WIDTH - 60, 85)

# Hands around the table:
# 16 hands: 4 per category, distributed around edges
HAND_SIZE = 64
hands = []

# Build positions: 4 top, 4 bottom, 4 left, 4 right
top_positions = [(TABLE_RECT.left + 90 + i * 150, TABLE_RECT.top - 75) for i in range(4)]
bot_positions = [(TABLE_RECT.left + 90 + i * 150, TABLE_RECT.bottom + 15) for i in range(4)]
left_positions = [(TABLE_RECT.left - 75, TABLE_RECT.top + 50 + i * 80) for i in range(4)]
right_positions = [(TABLE_RECT.right + 15, TABLE_RECT.top + 50 + i * 80) for i in range(4)]

# Assign exactly 4 hands per category in a repeating pattern
# (kept deterministic and readable)
all_positions = top_positions + bot_positions + left_positions + right_positions
category_assignments = (
    ["STRUCTURE"] * 4
    + ["ACTION"] * 4
    + ["TARGET"] * 4
    + ["CONDITION"] * 4
)

for pos, cat in zip(all_positions, category_assignments):
    rect = pygame.Rect(pos[0], pos[1], HAND_SIZE, HAND_SIZE)
    hands.append({"rect": rect, "category": cat, "anim": 0.0})

# -----------------------------
# Fonts & colors
# -----------------------------
FONT = pygame.font.SysFont("consolas", 20)
SMALL = pygame.font.SysFont("consolas", 16)
BIG = pygame.font.SysFont("consolas", 28, bold=True)

COL_BG = (22, 22, 30)
COL_TABLE = (72, 58, 48)
COL_TABLE_EDGE = (150, 125, 105)
COL_PANEL = (30, 30, 40)
COL_PANEL_EDGE = (95, 95, 110)
COL_TEXT = (245, 245, 245)
COL_MUTED = (190, 190, 205)

CATEGORY_COLORS = {
    "STRUCTURE": (120, 190, 255),
    "ACTION": (255, 180, 110),
    "TARGET": (170, 255, 170),
    "CONDITION": (255, 130, 190),
}

def draw_text(text, x, y, font=FONT, color=COL_TEXT):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_panel(rect, alpha=190):
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surf.fill((COL_PANEL[0], COL_PANEL[1], COL_PANEL[2], alpha))
    pygame.draw.rect(surf, (*COL_PANEL_EDGE, 220), surf.get_rect(), 2, border_radius=10)
    screen.blit(surf, rect.topleft)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# -----------------------------
# Game state
# -----------------------------
def reset_game():
    return {
        "clarity": MAX_CLARITY,
        "assembly": [],           # list of dicts: {"cat":..., "text":...}
        "rules_completed": 0,
        "notepad": [],            # list of completed rule strings
        "message": "Click hands to assemble a rule (STRUCTURE + ACTION + TARGET + CONDITION).",
        "message_t": 2.2,
        "ended": False,
        "end_reason": "",
    }

state = reset_game()

def set_message(msg, seconds=2.0):
    state["message"] = msg
    state["message_t"] = seconds

def has_structure_in_first_two():
    first_two = state["assembly"][:2]
    return any(t["cat"] == "STRUCTURE" for t in first_two)

def assembly_types_used():
    return {t["cat"] for t in state["assembly"]}

def assemble_rule_text():
    # Preserve click order for "visible authorship"
    return " ".join(t["text"] for t in state["assembly"])

def apply_micro_constraint_if_needed():
    # At the moment the 2nd token is added, if no STRUCTURE in first two -> penalty
    if len(state["assembly"]) == 2 and not has_structure_in_first_two():
        state["clarity"] -= MICRO_CONSTRAINT_PENALTY
        set_message("Penalty: No STRUCTURE in first two clicks. (Intentional sequencing matters.)", 2.4)

def validate_and_resolve_rule():
    used = assembly_types_used()

    # Must have exactly 4 tokens, exactly one from each category, no duplicates by category
    if len(state["assembly"]) != 4:
        return

    if used == REQUIRED:
        rule = assemble_rule_text()
        state["notepad"].append(rule)
        state["rules_completed"] += 1
        state["clarity"] = clamp(state["clarity"] + CLARITY_RESTORE_ON_VALID, 0, MAX_CLARITY)
        set_message(f"VALID RULE CREATED (+{int(CLARITY_RESTORE_ON_VALID)} clarity).", 1.8)
    else:
        state["clarity"] -= CLARITY_PENALTY_ON_INVALID
        set_message(f"INVALID RULE (missing/duplicate categories) (-{int(CLARITY_PENALTY_ON_INVALID)} clarity).", 2.0)

    state["assembly"].clear()

def end_if_needed():
    if state["ended"]:
        return
    if state["clarity"] <= 0:
        state["ended"] = True
        state["end_reason"] = "DEFEAT: Clarity collapsed into incoherence."
        set_message("DEFEAT: Clarity collapsed. Press R to restart.", 999)
    elif state["rules_completed"] >= WIN_TARGET:
        state["ended"] = True
        state["end_reason"] = "VICTORY: Recursion proven without collapse."
        set_message("VICTORY: Recursion proven. Press R to restart.", 999)

# -----------------------------
# Main loop
# -----------------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    # Passive clarity drain (pressure)
    if not state["ended"]:
        state["clarity"] -= CLARITY_DRAIN_PER_SEC * dt
        state["clarity"] = clamp(state["clarity"], 0, MAX_CLARITY)

    # Animate hand clicks
    for h in hands:
        h["anim"] = max(0.0, h["anim"] - dt * 2.5)

    # Message timer
    if state["message_t"] > 0:
        state["message_t"] -= dt
        if state["message_t"] <= 0 and not state["ended"]:
            state["message"] = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r:
                state = reset_game()

            if not state["ended"]:
                if event.key == pygame.K_BACKSPACE:
                    if state["assembly"]:
                        state["assembly"].pop()
                        state["clarity"] -= UNDO_COST
                        set_message(f"Undo (-{UNDO_COST} clarity).", 1.2)

                if event.key == pygame.K_c:
                    if state["assembly"]:
                        state["assembly"].clear()
                        state["clarity"] -= CLEAR_COST
                        set_message(f"Cleared assembly (-{CLEAR_COST} clarity).", 1.3)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["ended"]:
                continue

            mx, my = event.pos

            # Click on a hand -> add token
            for h in hands:
                if h["rect"].collidepoint(mx, my):
                    cat = h["category"]

                    # Rule assembly constraint: no duplicate categories
                    if cat in assembly_types_used():
                        state["clarity"] -= 4.0
                        set_message(f"Duplicate category '{cat}' not allowed. (-4 clarity)", 1.8)
                        h["anim"] = 1.0
                        break

                    token = random.choice(TOKEN_POOLS[cat])

                    state["assembly"].append({"cat": cat, "text": token})
                    state["clarity"] -= CLARITY_COST_PER_CLICK
                    h["anim"] = 1.0

                    apply_micro_constraint_if_needed()

                    if len(state["assembly"]) == 4:
                        validate_and_resolve_rule()
                    break

    end_if_needed()

    # -----------------------------
    # Draw
    # -----------------------------
    screen.fill(COL_BG)

    # Header
    draw_text("0002 — AT SEA", 30, 8, BIG)
    draw_text("Craft Table Recursion Chamber (mouse-only)", 30, 42, FONT, COL_MUTED)

    # Table
    pygame.draw.rect(screen, COL_TABLE, TABLE_RECT, border_radius=16)
    pygame.draw.rect(screen, COL_TABLE_EDGE, TABLE_RECT, 4, border_radius=16)
    draw_text("RULE ASSEMBLY AREA", TABLE_RECT.centerx - 150, TABLE_RECT.y + 18, BIG)

    # Assembly panel
    draw_panel(ASSEMBLY_RECT, alpha=160)
    draw_text("Current Assembly (max 4):", ASSEMBLY_RECT.x + 14, ASSEMBLY_RECT.y + 12, FONT, COL_MUTED)

    # Show assembly tokens in click order
    ay = ASSEMBLY_RECT.y + 48
    for i in range(4):
        if i < len(state["assembly"]):
            t = state["assembly"][i]
            col = CATEGORY_COLORS.get(t["cat"], COL_TEXT)
            draw_text(f"{i+1}. [{t['cat']}] {t['text']}", ASSEMBLY_RECT.x + 14, ay, FONT, col)
        else:
            draw_text(f"{i+1}. —", ASSEMBLY_RECT.x + 14, ay, FONT, (140, 140, 155))
        ay += 44

    # Hands
    for h in hands:
        cat = h["category"]
        base = CATEGORY_COLORS.get(cat, (210, 210, 225))
        # Animate: brighten on click
        t = h["anim"]
        col = (
            clamp(int(base[0] + 60 * t), 0, 255),
            clamp(int(base[1] + 60 * t), 0, 255),
            clamp(int(base[2] + 60 * t), 0, 255),
        )
        pygame.draw.rect(screen, col, h["rect"], border_radius=12)
        pygame.draw.rect(screen, (20, 20, 26), h["rect"], 2, border_radius=12)

        # Label
        abbrev = cat[:3]
        draw_text(abbrev, h["rect"].x + 12, h["rect"].y + 20, FONT, (20, 20, 26))

    # Notepad
    draw_panel(NOTEPAD_RECT, alpha=180)
    draw_text("NOTEPAD", NOTEPAD_RECT.x + 86, NOTEPAD_RECT.y + 10, BIG)
    draw_text("Completed Rules:", NOTEPAD_RECT.x + 14, NOTEPAD_RECT.y + 54, FONT, COL_MUTED)

    ny = NOTEPAD_RECT.y + 84
    # show last 8 lines
    for rule in state["notepad"][-8:]:
        # Wrap roughly
        if len(rule) <= 26:
            draw_text(f"- {rule}", NOTEPAD_RECT.x + 14, ny, SMALL, COL_TEXT)
            ny += 22
        else:
            part1 = rule[:26]
            part2 = rule[26:52]
            draw_text(f"- {part1}", NOTEPAD_RECT.x + 14, ny, SMALL, COL_TEXT)
            ny += 20
            draw_text(f"  {part2}", NOTEPAD_RECT.x + 14, ny, SMALL, COL_TEXT)
            ny += 24

    # Clarity bar
    draw_text("CLARITY", 30, 62, FONT, COL_MUTED)
    pygame.draw.rect(screen, (60, 60, 70), CLARITY_RECT, border_radius=6)
    filled_w = int(CLARITY_RECT.width * (state["clarity"] / MAX_CLARITY))
    pygame.draw.rect(screen, (120, 210, 160), pygame.Rect(CLARITY_RECT.x, CLARITY_RECT.y, filled_w, CLARITY_RECT.height), border_radius=6)
    pygame.draw.rect(screen, (210, 210, 225), CLARITY_RECT, 2, border_radius=6)
    draw_text(f"{int(state['clarity'])}/{int(MAX_CLARITY)}", CLARITY_RECT.x + 100, CLARITY_RECT.y + 2, SMALL, (20, 20, 26))

    # Score
    draw_text(f"RULES COMPLETED: {state['rules_completed']}/{WIN_TARGET}", 30, 100, FONT, COL_TEXT)

    # Helper panel: categories and examples
    helper = pygame.Rect(30, 135, 280, 220)
    draw_panel(helper, alpha=150)
    draw_text("Token Categories:", helper.x + 12, helper.y + 12, FONT, COL_MUTED)
    hy = helper.y + 46
    for cat in CATEGORIES:
        col = CATEGORY_COLORS.get(cat, COL_TEXT)
        examples = ", ".join(TOKEN_POOLS[cat][:3])
        draw_text(f"{cat}:", helper.x + 12, hy, SMALL, col)
        draw_text(examples, helper.x + 12, hy + 18, SMALL, (210, 210, 225))
        hy += 50

    # Micro-constraint reminder
    draw_text("Micro-constraint:", helper.x + 12, helper.y + 184, SMALL, COL_MUTED)
    draw_text("STRUCTURE must appear in first 2 clicks.", helper.x + 12, helper.y + 202, SMALL, (210, 210, 225))

    # Status / message
    draw_panel(STATUS_RECT, alpha=185)
    if state["message"]:
        draw_text(state["message"], STATUS_RECT.x + 14, STATUS_RECT.y + 16, FONT, COL_TEXT)

    # Controls line
    draw_text("Backspace: Undo   C: Clear   R: Restart   ESC: Quit",
              STATUS_RECT.x + 14, STATUS_RECT.y + 48, SMALL, COL_MUTED)

    # End overlay
    if state["ended"]:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))
        if state["rules_completed"] >= WIN_TARGET:
            title = "RECURSION PROVEN"
            subtitle = "You invented stable rules under decay pressure."
            col = (130, 255, 180)
        else:
            title = "INVENTION COLLAPSED"
            subtitle = "Clarity hit 0. Tighten choices and sequence earlier."
            col = (255, 120, 120)

        draw_text(title, WIDTH // 2 - 160, HEIGHT // 2 - 60, BIG, col)
        draw_text(subtitle, WIDTH // 2 - 320, HEIGHT // 2 - 20, FONT, COL_TEXT)
        draw_text("Press R to restart, ESC to quit.", WIDTH // 2 - 220, HEIGHT // 2 + 20, FONT, COL_MUTED)

    pygame.display.flip()

pygame.quit()
sys.exit(0)

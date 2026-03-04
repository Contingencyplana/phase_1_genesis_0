import sys
import math
import random
import pygame

# ============================================================
# 0003 — FLAGSHIP (Junk Arcade Skeleton)
#
# Real-time continuous combat probe.
# Player commands multiple allied ships by:
#   1) Clicking an allied ship to select it
#   2) Clicking an enemy ship to assign target
#
# Core test:
#   Attention allocation under continuous combat pressure.
#
# Movement:
#   - Fixed speed
#   - Bounded arena (no wrap)
#   - No inertia
#
# Firing:
#   - Cooldown-based
#   - Instant damage (no projectiles)
#
# Enemies:
#   - Spawn at edges
#   - Move directly toward flagship
#   - Attack when in range
#
# Allies:
#   - Default FOLLOW flagship unless assigned a target
#   - If target destroyed -> return to FOLLOW
#
# Win:
#   Destroy all enemies in wave
# Loss:
#   Flagship health reaches 0
#
# Controls:
#   Mouse: click ally to select; click enemy to assign target
#   R: restart
#   ESC: quit
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1100, 720
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("0003 — Flagship (Junk Arcade)")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 20)
SMALL = pygame.font.SysFont("consolas", 16)
BIG = pygame.font.SysFont("consolas", 28, bold=True)

COL_BG = (22, 22, 30)
COL_TEXT = (245, 245, 245)
COL_MUTED = (190, 190, 205)

COL_FLAGSHIP = (120, 190, 255)
COL_ALLY = (170, 255, 170)
COL_ENEMY = (255, 130, 190)

COL_PANEL = (30, 30, 40)
COL_PANEL_EDGE = (95, 95, 110)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def norm(dx, dy):
    mag = math.hypot(dx, dy)
    if mag == 0:
        return 0.0, 0.0
    return dx / mag, dy / mag

def draw_text(text, x, y, font=FONT, color=COL_TEXT):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_panel(rect, alpha=190):
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surf.fill((COL_PANEL[0], COL_PANEL[1], COL_PANEL[2], alpha))
    pygame.draw.rect(surf, (*COL_PANEL_EDGE, 220), surf.get_rect(), 2, border_radius=10)
    screen.blit(surf, rect.topleft)

# ------------------------------------------------------------
# Entity definitions
# ------------------------------------------------------------

class Ship:
    def __init__(self, x, y, radius, color, max_hp):
        self.x = float(x)
        self.y = float(y)
        self.r = radius
        self.color = color
        self.max_hp = float(max_hp)
        self.hp = float(max_hp)

        self.speed = 90.0  # px/sec default; overridden per type
        self.fire_range = 140.0
        self.fire_cd = 1.0
        self.fire_timer = random.uniform(0.0, self.fire_cd)

        self.dmg = 6.0
        self.attack_range = self.fire_range

        # Visual pulse when firing
        self.pulse = 0.0

    def pos(self):
        return (self.x, self.y)

    def alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0.0, self.hp - amount)

    def update_fire_timer(self, dt):
        self.fire_timer = max(0.0, self.fire_timer - dt)
        self.pulse = max(0.0, self.pulse - dt * 2.5)

    def can_fire(self):
        return self.fire_timer <= 0.0

    def reset_fire(self):
        self.fire_timer = self.fire_cd
        self.pulse = 1.0

    def move_toward(self, tx, ty, dt):
        dx = tx - self.x
        dy = ty - self.y
        ux, uy = norm(dx, dy)
        self.x += ux * self.speed * dt
        self.y += uy * self.speed * dt
        self.x = clamp(self.x, self.r, WIDTH - self.r)
        self.y = clamp(self.y, self.r, HEIGHT - self.r)

    def draw(self, selected=False):
        # firing pulse halo
        if self.pulse > 0:
            halo_r = int(self.r + 10 * self.pulse)
            pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2]), (int(self.x), int(self.y)), halo_r, 2)

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(screen, (20, 20, 26), (int(self.x), int(self.y)), self.r, 2)

        # selection ring
        if selected:
            pygame.draw.circle(screen, (255, 255, 160), (int(self.x), int(self.y)), self.r + 6, 2)

        # HP bar (tiny)
        bar_w = 46
        bar_h = 6
        bx = int(self.x - bar_w / 2)
        by = int(self.y - self.r - 14)
        pct = 0.0 if self.max_hp == 0 else (self.hp / self.max_hp)
        pct = clamp(pct, 0.0, 1.0)
        pygame.draw.rect(screen, (60, 60, 70), (bx, by, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(screen, (120, 210, 160), (bx, by, int(bar_w * pct), bar_h), border_radius=3)
        pygame.draw.rect(screen, (210, 210, 225), (bx, by, bar_w, bar_h), 1, border_radius=3)

class AllyShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, radius=14, color=COL_ALLY, max_hp=40)
        self.speed = 120.0
        self.fire_range = 170.0
        self.fire_cd = random.choice([0.9, 1.0, 1.1])
        self.dmg = 8.0

        self.state = "FOLLOW"   # FOLLOW or TARGET
        self.target = None   # object reference to target enemy

class EnemyShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, radius=14, color=COL_ENEMY, max_hp=30)
        self.speed = 58.0
        self.fire_range = 115.0
        self.fire_cd = random.choice([1.0, 1.1, 1.2])
        self.dmg = 4.5

# ------------------------------------------------------------
# Spawning
# ------------------------------------------------------------

def spawn_enemy_at_edge(side=None):
    if side is None:
        side = random.choice(["top", "bottom", "left", "right"])
    pad = 20
    if side == "top":
        return random.randint(pad, WIDTH - pad), pad
    if side == "bottom":
        return random.randint(pad, WIDTH - pad), HEIGHT - pad
    if side == "left":
        return pad, random.randint(pad, HEIGHT - pad)
    return WIDTH - pad, random.randint(pad, HEIGHT - pad)

def spawn_wave(num_enemies):
    enemies = []
    # Distribute first enemies across edges to prevent clustering
    sides = ["top", "bottom", "left", "right"]
    for i in range(min(num_enemies, 4)):
        x, y = spawn_enemy_at_edge(side=sides[i])
        enemies.append(EnemyShip(x, y))
    # Remaining enemies spawn randomly
    for _ in range(num_enemies - min(num_enemies, 4)):
        x, y = spawn_enemy_at_edge()
        enemies.append(EnemyShip(x, y))
    return enemies

# ------------------------------------------------------------
# Game State
# ------------------------------------------------------------

def new_game():
    flagship = Ship(WIDTH // 2, HEIGHT // 2 + 80, radius=18, color=COL_FLAGSHIP, max_hp=200)
    flagship.speed = 80.0
    flagship.fire_range = 0.0
    flagship.fire_cd = 999.0
    flagship.dmg = 0.0

    allies = [
        AllyShip(flagship.x - 80, flagship.y - 40),
        AllyShip(flagship.x + 80, flagship.y - 40),
        AllyShip(flagship.x, flagship.y - 95),
    ]

    enemies = spawn_wave(num_enemies=5)

    return {
        "flagship": flagship,
        "allies": allies,
        "enemies": enemies,
        "selected_ally": None,  # index of selected ally
        "message": "Click an ALLY to select, then click an ENEMY to assign target.",
        "message_t": 3.0,
        "ended": False,
        "end_reason": "",
        "kills": 0,
    }

state = new_game()

def set_message(msg, t=2.0):
    state["message"] = msg
    state["message_t"] = t

def end_if_needed():
    if state["ended"]:
        return
    if not state["flagship"].alive():
        state["ended"] = True
        state["end_reason"] = "DEFEAT: Flagship destroyed."
        set_message("DEFEAT: Flagship destroyed. Press R to restart.", 999)
    elif len(state["enemies"]) == 0:
        state["ended"] = True
        state["end_reason"] = "VICTORY: Enemy wave destroyed."
        set_message("VICTORY: Wave destroyed. Press R to restart.", 999)

# ------------------------------------------------------------
# Update Loop Helpers
# ------------------------------------------------------------

def update_allies(dt):
    flagship = state["flagship"]
    enemies = state["enemies"]

    for ally in state["allies"]:
        ally.update_fire_timer(dt)

        # Validate target reference
        if ally.state == "TARGET":
            if ally.target is None or not ally.target.alive() or ally.target not in enemies:
                ally.state = "FOLLOW"
                ally.target = None

        if ally.state == "FOLLOW":
            # Base target: trailing orbit behavior around flagship
            # (slight offset based on ally identity for spread)
            seed = (id(ally) % 3) - 1
            tx = flagship.x + seed * 55
            ty = flagship.y - 70 - (seed * 15)
            
            # Separation from nearby allies (avoid stacking)
            sep_x, sep_y = 0.0, 0.0
            separation_radius = 35.0
            separation_count = 0
            
            for other in state["allies"]:
                if other is ally:
                    continue
                d = dist(ally.pos(), other.pos())
                if d < separation_radius and d > 0:
                    # Accumulate push-away vector
                    dx = ally.x - other.x
                    dy = ally.y - other.y
                    ux, uy = norm(dx, dy)
                    sep_x += ux
                    sep_y += uy
                    separation_count += 1
            
            # Apply separation offset to target
            if separation_count > 0:
                sep_x, sep_y = norm(sep_x, sep_y)
                # Push target 15px in separation direction
                tx += sep_x * 15
                ty += sep_y * 15
            
            ally.move_toward(tx, ty, dt)

        elif ally.state == "TARGET":
            target = ally.target
            # Move toward target until within comfortable fire range
            d = dist(ally.pos(), target.pos())
            if d > ally.fire_range * 0.85:
                ally.move_toward(target.x, target.y, dt)

            # Fire if in range and cooldown ready
            if d <= ally.fire_range and ally.can_fire():
                target.take_damage(ally.dmg)
                ally.reset_fire()

def update_enemies(dt):
    flagship = state["flagship"]

    # Enemies move toward flagship and attack when in range
    for enemy in state["enemies"]:
        enemy.update_fire_timer(dt)

        if not enemy.alive():
            continue

        d = dist(enemy.pos(), flagship.pos())

        # Movement toward flagship
        if d > enemy.fire_range * 0.8:
            enemy.move_toward(flagship.x, flagship.y, dt)

        # Attack flagship if in range and cooldown ready
        if d <= enemy.fire_range and enemy.can_fire():
            flagship.take_damage(enemy.dmg)
            enemy.reset_fire()

def purge_dead_enemies():
    before = len(state["enemies"])
    state["enemies"] = [e for e in state["enemies"] if e.alive()]
    after = len(state["enemies"])
    if after < before:
        state["kills"] += (before - after)

def handle_click(mx, my):
    if state["ended"]:
        return

    # First: check allies for selection
    for idx, ally in enumerate(state["allies"]):
        if dist((mx, my), ally.pos()) <= ally.r + 4:
            state["selected_ally"] = idx
            set_message("Ally selected. Now click an enemy to assign target.", 1.6)
            return

    # If we have selected ally, check enemies for targeting
    if state["selected_ally"] is not None:
        for enemy in state["enemies"]:
            if dist((mx, my), enemy.pos()) <= enemy.r + 4:
                ally = state["allies"][state["selected_ally"]]
                ally.state = "TARGET"
                ally.target = enemy
                set_message("Target assigned.", 1.1)
                # keep selection (attention test) OR clear selection
                # For clarity, clear selection after assignment:
                state["selected_ally"] = None
                return

    # Clicking empty space clears selection
    state["selected_ally"] = None

# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------

running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    # Message decay
    if state["message_t"] > 0 and not state["ended"]:
        state["message_t"] -= dt
        if state["message_t"] <= 0:
            state["message"] = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                state = new_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_click(*event.pos)

    if not state["ended"]:
        update_allies(dt)
        update_enemies(dt)
        purge_dead_enemies()
        end_if_needed()

    # --------------------------------------------------------
    # Draw
    # --------------------------------------------------------
    screen.fill(COL_BG)

    # Title / HUD
    draw_text("0003 — FLAGSHIP", 30, 12, BIG)
    draw_text("Click ALLY → click ENEMY (selective targeting). Real-time continuous.", 30, 46, FONT, COL_MUTED)

    # Entities
    flagship = state["flagship"]
    flagship.draw(selected=False)

    for idx, ally in enumerate(state["allies"]):
        ally.draw(selected=(state["selected_ally"] == idx))

        # Draw thin line to target if assigned
        if ally.state == "TARGET" and ally.target is not None and ally.target in state["enemies"]:
            pygame.draw.line(screen, (120, 255, 140), (int(ally.x), int(ally.y)), (int(ally.target.x), int(ally.target.y)), 2)

    for enemy in state["enemies"]:
        enemy.draw(selected=False)

    # Panels
    left_panel = pygame.Rect(30, 90, 320, 160)
    draw_panel(left_panel, alpha=165)
    draw_text("STATUS", left_panel.x + 12, left_panel.y + 10, FONT, COL_MUTED)
    draw_text(f"Flagship HP: {int(flagship.hp)}/{int(flagship.max_hp)}", left_panel.x + 12, left_panel.y + 44, FONT)
    draw_text(f"Enemies Remaining: {len(state['enemies'])}", left_panel.x + 12, left_panel.y + 74, FONT)
    draw_text(f"Kills: {state['kills']}", left_panel.x + 12, left_panel.y + 104, FONT)

    # Small legend
    draw_text("Legend:", left_panel.x + 12, left_panel.y + 132, SMALL, COL_MUTED)
    draw_text("Flagship", left_panel.x + 80, left_panel.y + 132, SMALL, COL_FLAGSHIP)
    draw_text("Allies", left_panel.x + 160, left_panel.y + 132, SMALL, COL_ALLY)
    draw_text("Enemies", left_panel.x + 220, left_panel.y + 132, SMALL, COL_ENEMY)

    bottom_panel = pygame.Rect(30, HEIGHT - 110, WIDTH - 60, 80)
    draw_panel(bottom_panel, alpha=185)
    if state["message"]:
        draw_text(state["message"], bottom_panel.x + 12, bottom_panel.y + 14, FONT)
    draw_text("R: Restart   ESC: Quit", bottom_panel.x + 12, bottom_panel.y + 46, SMALL, COL_MUTED)

    # End overlay
    if state["ended"]:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        if "VICTORY" in state["end_reason"]:
            title = "VICTORY — WAVE DESTROYED"
            subtitle = "Command clarity held under continuous threat."
            col = (130, 255, 180)
        else:
            title = "DEFEAT — FLAGSHIP DESTROYED"
            subtitle = "Pressure overcame command triage."
            col = (255, 120, 120)

        draw_text(title, WIDTH // 2 - 240, HEIGHT // 2 - 60, BIG, col)
        draw_text(subtitle, WIDTH // 2 - 260, HEIGHT // 2 - 20, FONT, COL_TEXT)
        draw_text("Press R to restart, ESC to quit.", WIDTH // 2 - 220, HEIGHT // 2 + 20, FONT, COL_MUTED)

    pygame.display.flip()

pygame.quit()
sys.exit(0)

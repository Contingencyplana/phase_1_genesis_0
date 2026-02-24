import pygame
import random
import sys
import os

# Add parent directory to path for shared modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harbor_geometry import (
    WIDTH, HEIGHT,
    HARBOR_STRIP_HEIGHT,
    BOAT_HULL_WIDTH,
    BOAT_HULL_HEIGHT,
    centered_boat_x,
    docked_boat_y
)
from harbor_art import (
    draw_boat_hull,
    draw_boat_mast,
    draw_boat_sails,
    draw_child_on_boat,
    draw_captain_on_boat
)

pygame.init()

# Initialize mixer for audio
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

# Get the directory of this script for relative audio paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, "assets", "audio")

# Audio file paths (robust relative loading)
def get_audio_path(filename):
    path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(path):
        return path
    else:
        print(f"Warning: Audio file not found: {path}")
        return None

# Load sound effects (will be None if not found)
SFX_PICKUP = None
SFX_DROP = None
SFX_HIT = None
SFX_SAIL = None
SFX_DEPART = None
SFX_DEFEAT = None

try:
    if get_audio_path("sfx_pickup.wav"):
        SFX_PICKUP = pygame.mixer.Sound(get_audio_path("sfx_pickup.wav"))
    if get_audio_path("sfx_drop.wav"):
        SFX_DROP = pygame.mixer.Sound(get_audio_path("sfx_drop.wav"))
    if get_audio_path("sfx_hit.wav"):
        SFX_HIT = pygame.mixer.Sound(get_audio_path("sfx_hit.wav"))
        SFX_HIT.set_volume(0.35)
    if get_audio_path("sfx_sail.wav"):
        SFX_SAIL = pygame.mixer.Sound(get_audio_path("sfx_sail.wav"))
        SFX_SAIL.set_volume(0.4)
    if get_audio_path("sfx_depart.wav"):
        SFX_DEPART = pygame.mixer.Sound(get_audio_path("sfx_depart.wav"))
    if get_audio_path("sfx_defeat.wav"):
        SFX_DEFEAT = pygame.mixer.Sound(get_audio_path("sfx_defeat.wav"))
except Exception as e:
    print(f"Warning: Could not load audio files: {e}")

FPS = 60

PLAYER_SIZE = 25
PLAYER_SPEED = 4
INITIAL_HEALTH = 5
RESCUE_TARGET = 8

INITIAL_CRACK_INTERVAL = 2000
CRACK_GROWTH_RATE = 0.3
CRACK_SIZE = 30

FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Harbor Tremor Rescue")
clock = pygame.time.Clock()

boat_zone = pygame.Rect(0, 0, WIDTH, HARBOR_STRIP_HEIGHT)

# Start background music
music_path = get_audio_path("music_loop.ogg") or get_audio_path("music_loop.wav")
if music_path:
    try:
        # pygame.mixer.music.load(music_path)
        # pygame.mixer.music.play(-1)  # -1 means loop forever
        pass
    except Exception as e:
        print(f"Warning: Could not play music: {e}")

class ToyChild:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gender = random.choice(["boy", "girl"])
        self.variant = random.randint(0, 3)

        self.dir_timer = 0
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])

        self.body_colors = [
            (255, 100, 100),
            (100, 255, 100),
            (100, 100, 255),
            (255, 200, 100)
        ]

        self.hair_colors = [
            (80, 40, 10),
            (200, 180, 50),
            (50, 20, 0),
            (0, 0, 0)
        ]

    def rect(self):
        return pygame.Rect(self.x - 8, self.y - 18, 16, 26)

    def update(self):
        self.dir_timer += 1
        if self.dir_timer > 60:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.dir_timer = 0

        self.x += self.dx * 0.5
        self.y += self.dy * 0.5

        self.x = max(20, min(WIDTH - 20, self.x))
        self.y = max(100, min(HEIGHT - 20, self.y))

    def draw(self, surface):
        body_color = self.body_colors[self.variant]
        hair_color = self.hair_colors[self.variant]

        pygame.draw.circle(surface, (255, 220, 180), (int(self.x), int(self.y - 8)), 5)

        if self.gender == "boy":
            pygame.draw.rect(surface, hair_color, (int(self.x - 5), int(self.y - 14), 10, 4))
            pygame.draw.line(surface, body_color, (self.x, self.y - 3), (self.x, self.y + 8), 2)
        else:
            pygame.draw.line(surface, hair_color, (self.x - 4, self.y - 14), (self.x - 4, self.y - 3), 2)
            pygame.draw.line(surface, hair_color, (self.x + 4, self.y - 14), (self.x + 4, self.y - 3), 2)
            pygame.draw.polygon(surface, body_color, [
                (self.x, self.y - 3),
                (self.x - 6, self.y + 8),
                (self.x + 6, self.y + 8)
            ])


def spawn_child():
    return ToyChild(
        random.randint(50, WIDTH - 50),
        random.randint(120, HEIGHT - 50)
    )


def reset_game():
    return {
        "player": pygame.Rect(WIDTH//2, HEIGHT//2, PLAYER_SIZE, PLAYER_SIZE),
        "child": spawn_child(),
        "carrying": False,
        "rescued_children": [],
        "health": INITIAL_HEALTH,
        "cracks": [],
        "last_crack_spawn": pygame.time.get_ticks(),
        "crack_interval": INITIAL_CRACK_INTERVAL,
        "game_over": False,
        "victory": False,
        "departure_active": False,
        "departure_start_time": 0,
        "boat_offset_x": 0,
        # Audio state tracking
        "last_pickup_played": False,
        "last_drop_played": False,
        "played_depart_sound": False,
        "played_defeat_sound": False,
    }


game = reset_game()


# -------------------------------------------------
# BOAT
# -------------------------------------------------

def draw_boat(surface, rescued_children, victory, boat_offset_x=0, departure_time=0):

    boat_x = centered_boat_x(offset_x=boat_offset_x)
    boat_y = docked_boat_y(HARBOR_STRIP_HEIGHT)

    # Draw hull using shared art module
    draw_boat_hull(surface, boat_x, boat_y, BOAT_HULL_WIDTH, BOAT_HULL_HEIGHT)
    
    # Draw mast using shared art module
    draw_boat_mast(surface, boat_x, boat_y, BOAT_HULL_WIDTH)

    # Draw sails if departing
    if victory:
        draw_boat_sails(surface, boat_x, boat_y, BOAT_HULL_WIDTH, departure_time)

    # Draw children on board using shared art module
    spacing = 20
    start_x = boat_x + BOAT_HULL_WIDTH - 30

    for i, child in enumerate(rescued_children):
        cx = start_x - i * spacing
        cy = boat_y - 8
        draw_child_on_boat(surface, cx, cy, child.variant, child.gender)

    # Draw captain if victorious
    if victory:
        draw_captain_on_boat(surface, boat_x, boat_y)


def draw_captain(surface, rect):
    """Draw a tiny toy soldier captain sprite centered on the rect."""
    cx = rect.centerx
    cy = rect.centery
    
    # Legs (thick blue vertical lines)
    pygame.draw.line(surface, (50, 150, 255), (cx - 3, cy + 3), (cx - 3, cy + 10), 4)
    pygame.draw.line(surface, (50, 150, 255), (cx + 3, cy + 3), (cx + 3, cy + 10), 4)
    
    # Torso (solid rectangular block)
    pygame.draw.rect(surface, (50, 150, 255), (cx - 6, cy - 5, 12, 10))
    
    # Arms (thick horizontal lines)
    pygame.draw.line(surface, (50, 150, 255), (cx - 8, cy), (cx + 8, cy), 4)
    
    # Head (larger skin-colored circle)
    pygame.draw.circle(surface, (255, 220, 180), (cx, cy - 10), 7)
    
    # Eyes (looking slightly right)
    pygame.draw.circle(surface, (0, 0, 0), (cx - 2, cy - 10), 1)
    pygame.draw.circle(surface, (0, 0, 0), (cx + 3, cy - 10), 1)
    
    # Helmet/hat (wider blue-gray rectangle)
    pygame.draw.rect(surface, (80, 100, 150), (cx - 7, cy - 18, 14, 5))


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------

while True:
    clock.tick(FPS)
    screen.fill((30, 40, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game["game_over"] and event.key == pygame.K_r:
                game = reset_game()
                # Restart music
                music_path = get_audio_path("music_loop.ogg") or get_audio_path("music_loop.wav")
                if music_path:
                    try:
                        # pygame.mixer.music.load(music_path)
                        # pygame.mixer.music.play(-1)
                        pass
                    except Exception as e:
                        print(f"Warning: Could not play music: {e}")

    if not game["game_over"]:

        # Freeze player movement during departure
        if not game["departure_active"]:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                game["player"].x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                game["player"].x += PLAYER_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                game["player"].y -= PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                game["player"].y += PLAYER_SPEED

            game["player"].clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        if game["child"] is not None and not game["departure_active"]:
            game["child"].update()

        if game["child"] is not None and not game["carrying"] and game["player"].colliderect(game["child"].rect()):
            game["carrying"] = True
            if SFX_PICKUP:
                SFX_PICKUP.play()

        if game["carrying"] and boat_zone.colliderect(game["player"]):
            game["rescued_children"].append(game["child"])
            if SFX_DROP:
                # SFX_DROP.play()
                pass
            game["carrying"] = False
            if len(game["rescued_children"]) < RESCUE_TARGET:
                game["child"] = spawn_child()

        # Freeze hazard mechanics during departure
        if not game["departure_active"]:
            now = pygame.time.get_ticks()
            if now - game["last_crack_spawn"] > game["crack_interval"]:
                game["cracks"].append(
                    pygame.Rect(
                        random.randint(0, WIDTH - CRACK_SIZE),
                        random.randint(100, HEIGHT - CRACK_SIZE),
                        CRACK_SIZE,
                        CRACK_SIZE
                    )
                )
                game["last_crack_spawn"] = now
                game["crack_interval"] = max(500, game["crack_interval"] - 50)

            for crack in game["cracks"]:
                crack.inflate_ip(CRACK_GROWTH_RATE, CRACK_GROWTH_RATE)

            for crack in game["cracks"]:
                if game["player"].colliderect(crack):
                    game["health"] -= 1
                    if SFX_HIT:
                        SFX_HIT.play()
                    game["player"].center = (WIDTH//2, HEIGHT//2)
                    break

        if len(game["rescued_children"]) >= RESCUE_TARGET and not game["departure_active"]:
            game["victory"] = True
            game["departure_active"] = True
            if SFX_SAIL:
                SFX_SAIL.play()
            game["departure_start_time"] = pygame.time.get_ticks()
            game["child"] = None

        if game["health"] <= 0:
            game["game_over"] = True
            game["victory"] = False
            if not game["played_defeat_sound"]:
                if SFX_DEFEAT:
                    # SFX_DEFEAT.play()
                    pass
                game["played_defeat_sound"] = True

    # Handle departure sequence
    if game["departure_active"]:
        elapsed = (pygame.time.get_ticks() - game["departure_start_time"]) / 1000.0

        # Boat movement starts at t=0.4s
        if elapsed >= 0.4:
            if not game["played_depart_sound"]:
                if SFX_DEPART:
                    # SFX_DEPART.play()
                    pass
                game["played_depart_sound"] = True
            
            movement_time = elapsed - 0.4

            # Acceleration phase: 0.0 to 0.25s
            if movement_time <= 0.25:
                departure_speed = 150
                game["boat_offset_x"] = 0.5 * departure_speed * (movement_time ** 2) / 0.25
            else:
                # Constant glide speed after acceleration
                accel_distance = 0.5 * 150 * 0.25
                glide_time = movement_time - 0.25
                game["boat_offset_x"] = accel_distance + 150 * glide_time

        # Check if boat left edge is off-screen
        boat_x = centered_boat_x(offset_x=game["boat_offset_x"])
        if boat_x > WIDTH:
            game["game_over"] = True

    # Draw harbor strip

    pygame.draw.rect(screen, (80, 120, 160), boat_zone)

    hud = FONT.render(
        f"Rescued: {len(game['rescued_children'])}/{RESCUE_TARGET}   Health: {game['health']}",
        True,
        (255,255,255)
    )
    screen.blit(hud, (20, 50))

    departure_time = 0
    if game["departure_active"]:
        departure_time = (pygame.time.get_ticks() - game["departure_start_time"]) / 1000.0

    draw_boat(screen, game["rescued_children"], game["victory"], game["boat_offset_x"], departure_time)

    draw_captain(screen, game["player"])

    if not game["carrying"] and game["child"] is not None and not game["departure_active"]:
        game["child"].draw(screen)

    for crack in game["cracks"]:
        pygame.draw.rect(screen, (200, 50, 50), crack)

    if game["game_over"]:
        msg = "All Safe! Victory!" if game["victory"] else "Harbor Collapsed!"
        text = BIG_FONT.render(msg, True, (255,255,255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 40))
        restart = FONT.render("Press R to Restart", True, (255,255,255))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()

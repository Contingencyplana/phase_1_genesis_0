"""
Harbor Art - Shared boat and character rendering for arcade games
Implements consistent visual style across harbor-themed games
"""

import pygame


def draw_boat_hull(surface, boat_x, boat_y, boat_width=240, boat_height=30):
    """
    Draw the boat hull polygon.
    
    Args:
        surface: pygame surface to draw on
        boat_x: left edge X coordinate
        boat_y: top edge Y coordinate
        boat_width: width of hull (default: 240 from contract)
        boat_height: height of hull (default: 30 from contract)
    """
    pygame.draw.polygon(surface, (120, 70, 30), [
        (boat_x + 20, boat_y + boat_height),
        (boat_x, boat_y),
        (boat_x + boat_width, boat_y),
        (boat_x + boat_width - 30, boat_y + boat_height),
    ])


def draw_boat_mast(surface, boat_x, boat_y, boat_width=240):
    """
    Draw the boat mast (vertical pole from hull to top of screen).
    
    Args:
        surface: pygame surface to draw on
        boat_x: left edge X coordinate of boat
        boat_y: top edge Y coordinate of boat
        boat_width: width of hull (for centering mast)
    """
    mast_x = boat_x + boat_width // 2
    pygame.draw.line(surface, (200, 200, 200),
                     (mast_x, boat_y),
                     (mast_x, 0), 3)


def draw_boat_sails(surface, boat_x, boat_y, boat_width=240, departure_time=0.0):
    """
    Draw rectangular sails for departure (unfurl progressively).
    
    Args:
        surface: pygame surface to draw on
        boat_x: left edge X coordinate of boat
        boat_y: top edge Y coordinate of boat
        boat_width: width of hull
        departure_time: seconds elapsed since departure started (for animation)
    """
    mast_x = boat_x + boat_width // 2
    
    if departure_time >= 0.0:
        # Right sail unfurls first
        pygame.draw.polygon(surface, (255, 255, 255), [
            (mast_x, 0),
            (mast_x + 70, 0),
            (mast_x + 80, boat_y - 5),
            (mast_x, boat_y - 5)
        ])
    
    if departure_time >= 0.2:
        # Left sail unfurls 0.2s later
        pygame.draw.polygon(surface, (255, 255, 255), [
            (mast_x - 70, 0),
            (mast_x, 0),
            (mast_x, boat_y - 5),
            (mast_x - 80, boat_y - 5)
        ])


def draw_child_on_boat(surface, x, y, variant=0, gender="boy"):
    """
    Draw a child sprite on the boat (head with eyes and hair).
    
    Args:
        surface: pygame surface to draw on
        x: center X coordinate
        y: center Y coordinate (of the head)
        variant: 0-3 (selects hair color)
        gender: "boy" or "girl" (affects hair style)
    """
    hair_colors = [
        (80, 40, 10),      # Brown
        (200, 180, 50),    # Blonde
        (50, 20, 0),       # Dark brown
        (0, 0, 0)          # Black
    ]
    
    # Head (skin tone)
    pygame.draw.circle(surface, (255, 220, 180), (x, y), 5)
    
    # Eyes
    pygame.draw.circle(surface, (0, 0, 0), (x - 2, y), 1)
    pygame.draw.circle(surface, (0, 0, 0), (x + 2, y), 1)
    
    # Hair (style depends on gender)
    hair_color = hair_colors[variant % len(hair_colors)]
    if gender == "boy":
        pygame.draw.rect(surface, hair_color, (x - 5, y - 6, 10, 4))
    else:
        # Girl: pigtails (two lines)
        pygame.draw.line(surface, hair_color, (x - 4, y - 6), (x - 4, y + 1), 2)
        pygame.draw.line(surface, hair_color, (x + 4, y - 6), (x + 4, y + 1), 2)


def draw_captain_on_boat(surface, boat_x, boat_y):
    """
    Draw the captain standing on the boat (simple head + torso).
    
    Args:
        surface: pygame surface to draw on
        boat_x: left edge X coordinate of boat
        boat_y: top edge Y coordinate of boat
    """
    cap_x = boat_x + 15
    cap_y = boat_y - 16
    
    # Head (skin tone)
    pygame.draw.circle(surface, (255, 220, 180), (cap_x, cap_y), 6)
    
    # Eyes (looking slightly right)
    pygame.draw.circle(surface, (0, 0, 0), (cap_x - 1, cap_y), 1)
    pygame.draw.circle(surface, (0, 0, 0), (cap_x + 3, cap_y), 1)
    
    # Torso (blue uniform - simple line)
    pygame.draw.line(surface, (50, 150, 255),
                     (cap_x, cap_y + 4),
                     (cap_x, cap_y + 15), 3)


def draw_docked_boat_with_children(surface, boat_x, boat_y, children_count, 
                                    show_captain=True, boat_width=240, boat_height=30):
    """
    High-level function: draw complete docked boat with children and captain.
    
    Args:
        surface: pygame surface to draw on
        boat_x: left edge X coordinate
        boat_y: top edge Y coordinate
        children_count: number of children to draw on boat
        show_captain: whether to draw the captain
        boat_width: width of hull
        boat_height: height of hull
    """
    # Draw hull
    draw_boat_hull(surface, boat_x, boat_y, boat_width, boat_height)
    
    # Draw mast
    draw_boat_mast(surface, boat_x, boat_y, boat_width)
    
    # Draw children (spaced along the boat)
    spacing = 20
    start_x = boat_x + boat_width - 30
    
    for i in range(children_count):
        cx = start_x - i * spacing
        cy = boat_y - 8
        # Alternate gender and cycle through variants for variety
        gender = "girl" if i % 2 == 0 else "boy"
        variant = i % 4
        draw_child_on_boat(surface, cx, cy, variant, gender)
    
    # Draw captain
    if show_captain:
        draw_captain_on_boat(surface, boat_x, boat_y)

"""
Harbor Geometry - Shared visual constants and helpers
Implements: arcade_games/design/harbor_visual_contract.md
"""

# Screen dimensions (contract §1)
WIDTH = 800
HEIGHT = 600

# Harbor strip / boat zone (contract §1)
HARBOR_STRIP_HEIGHT = 80

# Boat geometry (contract §2)
BOAT_HULL_WIDTH = 240
BOAT_HULL_HEIGHT = 30

# Docking clearance (contract §4)
HULL_CLEARANCE = 4  # pixels between hull bottom and dock top


def centered_boat_x(boat_width=BOAT_HULL_WIDTH, offset_x=0):
    """
    Compute horizontally centered boat position.
    
    Args:
        boat_width: Width of the boat hull (default: BOAT_HULL_WIDTH)
        offset_x: Optional horizontal offset for animations
    
    Returns:
        X coordinate for boat's left edge
        
    Contract: §5 - Horizontal Centering Rule
    """
    return WIDTH // 2 - boat_width // 2 + offset_x


def docked_boat_y(dock_top_y, hull_height=BOAT_HULL_HEIGHT, clearance=HULL_CLEARANCE):
    """
    Compute vertically aligned boat position for docking.
    
    Args:
        dock_top_y: Y coordinate of dock's top edge (or harbor strip bottom)
        hull_height: Height of the boat hull (default: BOAT_HULL_HEIGHT)
        clearance: Visual gap between hull bottom and dock (default: HULL_CLEARANCE)
    
    Returns:
        Y coordinate for boat's top edge
        
    Contract: §4 - Vertical Dock Alignment Rule
    Formula: boat_y = dock_top_y - clearance - hull_height
    """
    return dock_top_y - clearance - hull_height

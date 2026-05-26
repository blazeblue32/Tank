import math

from core.constants import *

from world.terrain import *

# =====================================================
# VISION DIRECTION
# =====================================================
    
def angle_difference(a, b):

    diff = abs(a - b) % 360

    return min(
        diff,
        360 - diff
    )
    
def directional_vision_modifier(
    observer,
    target
):

    dx = target.x - observer.x
    dy = target.y - observer.y

    angle_to_target = math.degrees(
        math.atan2(dy, dx)
    ) % 360

    facing_angle = DIRECTION_ANGLES[
        observer.turret_direction
    ]

    difference = angle_difference(
        angle_to_target,
        facing_angle
    )

    # ================================================
    # SMOOTH FALLOFF
    # ================================================

    modifier = math.cos(
        math.radians(difference)
    )

    # ================================================
    # NORMALIZE
    # ================================================

    modifier = (
        modifier + 1.0
    ) / 2.0

    # ================================================
    # MINIMUM AWARENESS
    # ================================================

    modifier = max(
        0.25,
        modifier
    )

    return modifier
    
# =====================================================
# VISIBILITY
# =====================================================

def can_see(
    observer,
    target
):

    dx = target.x - observer.x
    dy = target.y - observer.y

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    # ================================================
    # MINIMUM DETECTION
    # ================================================

    if distance <= 48:
        return True

    detection_range = (
        observer.detection_range
    )

    # ================================================
    # DIRECTIONAL VISION
    # ================================================

    detection_range *= (
        directional_vision_modifier(
            observer,
            target
        )
    )

    # ================================================
    # TARGET CONCEALMENT
    # ================================================

    terrain = observer.tilemap.get_tile(
        target.tile_x,
        target.tile_y
    )

    if terrain is not None:

        concealment = terrain_concealment(
            terrain
        )

        detection_range *= (
            1.0 - concealment
        )

    # ================================================
    # OBSTRUCTION
    # ================================================

    obstruction = (
        observer.tilemap.calculate_obstruction_between(
            observer.tile_x,
            observer.tile_y,
            target.tile_x,
            target.tile_y
        )
    )

    detection_range *= max(
        0.2,
        1.0 - (
            obstruction * 0.15
        )
    )

    return distance <= detection_range
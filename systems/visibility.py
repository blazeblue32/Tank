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

    # ============================================
    # ANGLE DIFFERENCE
    # ============================================

    angle_diff = abs(
        observer_angle -
        target_angle
    )

    if angle_diff > 180:

        angle_diff = 360 - angle_diff

    # ============================================
    # DIRECTIONAL AWARENESS
    # ============================================

    # FRONT ARC
    if angle_diff <= 45:

        return 2.0

    # SIDE ARC
    elif angle_diff <= 135:

        return 1.0

    # REAR ARC
    else:

        return 0.75

# =====================================================
# RAYCAST VISIBILITY
# =====================================================

def raycast_visibility_strength(
    observer,
    target_tile_x,
    target_tile_y
):

    start_x = (
        observer.tile_x +
        0.5
    )

    start_y = (
        observer.tile_y +
        0.5
    )

    end_x = (
        target_tile_x +
        0.5
    )

    end_y = (
        target_tile_y +
        0.5
    )

    dx = end_x - start_x
    dy = end_y - start_y

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    # ============================================
    # ZERO DISTANCE
    # ============================================

    if distance <= 0.01:

        return 1.0

    # ============================================
    # SUB-TILE RAY STEPS
    # ============================================

    steps = max(
        1,
        int(distance * 4)
    )

    step_x = dx / steps
    step_y = dy / steps

    visibility = 1.0

    visited_tiles = set()

    current_x = start_x
    current_y = start_y

    for i in range(steps):

        current_x += step_x
        current_y += step_y

        tile_x = int(current_x)
        tile_y = int(current_y)

        # ========================================
        # MAP BOUNDS
        # ========================================

        if (
            tile_x < 0 or
            tile_y < 0 or
            tile_x >= MAP_WIDTH or
            tile_y >= MAP_HEIGHT
        ):

            return 0.0

        if (
            tile_x,
            tile_y
        ) in visited_tiles:

            continue

        visited_tiles.add(
            (
                tile_x,
                tile_y
            )
        )
        
        tile = observer.tilemap.get_tile(
            tile_x,
            tile_y
        )

        obstruction = terrain_obstruction(
            tile
        )

        distance_fraction = (
            i / steps
        )

        # ========================================
        # SOFT DISTANCE WEIGHTING
        # ========================================

        weighted_obstruction = (
            obstruction *
            (distance_fraction * 0.35)
        )

        # ========================================
        # SOFT ATTENUATION
        # ========================================

        visibility -= (
            weighted_obstruction *
            (
                1.0 +
                ((1.0 - visibility) * 1.5)
            )
        )

        # ========================================
        # VISIBILITY COLLAPSE
        # ========================================

        if visibility <= 0.15:

            return 0.0

    return max(
        0.0,
        min(1.0, visibility)
    )

def visibility_strength_between(
    observer,
    target_tile_x,
    target_tile_y
):

    dx = (
        target_tile_x -
        observer.tile_x
    )

    dy = (
        target_tile_y -
        observer.tile_y
    )

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    # ============================================
    # DIRECTIONAL VISIBILITY
    # ============================================

    target_angle = (
        math.degrees(
            math.atan2(dy, dx)
        ) % 360
    )

    facing_angle = DIRECTION_ANGLES[
        observer.turret_direction
    ]

    angle_diff = (
        (target_angle - facing_angle + 180)
        % 360
    ) - 180

    angle_diff = abs(angle_diff)

    direction_modifier = math.cos(
        math.radians(angle_diff)
    )

    direction_modifier = (
        direction_modifier + 1.0
    ) / 2.0

    direction_modifier = max(
        0.45,
        direction_modifier
    )

    effective_range = (
        observer.view_range *
        direction_modifier
    )

    # ============================================
    # RANGE FAILURE
    # ============================================

    if distance > effective_range:

        return 0.0

    # ============================================
    # BASE VISIBILITY
    # ============================================

    visibility = 1.0

    # ============================================
    # DISTANCE ATTENUATION
    # ============================================

    visibility *= (
        1.0 -
        (distance / effective_range)
    )

    # ============================================
    # RAYCAST VISIBILITY
    # ============================================

    visibility *= raycast_visibility_strength(
        observer,
        target_tile_x,
        target_tile_y
    )

    return max(
        0.0,
        min(1.0, visibility)
    )
   
# =====================================================
# VISIBILITY
# =====================================================

def can_see(
    observer,
    target
):

    visibility = visibility_strength_between(
        observer,
        target.tile_x,
        target.tile_y
    )

    return visibility >= 0.15
    
def can_see_tile(
    observer,
    tile_x,
    tile_y
):

    visibility = visibility_strength_between(
        observer,
        tile_x,
        tile_y
    )

    return visibility >= 0.15
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
        0.45,
        modifier
    )

    return modifier

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

    effective_range = observer.view_range

    # ============================================
    # RANGE FAILURE
    # ============================================

    if distance > effective_range:

        return 0.0

    # ============================================
    # BASE VISIBILITY
    # ============================================

    visibility = direction_modifier

    # ============================================
    # DISTANCE ATTENUATION
    # ============================================

    visibility *= (
        1.0 -
        (distance / effective_range)
    )

    # ============================================
    # PROPAGATED OBSTRUCTION
    # ============================================

    obstruction_visibility = (
        propagated_visibility(
            observer.tilemap,
            observer.tile_x,
            observer.tile_y,
            target_tile_x,
            target_tile_y
        )
    )

    visibility *= obstruction_visibility

    return max(
        0.0,
        min(1.0, visibility)
    )

# =====================================================
# OBSTRUCTION TRACE
# =====================================================

def propagated_visibility(
    tilemap,
    x1,
    y1,
    x2,
    y2
):

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x = x1
    y = y1

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    visibility = 1.0
    
    x += sx
    y += sy

    # =============================================
    # BRESENHAM TRACE
    # =============================================

    if dx > dy:

        err = dx / 2.0

        while x != x2:

            # =====================================
            # MAP BOUNDS
            # =====================================

            if (
                x < 0 or
                y < 0 or
                x >= MAP_WIDTH or
                y >= MAP_HEIGHT
            ):

                return 0.0

            tile = tilemap.get_tile(x, y)

            obstruction = terrain_obstruction(
                tile
            )

            visibility *= (
                1.0 - (obstruction * 0.75)
            )

            # =====================================
            # VISIBILITY COLLAPSE
            # =====================================

            if visibility <= 0.15:

                return 0.0

            err -= dy

            if err < 0:

                y += sy
                err += dx

            x += sx

    else:

        err = dy / 2.0

        while y != y2:

            # =====================================
            # MAP BOUNDS
            # =====================================

            if (
                x < 0 or
                y < 0 or
                x >= MAP_WIDTH or
                y >= MAP_HEIGHT
            ):

                return 0.0

            tile = tilemap.get_tile(x, y)

            obstruction = terrain_obstruction(
                tile
            )

            visibility *= (
                1.0 - obstruction
            )

            # =====================================
            # VISIBILITY COLLAPSE
            # =====================================

            if visibility <= 0.15:

                return 0.0

            err -= dx

            if err < 0:

                x += sx
                err += dy

            y += sy

    return visibility
   
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

    return visibility > 0.15
    
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

    return visibility > 0.15
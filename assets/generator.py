"""
Asset generator for creating all pixel art sprites and tiles.
Generates Zelda-style 32x32 pixel art programmatically.
"""

import os
import sys
from PIL import Image, ImageDraw
import numpy as np

# Add parent directory to path to import constants
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from game.constants import *


def scale_pixel_array(pixel_array, scale=2):
    """
    Scale a pixel array by a given factor.
    Each pixel becomes a scale x scale block.

    Args:
        pixel_array: 2D list of pixel values
        scale: Scaling factor (default 2 for 16x16 -> 32x32)

    Returns:
        Scaled 2D list
    """
    scaled = []
    for row in pixel_array:
        # Create 'scale' copies of each row
        for _ in range(scale):
            scaled_row = []
            for pixel in row:
                # Repeat each pixel 'scale' times
                scaled_row.extend([pixel] * scale)
            scaled.append(scaled_row)
    return scaled


def create_image_from_array(pixel_array, color_map, scale=2):
    """
    Create a PIL Image from a 2D pixel array and color map.

    Args:
        pixel_array: 2D list where each value is a color key (16x16 original)
        color_map: Dict mapping keys to RGB(A) tuples
        scale: Scaling factor to apply (default 2 for 32x32 output)

    Returns:
        PIL Image
    """
    # Scale the pixel array
    if scale > 1:
        pixel_array = scale_pixel_array(pixel_array, scale)

    height = len(pixel_array)
    width = len(pixel_array[0])

    # Create RGBA image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            color_key = pixel_array[y][x]
            if color_key in color_map:
                color = color_map[color_key]
                # Ensure color is RGBA
                if len(color) == 3:
                    color = (*color, 255)
                pixels[x, y] = color

    return img


def generate_player_sprites():
    """Generate player character sprites for all directions and animations."""

    # Color map for player
    colors = {
        0: (0, 0, 0, 0),  # Transparent
        1: HAIR_YELLOW,
        2: HAIR_DARK,
        3: SKIN_PEACH,
        4: SKIN_DARK,
        5: TUNIC_GREEN,
        6: TUNIC_DARK,
        7: OUTLINE_BLACK,
    }

    # Player facing down (idle)
    player_down = [
        [0,0,0,0,7,7,7,7,7,7,0,0,0,0,0,0],
        [0,0,0,7,1,1,1,1,1,1,7,0,0,0,0,0],
        [0,0,7,1,1,1,1,1,1,1,1,7,0,0,0,0],
        [0,0,7,2,1,1,1,1,1,1,2,7,0,0,0,0],
        [0,0,7,7,7,3,3,3,3,7,7,7,0,0,0,0],
        [0,0,0,7,3,3,3,3,3,3,7,0,0,0,0,0],
        [0,0,0,7,4,3,3,3,3,4,7,0,0,0,0,0],
        [0,0,7,5,7,7,7,7,7,7,5,7,0,0,0,0],
        [0,7,5,5,5,5,5,5,5,5,5,5,7,0,0,0],
        [0,7,6,5,5,5,5,5,5,5,5,6,7,0,0,0],
        [0,7,6,5,5,5,5,5,5,5,5,6,7,0,0,0],
        [0,0,7,6,5,5,7,7,5,5,6,7,0,0,0,0],
        [0,0,7,6,6,7,0,0,7,6,6,7,0,0,0,0],
        [0,0,0,7,7,0,0,0,0,7,7,0,0,0,0,0],
        [0,0,0,7,4,7,0,0,7,4,7,0,0,0,0,0],
        [0,0,0,0,7,7,0,0,7,7,0,0,0,0,0,0],
    ]

    # Player facing up
    player_up = [
        [0,0,0,0,7,7,7,7,7,7,0,0,0,0,0,0],
        [0,0,0,7,1,1,1,1,1,1,7,0,0,0,0,0],
        [0,0,7,1,1,1,1,1,1,1,1,7,0,0,0,0],
        [0,0,7,2,1,1,1,1,1,1,2,7,0,0,0,0],
        [0,0,7,7,7,3,3,3,3,7,7,7,0,0,0,0],
        [0,0,0,7,3,7,7,7,7,3,7,0,0,0,0,0],
        [0,0,0,7,3,3,3,3,3,3,7,0,0,0,0,0],
        [0,0,7,5,7,7,7,7,7,7,5,7,0,0,0,0],
        [0,7,5,5,5,5,5,5,5,5,5,5,7,0,0,0],
        [0,7,6,5,5,5,5,5,5,5,5,6,7,0,0,0],
        [0,7,6,5,5,5,5,5,5,5,5,6,7,0,0,0],
        [0,0,7,6,5,5,7,7,5,5,6,7,0,0,0,0],
        [0,0,7,6,6,7,0,0,7,6,6,7,0,0,0,0],
        [0,0,0,7,7,0,0,0,0,7,7,0,0,0,0,0],
        [0,0,0,7,4,7,0,0,7,4,7,0,0,0,0,0],
        [0,0,0,0,7,7,0,0,7,7,0,0,0,0,0,0],
    ]

    # Player facing left
    player_left = [
        [0,0,0,0,0,7,7,7,7,7,0,0,0,0,0,0],
        [0,0,0,0,7,1,1,1,1,1,7,0,0,0,0,0],
        [0,0,0,7,1,1,1,1,1,1,1,7,0,0,0,0],
        [0,0,0,7,2,1,1,1,1,1,2,7,0,0,0,0],
        [0,0,0,7,7,3,3,3,3,7,7,0,0,0,0,0],
        [0,0,0,0,7,3,3,3,3,7,0,0,0,0,0,0],
        [0,0,0,0,7,4,3,3,4,7,0,0,0,0,0,0],
        [0,0,0,7,5,7,7,7,7,5,7,0,0,0,0,0],
        [0,0,7,5,5,5,5,5,5,5,5,7,0,0,0,0],
        [0,0,7,6,5,5,5,5,5,5,5,7,0,0,0,0],
        [0,0,7,6,5,5,5,5,5,5,6,7,0,0,0,0],
        [0,0,0,7,6,5,5,7,7,6,7,0,0,0,0,0],
        [0,0,0,7,6,6,7,0,0,7,0,0,0,0,0,0],
        [0,0,0,0,7,7,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,7,4,7,0,0,7,7,0,0,0,0,0],
        [0,0,0,0,0,7,7,0,0,7,7,0,0,0,0,0],
    ]

    # Player facing right (mirror of left)
    player_right = [list(reversed(row)) for row in player_left]

    # Save idle sprites
    img = create_image_from_array(player_down, colors)
    img.save('assets/sprites/player_down.png')

    img = create_image_from_array(player_up, colors)
    img.save('assets/sprites/player_up.png')

    img = create_image_from_array(player_left, colors)
    img.save('assets/sprites/player_left.png')

    img = create_image_from_array(player_right, colors)
    img.save('assets/sprites/player_right.png')

    # Generate walk animations (simple variant with legs adjusted)
    # Walk frame 1 for down (left leg forward)
    player_down_walk1 = player_down.copy()
    player_down_walk1[13] = [0,0,7,6,6,7,0,0,0,7,7,0,0,0,0,0]
    player_down_walk1[14] = [0,7,4,7,0,0,0,0,7,4,7,0,0,0,0,0]
    player_down_walk1[15] = [0,7,7,0,0,0,0,0,0,7,7,0,0,0,0,0]

    img = create_image_from_array(player_down_walk1, colors)
    img.save('assets/sprites/player_down_walk1.png')

    # Walk frame 2 for down (right leg forward)
    player_down_walk2 = player_down.copy()
    player_down_walk2[13] = [0,0,0,7,7,0,0,0,7,6,6,7,0,0,0,0]
    player_down_walk2[14] = [0,0,7,4,7,0,0,0,0,0,7,4,7,0,0,0]
    player_down_walk2[15] = [0,0,0,7,7,0,0,0,0,0,0,7,7,0,0,0]

    img = create_image_from_array(player_down_walk2, colors)
    img.save('assets/sprites/player_down_walk2.png')

    print("Player sprites generated successfully!")


def generate_sword_sprites():
    """Generate sword swing sprites for all directions."""

    colors = {
        0: (0, 0, 0, 0),  # Transparent
        1: SWORD_BLADE,
        2: SWORD_HANDLE,
        3: OUTLINE_BLACK,
    }

    # Sword swinging down (in front of player)
    sword_down = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,2,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    # Sword swinging up
    sword_up = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,2,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    # Sword swinging left
    sword_left = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,3,2,3,3,3,3,3,3,3,0,0,0,0,0,0],
        [0,0,3,1,1,1,1,1,1,3,0,0,0,0,0,0],
        [0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    # Sword swinging right (mirror of left)
    sword_right = [list(reversed(row)) for row in sword_left]

    # Save sword sprites
    img = create_image_from_array(sword_down, colors)
    img.save('assets/sprites/sword_down.png')

    img = create_image_from_array(sword_up, colors)
    img.save('assets/sprites/sword_up.png')

    img = create_image_from_array(sword_left, colors)
    img.save('assets/sprites/sword_left.png')

    img = create_image_from_array(sword_right, colors)
    img.save('assets/sprites/sword_right.png')

    print("Sword sprites generated successfully!")


def generate_enemy_sprites():
    """Generate enemy sprites (slime and skeleton)."""

    # Slime colors
    slime_colors = {
        0: (0, 0, 0, 0),
        1: SLIME_GREEN,
        2: SLIME_DARK,
        3: OUTLINE_BLACK,
        4: TEXT_WHITE,  # Eyes
    }

    # Slime idle frame 1
    slime1 = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0],
        [0,0,0,3,1,1,1,1,1,1,3,0,0,0,0,0],
        [0,0,3,1,1,1,1,1,1,1,1,3,0,0,0,0],
        [0,0,3,1,3,4,1,1,3,4,1,3,0,0,0,0],
        [0,0,3,1,3,4,1,1,3,4,1,3,0,0,0,0],
        [0,3,1,1,1,1,1,1,1,1,1,1,3,0,0,0],
        [0,3,2,1,1,1,3,3,1,1,1,2,3,0,0,0],
        [0,3,2,2,1,3,1,1,3,1,2,2,3,0,0,0],
        [0,0,3,2,2,1,1,1,1,2,2,3,0,0,0,0],
        [0,0,0,3,2,2,2,2,2,2,3,0,0,0,0,0],
        [0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    # Slime idle frame 2 (slightly squished)
    slime2 = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0],
        [0,0,3,1,1,1,1,1,1,1,1,3,0,0,0,0],
        [0,3,1,1,3,4,1,1,3,4,1,1,3,0,0,0],
        [0,3,1,1,3,4,1,1,3,4,1,1,3,0,0,0],
        [0,3,2,1,1,1,1,1,1,1,1,1,3,0,0,0],
        [0,3,2,2,1,1,3,3,1,1,2,2,3,0,0,0],
        [0,3,2,2,1,3,1,1,3,1,2,2,3,0,0,0],
        [0,0,3,2,2,1,1,1,1,2,2,3,0,0,0,0],
        [0,0,0,3,2,2,2,2,2,2,3,0,0,0,0,0],
        [0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    img = create_image_from_array(slime1, slime_colors)
    img.save('assets/sprites/slime1.png')

    img = create_image_from_array(slime2, slime_colors)
    img.save('assets/sprites/slime2.png')

    # Skeleton colors
    skeleton_colors = {
        0: (0, 0, 0, 0),
        1: SKELETON_BONE,
        2: SKELETON_GRAY,
        3: OUTLINE_BLACK,
        4: HEART_RED,  # Eyes
    }

    # Skeleton frame 1
    skeleton1 = [
        [0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0],
        [0,0,0,0,3,1,1,1,1,3,0,0,0,0,0,0],
        [0,0,0,3,1,1,1,1,1,1,3,0,0,0,0,0],
        [0,0,0,3,3,4,3,3,4,3,3,0,0,0,0,0],
        [0,0,0,3,1,1,1,1,1,1,3,0,0,0,0,0],
        [0,0,0,0,3,1,3,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,3,3,2,2,3,3,0,0,0,0,0,0],
        [0,0,0,3,2,2,2,2,2,2,3,0,0,0,0,0],
        [0,0,3,2,2,2,2,2,2,2,2,3,0,0,0,0],
        [0,0,0,3,2,2,2,2,2,2,3,0,0,0,0,0],
        [0,0,0,0,3,2,2,2,2,3,0,0,0,0,0,0],
        [0,0,0,0,3,1,3,3,1,3,0,0,0,0,0,0],
        [0,0,0,3,1,1,3,3,1,1,3,0,0,0,0,0],
        [0,0,0,3,1,1,0,0,1,1,3,0,0,0,0,0],
        [0,0,0,3,1,3,0,0,3,1,3,0,0,0,0,0],
        [0,0,0,0,3,0,0,0,0,3,0,0,0,0,0,0],
    ]

    # Skeleton frame 2 (legs moved)
    skeleton2 = [
        [0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0],
        [0,0,0,0,3,1,1,1,1,3,0,0,0,0,0,0],
        [0,0,0,3,1,1,1,1,1,1,3,0,0,0,0,0],
        [0,0,0,3,3,4,3,3,4,3,3,0,0,0,0,0],
        [0,0,0,3,1,1,1,1,1,1,3,0,0,0,0,0],
        [0,0,0,0,3,1,3,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,3,3,2,2,3,3,0,0,0,0,0,0],
        [0,0,0,3,2,2,2,2,2,2,3,0,0,0,0,0],
        [0,0,3,2,2,2,2,2,2,2,2,3,0,0,0,0],
        [0,0,0,3,2,2,2,2,2,2,3,0,0,0,0,0],
        [0,0,0,0,3,2,2,2,2,3,0,0,0,0,0,0],
        [0,0,0,0,3,1,3,3,1,3,0,0,0,0,0,0],
        [0,0,0,0,3,1,3,3,1,3,0,0,0,0,0,0],
        [0,0,0,3,1,1,0,0,1,1,3,0,0,0,0,0],
        [0,0,0,3,1,3,0,0,3,1,3,0,0,0,0,0],
        [0,0,0,0,3,0,0,0,0,3,0,0,0,0,0,0],
    ]

    img = create_image_from_array(skeleton1, skeleton_colors)
    img.save('assets/sprites/skeleton1.png')

    img = create_image_from_array(skeleton2, skeleton_colors)
    img.save('assets/sprites/skeleton2.png')

    print("Enemy sprites generated successfully!")


def generate_tile_sprites():
    """Generate terrain tile sprites."""

    # Grass tile
    grass_colors = {
        0: GRASS_LIGHT,
        1: GRASS_DARK,
    }

    grass = [
        [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
        [0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    img = create_image_from_array(grass, grass_colors)
    img.save('assets/tiles/grass.png')

    # Wall/stone brick tile
    wall_colors = {
        0: WALL_DARK,
        1: WALL_LIGHT,
        2: OUTLINE_BLACK,
    }

    wall = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,1,1,1,2,0,0,0,1,1,1,1,2],
        [2,0,0,0,1,1,1,2,0,0,0,1,1,1,1,2],
        [2,0,0,0,1,1,1,2,0,0,0,1,1,1,1,2],
        [2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2],
        [2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2],
        [2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,1,1,1,1,2,0,0,0,1,1,1,2],
        [2,0,0,0,1,1,1,1,2,0,0,0,1,1,1,2],
        [2,0,0,0,1,1,1,1,2,0,0,0,1,1,1,2],
        [2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
        [2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
        [2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
        [2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ]

    img = create_image_from_array(wall, wall_colors)
    img.save('assets/tiles/wall.png')

    # Water tile
    water_colors = {
        0: WATER_BLUE,
        1: WATER_DARK,
    }

    water = [
        [0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0],
        [0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0],
        [1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,0],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0],
        [0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
        [0,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0],
        [0,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0],
        [0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0],
        [1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,0],
    ]

    img = create_image_from_array(water, water_colors)
    img.save('assets/tiles/water.png')

    # Stone floor tile
    stone_colors = {
        0: STONE_GRAY,
        1: STONE_DARK,
        2: OUTLINE_BLACK,
    }

    stone = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    img = create_image_from_array(stone, stone_colors)
    img.save('assets/tiles/stone.png')

    print("Tile sprites generated successfully!")


def main():
    """Generate all game assets."""
    print("Generating game assets...")
    print()

    # Create directories if they don't exist
    os.makedirs('assets/sprites', exist_ok=True)
    os.makedirs('assets/tiles', exist_ok=True)

    generate_player_sprites()
    generate_sword_sprites()
    generate_enemy_sprites()
    generate_tile_sprites()

    print()
    print("All assets generated successfully!")
    print("Sprites saved to: assets/sprites/")
    print("Tiles saved to: assets/tiles/")


if __name__ == "__main__":
    main()

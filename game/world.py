"""
World management - tile map, rendering, and collision detection.
"""

import pygame
from game.constants import *


class World:
    """Manages the game world, tiles, and collision detection."""

    def __init__(self):
        # Load tile images
        self.tile_images = {
            TILE_GRASS: pygame.image.load('assets/tiles/grass.png'),
            TILE_WALL: pygame.image.load('assets/tiles/wall.png'),
            TILE_WATER: pygame.image.load('assets/tiles/water.png'),
            TILE_STONE: pygame.image.load('assets/tiles/stone.png'),
        }

        # Define the world map (16x12 tiles)
        # 0 = grass, 1 = wall, 2 = water, 3 = stone
        self.tile_map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,2,2,0,0,0,0,2,2,0,0,0,1],
            [1,0,0,0,2,2,0,0,0,0,2,2,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,3,3,3,3,3,3,0,0,0,0,1],
            [1,0,0,0,0,3,3,3,3,3,3,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

        # Tiles that block movement
        self.collision_tiles = {TILE_WALL, TILE_WATER}

    def get_tile(self, x, y):
        """Get the tile type at world coordinates (x, y)."""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)

        if 0 <= tile_y < len(self.tile_map) and 0 <= tile_x < len(self.tile_map[0]):
            return self.tile_map[tile_y][tile_x]
        return TILE_WALL  # Out of bounds = wall

    def is_collidable(self, x, y):
        """Check if the position (x, y) collides with a solid tile."""
        tile = self.get_tile(x, y)
        return tile in self.collision_tiles

    def check_collision(self, rect):
        """
        Check if a rectangle collides with any solid tiles.
        Returns True if collision detected.
        """
        # Check the four corners of the rectangle
        corners = [
            (rect.left, rect.top),
            (rect.right - 1, rect.top),
            (rect.left, rect.bottom - 1),
            (rect.right - 1, rect.bottom - 1),
        ]

        for x, y in corners:
            if self.is_collidable(x, y):
                return True

        return False

    def render(self, surface):
        """Render the world to the given surface."""
        for row in range(TILES_HEIGHT):
            for col in range(TILES_WIDTH):
                tile_type = self.tile_map[row][col]
                tile_image = self.tile_images[tile_type]

                x = col * TILE_SIZE
                y = row * TILE_SIZE

                surface.blit(tile_image, (x, y))

    def get_spawn_positions(self):
        """Get valid spawn positions for player and enemies."""
        positions = []

        # Find all grass tiles
        for row in range(len(self.tile_map)):
            for col in range(len(self.tile_map[0])):
                if self.tile_map[row][col] == TILE_GRASS:
                    x = col * TILE_SIZE + TILE_SIZE // 2
                    y = row * TILE_SIZE + TILE_SIZE // 2
                    positions.append((x, y))

        return positions

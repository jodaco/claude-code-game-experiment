"""
Game constants for the Zelda-style game.
Includes colors, sizes, speeds, and other configuration values.
"""

# Display settings
TILE_SIZE = 32
TILES_WIDTH = 16
TILES_HEIGHT = 12
GAME_WIDTH = TILE_SIZE * TILES_WIDTH  # 512 pixels
GAME_HEIGHT = TILE_SIZE * TILES_HEIGHT  # 384 pixels
SCALE_FACTOR = 2
WINDOW_WIDTH = GAME_WIDTH * SCALE_FACTOR  # 1024 pixels
WINDOW_HEIGHT = GAME_HEIGHT * SCALE_FACTOR  # 768 pixels
FPS = 60

# Player colors
TUNIC_GREEN = (48, 184, 88)
TUNIC_DARK = (32, 120, 64)
HAIR_YELLOW = (248, 200, 88)
HAIR_DARK = (200, 152, 56)
SKIN_PEACH = (248, 176, 136)
SKIN_DARK = (200, 128, 88)

# Enemy colors
SLIME_GREEN = (88, 200, 72)
SLIME_DARK = (56, 152, 40)
SLIME_BLUE = (72, 136, 232)
SKELETON_GRAY = (184, 184, 200)
SKELETON_BONE = (240, 232, 216)
SKELETON_DARK = (120, 120, 136)

# Terrain colors
GRASS_LIGHT = (112, 208, 72)
GRASS_DARK = (72, 160, 56)
STONE_GRAY = (136, 136, 152)
STONE_DARK = (88, 88, 104)
WATER_BLUE = (72, 160, 232)
WATER_DARK = (40, 112, 184)
WALL_DARK = (64, 64, 72)
WALL_LIGHT = (96, 96, 104)

# UI colors
HEART_RED = (232, 56, 56)
HEART_EMPTY = (88, 88, 96)
HEART_OUTLINE = (40, 40, 48)
TEXT_WHITE = (248, 248, 248)
TEXT_BLACK = (24, 24, 32)
BG_BLACK = (0, 0, 0)

# Sword colors
SWORD_BLADE = (192, 192, 208)
SWORD_HANDLE = (136, 88, 56)

# Other colors
TRANSPARENT = (0, 0, 0, 0)
OUTLINE_BLACK = (24, 24, 32)

# Movement speeds (pixels per frame at 60 FPS)
PLAYER_SPEED = 4
SLIME_SPEED = 2
SKELETON_SPEED = 3

# Combat settings
PLAYER_MAX_HEALTH = 12  # 6 hearts = 12 half-hearts
SWORD_DAMAGE = 2  # 1 heart
ENEMY_DAMAGE = 2  # 1 heart
SLIME_HEALTH = 2  # 1 hit to kill
SKELETON_HEALTH = 6  # 3 hits to kill
INVULNERABILITY_TIME = 500  # milliseconds
SWORD_SWING_TIME = 250  # milliseconds

# Animation settings
WALK_ANIMATION_SPEED = 8  # frames per animation frame
SWORD_ANIMATION_SPEED = 5  # frames per animation frame
ENEMY_ANIMATION_SPEED = 15  # frames per animation frame

# Enemy AI settings
SKELETON_CHASE_RANGE = 5 * TILE_SIZE  # 5 tiles
ENEMY_WANDER_CHANGE_FREQ = 120  # frames (2 seconds at 60 FPS)

# Tile types
TILE_GRASS = 0
TILE_WALL = 1
TILE_WATER = 2
TILE_STONE = 3

# Directions
DIR_DOWN = 0
DIR_UP = 1
DIR_LEFT = 2
DIR_RIGHT = 3

# Game states
STATE_TITLE = "title"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

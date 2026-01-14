"""
Player character with WASD movement and sword attack.
"""

import pygame
import math
from game.constants import *
from game.sprites import AnimatedSprite, SwordSlash


class Player(AnimatedSprite):
    """Player character controlled by WASD and mouse."""

    def __init__(self, x, y, world):
        super().__init__(x, y)
        self.world = world

        # Health and combat
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.is_invulnerable = False
        self.invulnerability_timer = 0

        # Movement
        self.speed = PLAYER_SPEED
        self.direction = DIR_DOWN

        # Sword attack
        self.is_attacking = False
        self.attack_cooldown = 0

        # Load player sprites
        self.load_animations()

        # Set initial image and rect
        self.image = self.animation_frames['idle_down'][0]
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)

        self.animation_speed = WALK_ANIMATION_SPEED
        self.set_animation('idle_down')

    def load_animations(self):
        """Load all player animation frames."""
        # Idle animations (single frame)
        self.add_animation('idle_down', [pygame.image.load('assets/sprites/player_down.png')])
        self.add_animation('idle_up', [pygame.image.load('assets/sprites/player_up.png')])
        self.add_animation('idle_left', [pygame.image.load('assets/sprites/player_left.png')])
        self.add_animation('idle_right', [pygame.image.load('assets/sprites/player_right.png')])

        # Walk animations
        self.add_animation('walk_down', [
            pygame.image.load('assets/sprites/player_down.png'),
            pygame.image.load('assets/sprites/player_down_walk1.png'),
            pygame.image.load('assets/sprites/player_down.png'),
            pygame.image.load('assets/sprites/player_down_walk2.png'),
        ])

        self.add_animation('walk_up', [
            pygame.image.load('assets/sprites/player_up.png'),
        ])

        self.add_animation('walk_left', [
            pygame.image.load('assets/sprites/player_left.png'),
        ])

        self.add_animation('walk_right', [
            pygame.image.load('assets/sprites/player_right.png'),
        ])

    def handle_input(self, keys, mouse_buttons, mouse_pos):
        """Handle keyboard and mouse input."""
        # Movement with WASD
        dx = 0
        dy = 0
        moving = False

        if keys[pygame.K_w]:
            dy -= self.speed
            self.direction = DIR_UP
            moving = True

        if keys[pygame.K_s]:
            dy += self.speed
            self.direction = DIR_DOWN
            moving = True

        if keys[pygame.K_a]:
            dx -= self.speed
            self.direction = DIR_LEFT
            moving = True

        if keys[pygame.K_d]:
            dx += self.speed
            self.direction = DIR_RIGHT
            moving = True

        # Update animation based on movement
        if moving:
            if self.direction == DIR_DOWN:
                self.set_animation('walk_down')
            elif self.direction == DIR_UP:
                self.set_animation('walk_up')
            elif self.direction == DIR_LEFT:
                self.set_animation('walk_left')
            elif self.direction == DIR_RIGHT:
                self.set_animation('walk_right')
        else:
            if self.direction == DIR_DOWN:
                self.set_animation('idle_down')
            elif self.direction == DIR_UP:
                self.set_animation('idle_up')
            elif self.direction == DIR_LEFT:
                self.set_animation('idle_left')
            elif self.direction == DIR_RIGHT:
                self.set_animation('idle_right')

        # Move with collision detection
        self.move(dx, dy)

        # Sword attack with left mouse button (swings in facing direction)
        if mouse_buttons[0] and self.attack_cooldown <= 0:  # Left click
            self.attack()

    def move(self, dx, dy):
        """Move the player with collision detection."""
        if dx != 0:
            # Move horizontally
            old_x = self.x
            self.x += dx
            self.rect.x = int(self.x)

            # Check collision
            if self.world.check_collision(self.rect):
                self.x = old_x
                self.rect.x = int(self.x)

        if dy != 0:
            # Move vertically
            old_y = self.y
            self.y += dy
            self.rect.y = int(self.y)

            # Check collision
            if self.world.check_collision(self.rect):
                self.y = old_y
                self.rect.y = int(self.y)

    def attack(self):
        """Create a sword slash in the direction player is facing."""
        # Use the player's current facing direction
        sword_direction = self.direction

        # Calculate sword position (in front of player)
        sword_x = self.x
        sword_y = self.y

        if sword_direction == DIR_RIGHT:
            sword_x += TILE_SIZE
        elif sword_direction == DIR_LEFT:
            sword_x -= TILE_SIZE
        elif sword_direction == DIR_DOWN:
            sword_y += TILE_SIZE
        elif sword_direction == DIR_UP:
            sword_y -= TILE_SIZE

        # Create sword slash sprite
        self.sword_slash = SwordSlash(sword_x, sword_y, sword_direction, self)
        self.is_attacking = True
        self.attack_cooldown = SWORD_SWING_TIME

        return self.sword_slash

    def take_damage(self, damage):
        """Take damage if not invulnerable."""
        if not self.is_invulnerable:
            self.health -= damage
            self.health = max(0, self.health)

            # Start invulnerability
            self.is_invulnerable = True
            self.invulnerability_timer = INVULNERABILITY_TIME

            return True
        return False

    def update(self):
        """Update player state."""
        super().update()

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1000 / FPS  # Convert to milliseconds

        # Update invulnerability
        if self.is_invulnerable:
            self.invulnerability_timer -= 1000 / FPS
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False
                self.invulnerability_timer = 0

    def render(self, surface):
        """Render the player with invulnerability flash effect."""
        # Flash when invulnerable
        if self.is_invulnerable:
            # Flash every 100ms
            if int(self.invulnerability_timer) % 100 < 50:
                return  # Don't draw (creates flashing effect)

        surface.blit(self.image, self.rect)

    def is_alive(self):
        """Check if player is still alive."""
        return self.health > 0

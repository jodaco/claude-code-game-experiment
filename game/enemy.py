"""
Enemy sprites with AI behaviors.
"""

import pygame
import random
import math
from game.constants import *
from game.sprites import AnimatedSprite


class Enemy(AnimatedSprite):
    """Base enemy class."""

    def __init__(self, x, y, world):
        super().__init__(x, y)
        self.world = world
        self.health = 1
        self.max_health = 1
        self.speed = 1
        self.damage = ENEMY_DAMAGE

        # AI state
        self.state = "wander"
        self.wander_timer = 0
        self.wander_dx = 0
        self.wander_dy = 0

    def take_damage(self, damage):
        """Take damage."""
        self.health -= damage
        self.health = max(0, self.health)
        return True

    def is_alive(self):
        """Check if enemy is alive."""
        return self.health > 0

    def move(self, dx, dy):
        """Move with collision detection."""
        if dx != 0:
            old_x = self.x
            self.x += dx
            self.rect.x = int(self.x)

            if self.world.check_collision(self.rect):
                self.x = old_x
                self.rect.x = int(self.x)
                return False

        if dy != 0:
            old_y = self.y
            self.y += dy
            self.rect.y = int(self.y)

            if self.world.check_collision(self.rect):
                self.y = old_y
                self.rect.y = int(self.y)
                return False

        return True

    def update(self):
        """Update enemy. Override in subclasses."""
        super().update()


class Slime(Enemy):
    """Slime enemy that wanders randomly."""

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.health = SLIME_HEALTH
        self.max_health = SLIME_HEALTH
        self.speed = SLIME_SPEED

        # Load animations
        self.add_animation('idle', [
            pygame.image.load('assets/sprites/slime1.png'),
            pygame.image.load('assets/sprites/slime2.png'),
        ])

        self.animation_speed = ENEMY_ANIMATION_SPEED
        self.set_animation('idle')

        self.image = self.animation_frames['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)

        # Initialize wander
        self.change_wander_direction()

    def change_wander_direction(self):
        """Pick a new random direction to wander."""
        angle = random.uniform(0, 2 * math.pi)
        self.wander_dx = math.cos(angle) * self.speed
        self.wander_dy = math.sin(angle) * self.speed
        self.wander_timer = ENEMY_WANDER_CHANGE_FREQ

    def update(self):
        """Update slime behavior."""
        super().update()

        # Wander behavior
        self.wander_timer -= 1

        if self.wander_timer <= 0:
            self.change_wander_direction()

        # Try to move
        success = self.move(self.wander_dx, self.wander_dy)

        # If hit a wall, change direction immediately
        if not success:
            self.change_wander_direction()


class Skeleton(Enemy):
    """Skeleton enemy that chases the player when nearby."""

    def __init__(self, x, y, world, player):
        super().__init__(x, y, world)
        self.player = player
        self.health = SKELETON_HEALTH
        self.max_health = SKELETON_HEALTH
        self.speed = SKELETON_SPEED
        self.chase_range = SKELETON_CHASE_RANGE

        # Load animations
        self.add_animation('idle', [
            pygame.image.load('assets/sprites/skeleton1.png'),
            pygame.image.load('assets/sprites/skeleton2.png'),
        ])

        self.animation_speed = ENEMY_ANIMATION_SPEED
        self.set_animation('idle')

        self.image = self.animation_frames['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)

        # Initialize wander
        self.change_wander_direction()

    def change_wander_direction(self):
        """Pick a new random direction to wander."""
        angle = random.uniform(0, 2 * math.pi)
        self.wander_dx = math.cos(angle) * self.speed
        self.wander_dy = math.sin(angle) * self.speed
        self.wander_timer = ENEMY_WANDER_CHANGE_FREQ

    def get_distance_to_player(self):
        """Calculate distance to player."""
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def update(self):
        """Update skeleton behavior."""
        super().update()

        # Check if player is in chase range
        distance = self.get_distance_to_player()

        if distance < self.chase_range:
            # Chase player
            self.state = "chase"

            # Move toward player
            dx = self.player.x - self.x
            dy = self.player.y - self.y

            # Normalize and apply speed
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                dx = (dx / length) * self.speed
                dy = (dy / length) * self.speed

            self.move(dx, dy)

        else:
            # Wander
            self.state = "wander"
            self.wander_timer -= 1

            if self.wander_timer <= 0:
                self.change_wander_direction()

            success = self.move(self.wander_dx, self.wander_dy)

            if not success:
                self.change_wander_direction()

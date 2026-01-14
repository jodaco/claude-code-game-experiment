"""
Base sprite classes for the game.
"""

import pygame
from game.constants import *


class AnimatedSprite(pygame.sprite.Sprite):
    """Base class for animated sprites."""

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.animation_frames = {}
        self.current_animation = None
        self.animation_index = 0
        self.animation_counter = 0
        self.animation_speed = 10

        # Will be set by subclasses
        self.image = None
        self.rect = None

    def add_animation(self, name, frames):
        """Add an animation with given name and list of frame images."""
        self.animation_frames[name] = frames

    def set_animation(self, name):
        """Set the current animation."""
        if name in self.animation_frames and name != self.current_animation:
            self.current_animation = name
            self.animation_index = 0
            self.animation_counter = 0

    def update_animation(self):
        """Update the animation frame."""
        if self.current_animation and self.current_animation in self.animation_frames:
            frames = self.animation_frames[self.current_animation]

            if len(frames) > 0:
                self.animation_counter += 1

                if self.animation_counter >= self.animation_speed:
                    self.animation_counter = 0
                    self.animation_index = (self.animation_index + 1) % len(frames)

                self.image = frames[self.animation_index]

    def update(self):
        """Update sprite. Override in subclasses."""
        self.update_animation()
        if self.rect:
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)


class SwordSlash(pygame.sprite.Sprite):
    """Sword slash hitbox sprite."""

    def __init__(self, x, y, direction, owner):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.owner = owner  # Player or enemy that created this slash
        self.lifetime = SWORD_SWING_TIME
        self.created_time = pygame.time.get_ticks()
        self.damage = SWORD_DAMAGE

        # Load sword sprite based on direction
        if direction == DIR_DOWN:
            self.image = pygame.image.load('assets/sprites/sword_down.png')
        elif direction == DIR_UP:
            self.image = pygame.image.load('assets/sprites/sword_up.png')
        elif direction == DIR_LEFT:
            self.image = pygame.image.load('assets/sprites/sword_left.png')
        elif direction == DIR_RIGHT:
            self.image = pygame.image.load('assets/sprites/sword_right.png')

        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)

    def update(self):
        """Update sword slash, remove if lifetime expired."""
        current_time = pygame.time.get_ticks()
        if current_time - self.created_time >= self.lifetime:
            self.kill()


class HealthBar(pygame.sprite.Sprite):
    """Health bar display for entities."""

    def __init__(self, entity, width=16, height=2):
        super().__init__()
        self.entity = entity
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

    def update(self):
        """Update health bar position and appearance."""
        # Position above entity
        self.rect.x = int(self.entity.x)
        self.rect.y = int(self.entity.y - 4)

        # Draw health bar
        self.image.fill(HEART_EMPTY)

        if hasattr(self.entity, 'health') and hasattr(self.entity, 'max_health'):
            health_ratio = max(0, self.entity.health / self.entity.max_health)
            health_width = int(self.width * health_ratio)

            if health_width > 0:
                pygame.draw.rect(self.image, HEART_RED, (0, 0, health_width, self.height))

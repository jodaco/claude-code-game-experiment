"""
Combat system - damage calculation, hit detection, and collision handling.
"""

import pygame
import math


class CombatSystem:
    """Manages combat interactions between entities."""

    def __init__(self):
        self.hit_enemies = set()  # Track which enemies have been hit by current attack

    def check_sword_hits(self, sword_slashes, enemies):
        """
        Check if any sword slashes hit enemies.
        Returns list of (enemy, damage) tuples.
        """
        hits = []

        for sword in sword_slashes:
            for enemy in enemies:
                # Check if this enemy was already hit by this sword
                hit_key = (id(sword), id(enemy))

                if hit_key not in self.hit_enemies:
                    # Check collision
                    if self.check_collision(sword.rect, enemy.rect):
                        hits.append((enemy, sword.damage))
                        self.hit_enemies.add(hit_key)

        # Clean up hit tracking for swords that no longer exist
        current_sword_ids = {id(sword) for sword in sword_slashes}
        self.hit_enemies = {
            (sword_id, enemy_id)
            for sword_id, enemy_id in self.hit_enemies
            if sword_id in current_sword_ids
        }

        return hits

    def check_enemy_collisions(self, player, enemies):
        """
        Check if player collides with any enemies (contact damage).
        Returns list of enemies that hit the player.
        """
        hits = []

        for enemy in enemies:
            if self.check_collision(player.rect, enemy.rect):
                hits.append(enemy)

        return hits

    def check_collision(self, rect1, rect2):
        """Check if two rectangles collide."""
        return rect1.colliderect(rect2)

    def check_circle_collision(self, x1, y1, r1, x2, y2, r2):
        """Check if two circles collide."""
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance < (r1 + r2)

    def apply_damage(self, entity, damage):
        """Apply damage to an entity."""
        if hasattr(entity, 'take_damage'):
            return entity.take_damage(damage)
        elif hasattr(entity, 'health'):
            entity.health -= damage
            entity.health = max(0, entity.health)
            return True
        return False

    def is_alive(self, entity):
        """Check if an entity is alive."""
        if hasattr(entity, 'is_alive'):
            return entity.is_alive()
        elif hasattr(entity, 'health'):
            return entity.health > 0
        return True

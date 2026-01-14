"""
Main game engine - game loop, state management, and rendering.
"""

import pygame
import sys
import random
from game.constants import *
from game.world import World
from game.player import Player
from game.enemy import Slime, Skeleton
from game.combat import CombatSystem


class GameEngine:
    """Main game engine managing the game loop and state."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create window
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Zelda-Style Adventure")

        # Create game surface (will be scaled up)
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Game state
        self.state = STATE_TITLE
        self.running = True

        # Game objects
        self.world = None
        self.player = None
        self.enemies = None
        self.sword_slashes = None
        self.combat_system = None

        # Font for UI
        self.font = pygame.font.Font(None, 16)
        self.big_font = pygame.font.Font(None, 32)

    def new_game(self):
        """Start a new game."""
        # Create world
        self.world = World()

        # Get spawn positions
        spawn_positions = self.world.get_spawn_positions()

        # Create player at center
        player_pos = spawn_positions[len(spawn_positions) // 2]
        self.player = Player(player_pos[0], player_pos[1], self.world)

        # Create sprite groups
        self.enemies = pygame.sprite.Group()
        self.sword_slashes = pygame.sprite.Group()

        # Spawn enemies
        self.spawn_enemies(spawn_positions)

        # Create combat system
        self.combat_system = CombatSystem()

        # Set state to playing
        self.state = STATE_PLAYING

    def spawn_enemies(self, spawn_positions):
        """Spawn enemies at random valid positions."""
        # Filter out positions near player
        player_x, player_y = self.player.x, self.player.y
        valid_positions = [
            pos for pos in spawn_positions
            if abs(pos[0] - player_x) > 64 or abs(pos[1] - player_y) > 64
        ]

        # Spawn 2 slimes
        for _ in range(2):
            if valid_positions:
                pos = random.choice(valid_positions)
                valid_positions.remove(pos)
                slime = Slime(pos[0], pos[1], self.world)
                self.enemies.add(slime)

        # Spawn 2 skeletons
        for _ in range(2):
            if valid_positions:
                pos = random.choice(valid_positions)
                valid_positions.remove(pos)
                skeleton = Skeleton(pos[0], pos[1], self.world, self.player)
                self.enemies.add(skeleton)

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle key presses based on game state
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_TITLE:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.new_game()

                elif self.state == STATE_GAME_OVER or self.state == STATE_VICTORY:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_TITLE

                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_TITLE

    def update(self):
        """Update game state."""
        if self.state == STATE_PLAYING:
            # Get input
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            # Scale mouse position to game coordinates
            scaled_mouse_x = mouse_pos[0] / SCALE_FACTOR
            scaled_mouse_y = mouse_pos[1] / SCALE_FACTOR

            # Handle player input
            self.player.handle_input(keys, mouse_buttons, (scaled_mouse_x, scaled_mouse_y))

            # Check if player created a sword slash
            if hasattr(self.player, 'sword_slash') and self.player.sword_slash:
                self.sword_slashes.add(self.player.sword_slash)
                self.player.sword_slash = None

            # Update player
            self.player.update()

            # Update enemies
            self.enemies.update()

            # Update sword slashes
            self.sword_slashes.update()

            # Check combat
            self.check_combat()

            # Check win/lose conditions
            if not self.player.is_alive():
                self.state = STATE_GAME_OVER
            elif len(self.enemies) == 0:
                self.state = STATE_VICTORY

    def check_combat(self):
        """Handle all combat interactions."""
        # Check sword hits on enemies
        hits = self.combat_system.check_sword_hits(self.sword_slashes, self.enemies)

        for enemy, damage in hits:
            self.combat_system.apply_damage(enemy, damage)

            # Remove dead enemies
            if not enemy.is_alive():
                enemy.kill()

        # Check enemy collisions with player
        enemy_hits = self.combat_system.check_enemy_collisions(self.player, self.enemies)

        for enemy in enemy_hits:
            self.combat_system.apply_damage(self.player, enemy.damage)

    def render(self):
        """Render the game."""
        if self.state == STATE_TITLE:
            self.render_title_screen()

        elif self.state == STATE_PLAYING:
            self.render_game()

        elif self.state == STATE_GAME_OVER:
            self.render_game_over()

        elif self.state == STATE_VICTORY:
            self.render_victory()

        # Scale game surface to window
        scaled_surface = pygame.transform.scale(self.game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def render_title_screen(self):
        """Render the title screen."""
        self.game_surface.fill(BG_BLACK)

        # Title
        title_text = self.big_font.render("ZELDA ADVENTURE", True, TEXT_WHITE)
        title_rect = title_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 30))
        self.game_surface.blit(title_text, title_rect)

        # Instructions
        start_text = self.font.render("Press SPACE to Start", True, TEXT_WHITE)
        start_rect = start_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 10))
        self.game_surface.blit(start_text, start_rect)

        controls_text = self.font.render("WASD to move, Mouse to attack", True, TEXT_WHITE)
        controls_rect = controls_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 30))
        self.game_surface.blit(controls_text, controls_rect)

    def render_game(self):
        """Render the main game."""
        # Clear screen
        self.game_surface.fill(BG_BLACK)

        # Render world
        self.world.render(self.game_surface)

        # Render enemies
        for enemy in self.enemies:
            self.game_surface.blit(enemy.image, enemy.rect)

        # Render player
        self.player.render(self.game_surface)

        # Render sword slashes
        for slash in self.sword_slashes:
            self.game_surface.blit(slash.image, slash.rect)

        # Render UI
        self.render_ui()

    def render_ui(self):
        """Render UI elements (hearts, enemy count, etc)."""
        # Render hearts
        heart_x = 8
        heart_y = 8

        full_hearts = self.player.health // 2
        half_heart = self.player.health % 2

        for i in range(self.player.max_health // 2):
            if i < full_hearts:
                # Full heart
                pygame.draw.rect(self.game_surface, HEART_OUTLINE, (heart_x, heart_y, 8, 7))
                pygame.draw.rect(self.game_surface, HEART_RED, (heart_x + 1, heart_y + 1, 6, 5))
            elif i == full_hearts and half_heart:
                # Half heart
                pygame.draw.rect(self.game_surface, HEART_OUTLINE, (heart_x, heart_y, 8, 7))
                pygame.draw.rect(self.game_surface, HEART_RED, (heart_x + 1, heart_y + 1, 3, 5))
                pygame.draw.rect(self.game_surface, HEART_EMPTY, (heart_x + 4, heart_y + 1, 3, 5))
            else:
                # Empty heart
                pygame.draw.rect(self.game_surface, HEART_OUTLINE, (heart_x, heart_y, 8, 7))
                pygame.draw.rect(self.game_surface, HEART_EMPTY, (heart_x + 1, heart_y + 1, 6, 5))

            heart_x += 10

        # Render enemy count
        enemy_text = self.font.render(f"Enemies: {len(self.enemies)}", True, TEXT_WHITE)
        self.game_surface.blit(enemy_text, (8, GAME_HEIGHT - 20))

    def render_game_over(self):
        """Render game over screen."""
        # Render the game in background
        self.render_game()

        # Dark overlay
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BG_BLACK)
        self.game_surface.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.big_font.render("GAME OVER", True, HEART_RED)
        game_over_rect = game_over_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 20))
        self.game_surface.blit(game_over_text, game_over_rect)

        # Restart instructions
        restart_text = self.font.render("Press SPACE to Restart", True, TEXT_WHITE)
        restart_rect = restart_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 10))
        self.game_surface.blit(restart_text, restart_rect)

        menu_text = self.font.render("Press ESC for Menu", True, TEXT_WHITE)
        menu_rect = menu_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 30))
        self.game_surface.blit(menu_text, menu_rect)

    def render_victory(self):
        """Render victory screen."""
        # Render the game in background
        self.render_game()

        # Dark overlay
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BG_BLACK)
        self.game_surface.blit(overlay, (0, 0))

        # Victory text
        victory_text = self.big_font.render("VICTORY!", True, TUNIC_GREEN)
        victory_rect = victory_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 20))
        self.game_surface.blit(victory_text, victory_rect)

        # Restart instructions
        restart_text = self.font.render("Press SPACE to Play Again", True, TEXT_WHITE)
        restart_rect = restart_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 10))
        self.game_surface.blit(restart_text, restart_rect)

        menu_text = self.font.render("Press ESC for Menu", True, TEXT_WHITE)
        menu_rect = menu_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 30))
        self.game_surface.blit(menu_text, menu_rect)

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

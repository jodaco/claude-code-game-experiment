#!/usr/bin/env python3
"""
Zelda-Style Adventure Game
A simple action-adventure game inspired by classic Zelda titles.

Controls:
- WASD: Move the player
- Left Mouse Click: Swing sword toward mouse cursor
- ESC: Return to menu
- SPACE: Start game / Restart

Features:
- Pixel art graphics
- Tile-based world
- Enemy AI (wandering slimes, chasing skeletons)
- Combat system with sword attacks
- Health system with hearts
"""

from game.engine import GameEngine


def main():
    """Main entry point for the game."""
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()

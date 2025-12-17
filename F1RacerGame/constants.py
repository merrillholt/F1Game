"""
Game constants and configuration values.
"""

from typing import Tuple

# Display settings
DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 600
FPS = 60

# UI Layout
BUTTON_START_X = 75
NEW_GAME_Y = 400
QUIT_Y = 460
BUTTON_WIDTH = 242
BUTTON_HEIGHT = 50

# Game physics
CAR_SPEED = 10
OBSTACLE_INITIAL_SPEED = 5
OBSTACLE_SPEED_INCREMENT = 1
OBSTACLE_START_Y = -600

# Car positioning
CAR_START_X_RATIO = 0.4  # 40% of screen width
CAR_START_Y_RATIO = 0.6  # 60% of screen height

# Collision detection tolerances
COLLISION_Y_TOLERANCE = 15
COLLISION_X_TOLERANCE = 5

# Colors (RGB tuples)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
RED_LIGHT: Tuple[int, int, int] = (255, 21, 21)
LIGHT_BLUE: Tuple[int, int, int] = (30, 139, 195)
GRAY: Tuple[int, int, int] = (112, 128, 144)
GREEN: Tuple[int, int, int] = (0, 255, 0)
GREEN_LIGHT: Tuple[int, int, int] = (51, 255, 51)
BLUE: Tuple[int, int, int] = (0, 0, 255)

# Asset file names
ASSET_FILES = {
    "car": "car.png",
    "car_left": "car_left.png",
    "car_right": "car_right.png",
    "obstacle": "obstacle.png",
    "texture": "texture.png",
    "background": "background.png",
    "background_still": "background_inv.png",
    "intro_1": "intro1.wav",
    "intro_2": "intro2.wav",
    "crash_sound": "car_crash.wav",
    "ignition": "ignition.wav",
    "running": "running.wav",
    "high_score": "high_score.txt",
}

# Font settings
LARGE_FONT_SIZE = 50
MEDIUM_FONT_SIZE = 40
SMALL_FONT_SIZE = 25
BUTTON_FONT_SIZE = 20
DEFAULT_FONT = "freesansbold.ttf"

# Animation and timing
COUNTDOWN_DELAY = 0.75
TITLE_ANIMATION_SPEED = 1.5
TEXTURE_OFFSET = 400

# Game difficulty settings
DIFFICULTY_LEVELS = {
    "easy": {"obstacle_speed": 3, "speed_increment": 0.5, "spawn_rate": 1.0},
    "normal": {"obstacle_speed": 5, "speed_increment": 1.0, "spawn_rate": 1.0},
    "hard": {"obstacle_speed": 7, "speed_increment": 1.5, "spawn_rate": 0.8},
}

# Power-up settings
POWERUP_SPAWN_CHANCE = 0.1  # 10% chance per obstacle
POWERUP_DURATION = 5.0  # seconds
POWERUP_TYPES = {
    "shield": {"color": BLUE, "duration": 3.0},
    "slow_motion": {"color": GREEN, "duration": 5.0},
    "speed_boost": {"color": RED, "duration": 2.0},
}

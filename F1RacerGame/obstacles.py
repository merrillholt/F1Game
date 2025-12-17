"""
Multiple obstacle types for F1 Racing Game.
"""

import pygame
import random
from typing import List, Optional, Any
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, OBSTACLE_START_Y
from logger import log_game_event


class ObstacleType:
    """Defines properties for different obstacle types."""

    def __init__(
        self,
        name: str,
        width: int,
        height: int,
        speed_modifier: float,
        score_value: int,
        color: tuple,
        spawn_weight: float = 1.0,
    ):
        """Initialize obstacle type.

        Args:
            name: Obstacle type name
            width: Width in pixels
            height: Height in pixels
            speed_modifier: Speed multiplier (1.0 = normal)
            score_value: Points for dodging this obstacle
            color: RGB color tuple
            spawn_weight: Relative spawn frequency (higher = more common)
        """
        self.name = name
        self.width = width
        self.height = height
        self.speed_modifier = speed_modifier
        self.score_value = score_value
        self.color = color
        self.spawn_weight = spawn_weight


# Define obstacle types
OBSTACLE_TYPES = {
    "normal": ObstacleType(
        name="Normal Car",
        width=46,
        height=90,
        speed_modifier=1.0,
        score_value=1,
        color=(255, 0, 0),  # Red
        spawn_weight=5.0,
    ),
    "truck": ObstacleType(
        name="Truck",
        width=50,
        height=120,
        speed_modifier=0.8,
        score_value=2,
        color=(139, 69, 19),  # Brown
        spawn_weight=2.0,
    ),
    "sports_car": ObstacleType(
        name="Sports Car",
        width=42,
        height=80,
        speed_modifier=1.3,
        score_value=3,
        color=(255, 215, 0),  # Gold
        spawn_weight=1.5,
    ),
    "motorcycle": ObstacleType(
        name="Motorcycle",
        width=25,
        height=60,
        speed_modifier=1.5,
        score_value=2,
        color=(128, 0, 128),  # Purple
        spawn_weight=1.0,
    ),
    "bus": ObstacleType(
        name="Bus",
        width=55,
        height=150,
        speed_modifier=0.6,
        score_value=4,
        color=(0, 100, 0),  # Dark Green
        spawn_weight=0.5,
    ),
}


class MultiObstacle:
    """Enhanced obstacle with multiple types."""

    def __init__(self, assets, base_speed: float, obstacle_type: Optional[str] = None):
        """Initialize multi-type obstacle.

        Args:
            assets: AssetManager instance
            base_speed: Base speed for obstacle
            obstacle_type: Specific type to use (random if None)
        """
        self.assets = assets

        # Select obstacle type
        if obstacle_type and obstacle_type in OBSTACLE_TYPES:
            self.obstacle_type = OBSTACLE_TYPES[obstacle_type]
        else:
            self.obstacle_type = self._select_random_type()

        # Position
        margin = 8
        max_x = DISPLAY_WIDTH - self.obstacle_type.width - margin
        self.x = random.randrange(margin, max(margin + 1, max_x))
        self.y: float = float(OBSTACLE_START_Y)

        # Speed with type modifier
        self.base_speed = base_speed
        self.speed = base_speed * self.obstacle_type.speed_modifier

        log_game_event(
            "Obstacle spawned",
            {"type": self.obstacle_type.name, "position": (self.x, self.y), "speed": self.speed},
        )

    def _select_random_type(self) -> ObstacleType:
        """Select random obstacle type based on spawn weights."""
        types = list(OBSTACLE_TYPES.values())
        weights = [t.spawn_weight for t in types]

        return random.choices(types, weights=weights)[0]

    def update(self) -> bool:
        """Update obstacle position.

        Returns:
            True if obstacle passed the screen
        """
        self.y += self.speed
        if self.y > DISPLAY_HEIGHT:
            self.reset()
            return True
        return False

    def reset(self) -> None:
        """Reset obstacle to top of screen with new type."""
        # Select new type
        self.obstacle_type = self._select_random_type()

        # Reset position
        margin = 8
        max_x = DISPLAY_WIDTH - self.obstacle_type.width - margin
        self.x = random.randrange(margin, max(margin + 1, max_x))
        self.y = 0 - self.obstacle_type.height

        # Update speed with new type modifier
        self.speed = self.base_speed * self.obstacle_type.speed_modifier

        log_game_event(
            "Obstacle reset",
            {"type": self.obstacle_type.name, "position": (self.x, self.y), "speed": self.speed},
        )

    def render(self, display) -> None:
        """Render obstacle on screen."""
        # Draw filled rectangle
        pygame.draw.rect(
            display,
            self.obstacle_type.color,
            (self.x, self.y, self.obstacle_type.width, self.obstacle_type.height),
        )

        # Draw border
        pygame.draw.rect(
            display,
            (255, 255, 255),
            (self.x, self.y, self.obstacle_type.width, self.obstacle_type.height),
            2,
        )

    def check_collision(self, car: Any) -> bool:
        """Check collision with car.

        Args:
            car: Car object to check collision with

        Returns:
            True if collision detected
        """
        tolerance_y = 15
        tolerance_x = 5

        return bool(
            car.y < self.y + self.obstacle_type.height - tolerance_y
            and car.x > self.x - self.assets.car_width - tolerance_x
            and car.x < self.x + self.obstacle_type.width - tolerance_x
        )

    def get_score_value(self) -> int:
        """Get score value for dodging this obstacle.

        Returns:
            Score points
        """
        return self.obstacle_type.score_value

    def get_width(self) -> int:
        """Get obstacle width."""
        return self.obstacle_type.width

    def get_height(self) -> int:
        """Get obstacle height."""
        return self.obstacle_type.height

    def get_type_name(self) -> str:
        """Get obstacle type name."""
        return self.obstacle_type.name


class ObstacleManager:
    """Manages multiple obstacles on screen."""

    def __init__(self, max_obstacles: int = 3):
        """Initialize obstacle manager.

        Args:
            max_obstacles: Maximum number of obstacles on screen
        """
        self.max_obstacles = max_obstacles
        self.obstacles: List[MultiObstacle] = []
        self.spawn_timer = 0
        self.spawn_delay = 120  # Frames between spawns

    def update(self, base_speed: float, car) -> int:
        """Update all obstacles.

        Args:
            base_speed: Base speed for new obstacles
            car: Car object for collision checking

        Returns:
            Score points earned from dodged obstacles
        """
        score_earned = 0

        # Update existing obstacles
        for obstacle in self.obstacles[:]:  # Use slice copy
            if obstacle.update():
                score_earned += obstacle.get_score_value()
                self.obstacles.remove(obstacle)

        # Spawn new obstacles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay and len(self.obstacles) < self.max_obstacles:

            new_obstacle = MultiObstacle(car.assets, base_speed)
            self.obstacles.append(new_obstacle)
            self.spawn_timer = 0

        return score_earned

    def render(self, display) -> None:
        """Render all obstacles."""
        for obstacle in self.obstacles:
            obstacle.render(display)

    def check_collisions(self, car) -> bool:
        """Check collisions with car.

        Args:
            car: Car object

        Returns:
            True if any collision detected
        """
        return any(obstacle.check_collision(car) for obstacle in self.obstacles)

    def clear_all(self) -> None:
        """Clear all obstacles."""
        self.obstacles.clear()
        self.spawn_timer = 0

    def get_obstacles(self) -> List[MultiObstacle]:
        """Get list of current obstacles."""
        return self.obstacles.copy()

    def set_spawn_delay(self, delay: int) -> None:
        """Set spawn delay between obstacles.

        Args:
            delay: Delay in frames
        """
        self.spawn_delay = delay

    def set_max_obstacles(self, max_count: int) -> None:
        """Set maximum number of obstacles.

        Args:
            max_count: Maximum obstacle count
        """
        self.max_obstacles = max_count


# Global obstacle manager
obstacle_manager = ObstacleManager()

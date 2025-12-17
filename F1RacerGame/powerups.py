"""
Power-up system for F1 Racing Game.
"""

import random
import time
from typing import Dict, Any
from constants import (
    POWERUP_SPAWN_CHANCE,
    POWERUP_DURATION,
    POWERUP_TYPES,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
)
from logger import log_game_event


class PowerUp:
    """Individual power-up item."""

    def __init__(self, x: float, y: float, powerup_type: str):
        """Initialize power-up.

        Args:
            x: X position
            y: Y position
            powerup_type: Type of power-up
        """
        self.x = x
        self.y = y
        self.type = powerup_type
        self.width = 30
        self.height = 30
        self.speed = 3
        self.collected = False

        # Get properties from configuration
        self.properties = POWERUP_TYPES.get(powerup_type, POWERUP_TYPES["shield"])

    def update(self) -> bool:
        """Update power-up position.

        Returns:
            True if power-up should be removed (went off screen)
        """
        if self.collected:
            return True

        self.y += self.speed
        return self.y > DISPLAY_HEIGHT

    def check_collision(
        self, car_x: float, car_y: float, car_width: float, car_height: float
    ) -> bool:
        """Check collision with car.

        Args:
            car_x: Car X position
            car_y: Car Y position
            car_width: Car width
            car_height: Car height

        Returns:
            True if collision detected
        """
        if self.collected:
            return False

        return (
            car_x < self.x + self.width
            and car_x + car_width > self.x
            and car_y < self.y + self.height
            and car_y + car_height > self.y
        )

    def collect(self) -> Dict[str, Any]:
        """Mark power-up as collected and return its properties.

        Returns:
            Power-up properties dictionary
        """
        self.collected = True
        log_game_event("Power-up collected", {"type": self.type, "position": (self.x, self.y)})
        return self.properties.copy()


class ActivePowerUp:
    """An active power-up effect."""

    def __init__(self, powerup_type: str, duration: float):
        """Initialize active power-up.

        Args:
            powerup_type: Type of power-up
            duration: Duration in seconds
        """
        self.type = powerup_type
        self.duration = duration
        self.start_time = time.time()
        self.properties = POWERUP_TYPES.get(powerup_type, {})

    def is_expired(self) -> bool:
        """Check if power-up effect has expired.

        Returns:
            True if expired
        """
        return time.time() - self.start_time >= self.duration

    def get_remaining_time(self) -> float:
        """Get remaining time for this power-up.

        Returns:
            Remaining time in seconds
        """
        elapsed = time.time() - self.start_time
        return max(0, self.duration - elapsed)


class PowerUpManager:
    """Manages power-up spawning and active effects."""

    def __init__(self):
        """Initialize power-up manager."""
        self.powerups = []  # List of PowerUp objects
        self.active_powerups = []  # List of ActivePowerUp objects
        self.spawn_chance = POWERUP_SPAWN_CHANCE

    def update(self, car_x: float, car_y: float, car_width: float, car_height: float) -> None:
        """Update all power-ups and check for collisions.

        Args:
            car_x: Car X position
            car_y: Car Y position
            car_width: Car width
            car_height: Car height
        """
        # Update power-ups and remove expired ones
        self.powerups = [p for p in self.powerups if not p.update()]

        # Check collisions and collect power-ups
        for powerup in self.powerups[:]:  # Use slice copy to allow removal during iteration
            if powerup.check_collision(car_x, car_y, car_width, car_height):
                properties = powerup.collect()
                self.activate_powerup(powerup.type, properties.get("duration", POWERUP_DURATION))
                self.powerups.remove(powerup)

        # Update active power-ups and remove expired ones
        self.active_powerups = [p for p in self.active_powerups if not p.is_expired()]

    def spawn_powerup(self, obstacle_x: float, obstacle_y: float) -> None:
        """Possibly spawn a power-up when an obstacle is dodged.

        Args:
            obstacle_x: X position of dodged obstacle
            obstacle_y: Y position of dodged obstacle
        """
        if random.random() < self.spawn_chance:
            # Random power-up type
            powerup_type = random.choice(list(POWERUP_TYPES.keys()))

            # Spawn near the obstacle position
            x = obstacle_x + random.randint(-20, 20)
            x = max(0, min(x, DISPLAY_WIDTH - 30))  # Keep in bounds

            powerup = PowerUp(x, obstacle_y, powerup_type)
            self.powerups.append(powerup)

            log_game_event("Power-up spawned", {"type": powerup_type, "position": (x, obstacle_y)})

    def activate_powerup(self, powerup_type: str, duration: float) -> None:
        """Activate a power-up effect.

        Args:
            powerup_type: Type of power-up
            duration: Duration in seconds
        """
        # Remove existing power-up of same type
        self.active_powerups = [p for p in self.active_powerups if p.type != powerup_type]

        # Add new active power-up
        active_powerup = ActivePowerUp(powerup_type, duration)
        self.active_powerups.append(active_powerup)

        log_game_event("Power-up activated", {"type": powerup_type, "duration": duration})

    def has_active_powerup(self, powerup_type: str) -> bool:
        """Check if a specific power-up is currently active.

        Args:
            powerup_type: Type of power-up to check

        Returns:
            True if power-up is active
        """
        return any(p.type == powerup_type for p in self.active_powerups)

    def get_active_powerups(self) -> list:
        """Get list of currently active power-ups.

        Returns:
            List of ActivePowerUp objects
        """
        return self.active_powerups.copy()

    def get_powerups(self) -> list:
        """Get list of power-up items on screen.

        Returns:
            List of PowerUp objects
        """
        return self.powerups.copy()

    def clear_all(self) -> None:
        """Clear all power-ups and active effects."""
        self.powerups.clear()
        self.active_powerups.clear()
        log_game_event("All power-ups cleared")

    def get_speed_multiplier(self) -> float:
        """Get speed multiplier based on active power-ups.

        Returns:
            Speed multiplier (1.0 = normal speed)
        """
        if self.has_active_powerup("slow_motion"):
            return 0.5
        elif self.has_active_powerup("speed_boost"):
            return 1.5
        return 1.0

    def is_shielded(self) -> bool:
        """Check if player is currently shielded.

        Returns:
            True if shield is active
        """
        return self.has_active_powerup("shield")


# Global power-up manager instance
powerup_manager = PowerUpManager()

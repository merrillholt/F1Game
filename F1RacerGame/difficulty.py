"""
Difficulty management system for F1 Racing Game.
"""

from typing import Dict, Any, Optional
from constants import DIFFICULTY_LEVELS
from logger import log_info, log_game_event


class DifficultyManager:
    """Manages game difficulty settings and adjustments."""

    def __init__(self, initial_difficulty: str = "normal"):
        """Initialize difficulty manager.

        Args:
            initial_difficulty: Starting difficulty level
        """
        self.current_difficulty = initial_difficulty
        self.settings = DIFFICULTY_LEVELS[initial_difficulty].copy()
        log_info(f"Initialized difficulty manager with {initial_difficulty} difficulty")

    def set_difficulty(self, difficulty: str) -> bool:
        """Set game difficulty.

        Args:
            difficulty: Difficulty level name

        Returns:
            True if difficulty was set successfully
        """
        if difficulty not in DIFFICULTY_LEVELS:
            return False

        old_difficulty = self.current_difficulty
        self.current_difficulty = difficulty
        self.settings = DIFFICULTY_LEVELS[difficulty].copy()

        log_game_event(
            "Difficulty changed",
            {"from": old_difficulty, "to": difficulty, "settings": self.settings},
        )

        return True

    def get_difficulty(self) -> str:
        """Get current difficulty level.

        Returns:
            Current difficulty name
        """
        return self.current_difficulty

    def get_obstacle_speed(self) -> float:
        """Get obstacle speed for current difficulty.

        Returns:
            Obstacle speed value
        """
        return self.settings["obstacle_speed"]

    def get_speed_increment(self) -> float:
        """Get speed increment for current difficulty.

        Returns:
            Speed increment value
        """
        return self.settings["speed_increment"]

    def get_spawn_rate(self) -> float:
        """Get spawn rate multiplier for current difficulty.

        Returns:
            Spawn rate multiplier (1.0 = normal)
        """
        return self.settings["spawn_rate"]

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings for current difficulty.

        Returns:
            Dictionary of all difficulty settings
        """
        return self.settings.copy()

    def get_available_difficulties(self) -> list:
        """Get list of available difficulty levels.

        Returns:
            List of difficulty names
        """
        return list(DIFFICULTY_LEVELS.keys())

    def get_difficulty_description(self, difficulty: Optional[str] = None) -> str:
        """Get description of a difficulty level.

        Args:
            difficulty: Difficulty to describe (current if None)

        Returns:
            Human-readable difficulty description
        """
        if difficulty is None:
            difficulty = self.current_difficulty

        descriptions = {
            "easy": "Slower obstacles, gentler speed increases. Perfect for beginners!",
            "normal": "Balanced gameplay with moderate challenge. The classic experience.",
            "hard": "Fast obstacles and quick speed increases. For experienced players!",
        }

        return descriptions.get(difficulty, "Unknown difficulty level")

    def adjust_for_score(self, score: int) -> None:
        """Dynamically adjust difficulty based on player score.

        Args:
            score: Current player score
        """
        # Progressive difficulty scaling
        if score > 50 and self.current_difficulty == "easy":
            log_game_event(
                "Auto-adjusting difficulty up", {"score": score, "reason": "good_performance"}
            )
            # Don't auto-change difficulty, just log for analytics

        # Could implement adaptive difficulty here
        # For now, just log performance milestones
        milestones = [10, 25, 50, 100, 200]
        if score in milestones:
            log_game_event(
                "Score milestone reached",
                {"score": score, "difficulty": self.current_difficulty, "settings": self.settings},
            )


# Global difficulty manager instance
difficulty_manager = DifficultyManager()

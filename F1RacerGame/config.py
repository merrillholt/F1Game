"""
Configuration management for F1 Racing Game.
Handles loading and saving game settings.
"""

import json
import os
from typing import Dict, Any, Optional
from constants import DIFFICULTY_LEVELS


class GameConfig:
    """Manages game configuration settings."""

    def __init__(self, config_file: str = "game_config.json"):
        """Initialize configuration manager.

        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_path, config_file)

        # Default configuration
        self.default_config = {
            "graphics": {
                "display_width": 400,
                "display_height": 600,
                "fps": 60,
                "fullscreen": False,
            },
            "audio": {
                "master_volume": 0.7,
                "music_volume": 0.5,
                "sound_effects_volume": 0.8,
                "mute": False,
            },
            "gameplay": {
                "difficulty": "normal",
                "show_fps": False,
                "auto_pause_on_focus_loss": True,
                "enable_powerups": True,
            },
            "controls": {
                "left_key": "a",
                "right_key": "d",
                "left_arrow": True,
                "right_arrow": True,
                "pause_key": "space",
                "quit_key": "escape",
            },
            "debug": {
                "show_collision_boxes": False,
                "show_coordinates": False,
                "enable_dev_mode": False,
            },
        }

        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.

        Returns:
            Configuration dictionary
        """
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)

            # Merge with defaults to handle missing keys
            return self._merge_configs(self.default_config, config)

        except (FileNotFoundError, json.JSONDecodeError):
            # Create default config file
            self.save_config(self.default_config)
            return self.default_config.copy()

    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file.

        Args:
            config: Configuration to save (uses current if None)

        Returns:
            True if successful, False otherwise
        """
        try:
            config_to_save = config or self.config
            with open(self.config_path, "w") as f:
                json.dump(config_to_save, f, indent=4)
            return True
        except IOError:
            return False

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key_path: Period-separated path (e.g., "graphics.fps")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key_path.split(".")
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation.

        Args:
            key_path: Period-separated path (e.g., "graphics.fps")
            value: Value to set
        """
        keys = key_path.split(".")
        config = self.config

        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        # Set the value
        config[keys[-1]] = value

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = self.default_config.copy()
        self.save_config()

    def get_difficulty_settings(self) -> Dict[str, Any]:
        """Get current difficulty settings.

        Returns:
            Difficulty configuration dictionary
        """
        difficulty = self.get("gameplay.difficulty", "normal")
        return DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS["normal"])

    def validate_config(self) -> bool:
        """Validate current configuration.

        Returns:
            True if configuration is valid
        """
        # Check required sections
        required_sections = ["graphics", "audio", "gameplay", "controls"]
        for section in required_sections:
            if section not in self.config:
                return False

        # Validate difficulty
        difficulty = self.get("gameplay.difficulty")
        if difficulty not in DIFFICULTY_LEVELS:
            return False

        # Validate numeric ranges
        fps = self.get("graphics.fps")
        if not isinstance(fps, int) or fps < 30 or fps > 144:
            return False

        # Validate volume levels
        for volume_key in ["master_volume", "music_volume", "sound_effects_volume"]:
            volume = self.get(f"audio.{volume_key}")
            if not isinstance(volume, (int, float)) or volume < 0.0 or volume > 1.0:
                return False

        return True

    def _merge_configs(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with default config.

        Args:
            default: Default configuration
            loaded: Loaded configuration

        Returns:
            Merged configuration
        """
        result = default.copy()

        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result


# Global configuration instance
game_config = GameConfig()

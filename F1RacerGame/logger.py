"""
Logging configuration for F1 Racing Game.
Provides structured logging with different levels and output formats.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class GameLogger:
    """Manages game logging with multiple handlers and formatters."""

    def __init__(self, name: str = "F1Game", log_level: str = "INFO"):
        """Initialize the game logger.

        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up logging handlers for console and file output."""
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)

        # File handler for all logs
        log_file = os.path.join(log_dir, f"game_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)

        # Error file handler
        error_file = os.path.join(log_dir, f"errors_{datetime.now().strftime('%Y%m%d')}.log")
        error_handler = logging.FileHandler(error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)

        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, exception: Optional[Exception] = None, **kwargs) -> None:
        """Log error message with optional exception details."""
        if exception:
            self.logger.error(f"{message}: {str(exception)}", exc_info=True, **kwargs)
        else:
            self.logger.error(message, **kwargs)

    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs) -> None:
        """Log critical message with optional exception details."""
        if exception:
            self.logger.critical(f"{message}: {str(exception)}", exc_info=True, **kwargs)
        else:
            self.logger.critical(message, **kwargs)

    def game_event(self, event: str, details: Optional[dict] = None) -> None:
        """Log game-specific events with structured data.

        Args:
            event: Event name
            details: Additional event details
        """
        details_str = f" - {details}" if details else ""
        self.info(f"GAME_EVENT: {event}{details_str}")

    def performance(self, metric: str, value: float, unit: str = "") -> None:
        """Log performance metrics.

        Args:
            metric: Metric name
            value: Metric value
            unit: Unit of measurement
        """
        unit_str = f" {unit}" if unit else ""
        self.debug(f"PERFORMANCE: {metric} = {value}{unit_str}")

    def collision(self, car_pos: tuple, obstacle_pos: tuple, speed: float) -> None:
        """Log collision events with game state details.

        Args:
            car_pos: Car position (x, y)
            obstacle_pos: Obstacle position (x, y)
            speed: Current game speed
        """
        self.info(f"COLLISION: Car at {car_pos}, Obstacle at {obstacle_pos}, Speed: {speed}")

    def score_update(self, score: int, high_score: int, speed: float) -> None:
        """Log score updates.

        Args:
            score: Current score
            high_score: Current high score
            speed: Current game speed
        """
        self.debug(f"SCORE: {score} (High: {high_score}) Speed: {speed}")

    def asset_load(self, asset_type: str, asset_name: str, success: bool = True) -> None:
        """Log asset loading events.

        Args:
            asset_type: Type of asset (image, sound, etc.)
            asset_name: Name/path of asset
            success: Whether loading was successful
        """
        status = "SUCCESS" if success else "FAILED"
        self.debug(f"ASSET_LOAD: {asset_type} '{asset_name}' - {status}")

    def state_change(self, from_state: str, to_state: str) -> None:
        """Log game state changes.

        Args:
            from_state: Previous state
            to_state: New state
        """
        self.info(f"STATE_CHANGE: {from_state} -> {to_state}")


# Global logger instance
game_logger = GameLogger()


# Convenience functions for easy access
def log_debug(message: str, **kwargs) -> None:
    """Log debug message."""
    game_logger.debug(message, **kwargs)


def log_info(message: str, **kwargs) -> None:
    """Log info message."""
    game_logger.info(message, **kwargs)


def log_warning(message: str, **kwargs) -> None:
    """Log warning message."""
    game_logger.warning(message, **kwargs)


def log_error(message: str, exception: Optional[Exception] = None, **kwargs) -> None:
    """Log error message."""
    game_logger.error(message, exception, **kwargs)


def log_critical(message: str, exception: Optional[Exception] = None, **kwargs) -> None:
    """Log critical message."""
    game_logger.critical(message, exception, **kwargs)


def log_game_event(event: str, details: Optional[dict] = None) -> None:
    """Log game event."""
    game_logger.game_event(event, details)


def log_performance(metric: str, value: float, unit: str = "") -> None:
    """Log performance metric."""
    game_logger.performance(metric, value, unit)


def log_collision(car_pos: tuple, obstacle_pos: tuple, speed: float) -> None:
    """Log collision event."""
    game_logger.collision(car_pos, obstacle_pos, speed)


def log_score_update(score: int, high_score: int, speed: float) -> None:
    """Log score update."""
    game_logger.score_update(score, high_score, speed)


def log_asset_load(asset_type: str, asset_name: str, success: bool = True) -> None:
    """Log asset loading."""
    game_logger.asset_load(asset_type, asset_name, success)


def log_state_change(from_state: str, to_state: str) -> None:
    """Log state change."""
    game_logger.state_change(from_state, to_state)

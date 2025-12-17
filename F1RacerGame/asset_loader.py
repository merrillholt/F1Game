"""
Asset loading abstraction layer for F1 Racing Game.
Provides a clean interface for loading pygame assets that's easy to mock in tests.
"""

import pygame
from typing import Tuple, Any


class ImageData:
    """Container for image data and metadata."""

    def __init__(self, image: Any, size: Tuple[int, int]):
        """Initialize image data.

        Args:
            image: Pygame surface object
            size: Width and height tuple
        """
        self.image = image
        self.width = size[0]
        self.height = size[1]


class AssetLoader:
    """Handles loading of pygame assets."""

    @staticmethod
    def load_image(path: str) -> ImageData:
        """Load an image file and return image data.

        Args:
            path: Path to image file

        Returns:
            ImageData object containing image and dimensions
        """
        image = pygame.image.load(path)
        rect = image.get_rect()
        size = rect.size
        return ImageData(image, size)

    @staticmethod
    def load_sound(path: str) -> Any:
        """Load a sound file.

        Args:
            path: Path to sound file

        Returns:
            Pygame Sound object
        """
        return pygame.mixer.Sound(path)

    @staticmethod
    def load_music(path: str) -> None:
        """Load a music file.

        Args:
            path: Path to music file
        """
        pygame.mixer.music.load(path)


# Global instance
asset_loader = AssetLoader()

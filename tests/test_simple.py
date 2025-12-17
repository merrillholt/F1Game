import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the F1RacerGame directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "F1RacerGame"))

# Mock pygame before importing our modules
pygame_mock = MagicMock()
pygame_mock.mixer = MagicMock()
pygame_mock.mixer.Sound = MagicMock()
pygame_mock.mixer.music = MagicMock()
pygame_mock.image = MagicMock()
pygame_mock.font = MagicMock()
pygame_mock.display = MagicMock()
pygame_mock.time = MagicMock()
pygame_mock.event = MagicMock()
pygame_mock.mouse = MagicMock()
pygame_mock.key = MagicMock()

with patch.dict("sys.modules", {"pygame": pygame_mock}):
    from index import Car, Obstacle, GameState


class TestGameCore(unittest.TestCase):
    """Test core game functionality without heavy mocking."""

    def test_car_movement(self):
        """Test car movement mechanics."""
        mock_assets = Mock()
        mock_assets.car_width = 50
        car = Car(mock_assets)

        # Test initial state
        self.assertEqual(car.x_change, 0)
        self.assertEqual(car.direction, 0)

        # Test left movement
        car.move_left()
        self.assertEqual(car.x_change, -10)
        self.assertEqual(car.direction, -1)

        # Test right movement
        car.move_right()
        self.assertEqual(car.x_change, 10)
        self.assertEqual(car.direction, 1)

        # Test stop
        car.stop_moving()
        self.assertEqual(car.x_change, 0)
        self.assertEqual(car.direction, 0)

    def test_car_position_update(self):
        """Test car position updates."""
        mock_assets = Mock()
        mock_assets.car_width = 50
        car = Car(mock_assets)

        initial_x = car.x
        car.move_right()
        car.update()
        self.assertEqual(car.x, initial_x + 10)

    def test_obstacle_movement(self):
        """Test obstacle movement."""
        mock_assets = Mock()
        mock_assets.obstacle_width = 30
        mock_assets.obstacle_height = 40

        with patch("random.randrange", return_value=100):
            obstacle = Obstacle(mock_assets)

        # Test initial position
        self.assertEqual(obstacle.y, -600)
        self.assertEqual(obstacle.speed, 5)

        # Test update
        initial_y = obstacle.y
        obstacle.update()
        self.assertEqual(obstacle.y, initial_y + 5)

    def test_game_state_constants(self):
        """Test game state constants."""
        self.assertEqual(GameState.INTRO, 0)
        self.assertEqual(GameState.DIFFICULTY_SELECT, 1)
        self.assertEqual(GameState.PLAYING, 2)
        self.assertEqual(GameState.PAUSED, 3)
        self.assertEqual(GameState.CRASHED, 4)
        self.assertEqual(GameState.QUIT, 5)


if __name__ == "__main__":
    unittest.main()

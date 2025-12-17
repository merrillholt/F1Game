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
pygame_mock.KEYDOWN = 1
pygame_mock.KEYUP = 2
pygame_mock.QUIT = 3
pygame_mock.K_LEFT = 4
pygame_mock.K_RIGHT = 5
pygame_mock.K_a = 6
pygame_mock.K_d = 7
pygame_mock.K_SPACE = 8
pygame_mock.K_ESCAPE = 9

with patch.dict("sys.modules", {"pygame": pygame_mock}):
    from index import Car, Obstacle, AssetManager, TextManager, GameState


class TestCar(unittest.TestCase):
    """Test cases for the Car class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_assets = Mock()
        self.mock_assets.car_width = 50
        self.mock_assets.car_img = Mock()
        self.mock_assets.car_left = Mock()
        self.mock_assets.car_right = Mock()
        self.car = Car(self.mock_assets)

    def test_car_initialization(self):
        """Test car is initialized with correct default values."""
        self.assertEqual(self.car.x, 400 * 0.4)  # DISPLAY_WIDTH * 0.4
        self.assertEqual(self.car.y, 600 * 0.6)  # DISPLAY_HEIGHT * 0.6
        self.assertEqual(self.car.x_change, 0)
        self.assertEqual(self.car.direction, 0)

    def test_car_move_left(self):
        """Test car moves left correctly."""
        self.car.move_left()
        self.assertEqual(self.car.x_change, -10)
        self.assertEqual(self.car.direction, -1)

    def test_car_move_right(self):
        """Test car moves right correctly."""
        self.car.move_right()
        self.assertEqual(self.car.x_change, 10)
        self.assertEqual(self.car.direction, 1)

    def test_car_stop_moving(self):
        """Test car stops moving correctly."""
        self.car.move_left()
        self.car.stop_moving()
        self.assertEqual(self.car.x_change, 0)
        self.assertEqual(self.car.direction, 0)

    def test_car_update_position(self):
        """Test car position updates correctly."""
        initial_x = self.car.x
        self.car.move_right()
        self.car.update()
        self.assertEqual(self.car.x, initial_x + 10)

    def test_car_out_of_bounds_left(self):
        """Test car out of bounds detection on left side."""
        self.car.x = -10
        self.assertTrue(self.car.is_out_of_bounds())

    def test_car_out_of_bounds_right(self):
        """Test car out of bounds detection on right side."""
        self.car.x = 400  # DISPLAY_WIDTH
        self.assertTrue(self.car.is_out_of_bounds())

    def test_car_in_bounds(self):
        """Test car in bounds detection."""
        self.car.x = 200
        self.assertFalse(self.car.is_out_of_bounds())


class TestObstacle(unittest.TestCase):
    """Test cases for the Obstacle class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_assets = Mock()
        self.mock_assets.obstacle_width = 30
        self.mock_assets.obstacle_height = 40
        self.mock_assets.obstacle_img = Mock()
        self.mock_assets.car_width = 50

        with patch("random.randrange", return_value=100):
            self.obstacle = Obstacle(self.mock_assets)

    def test_obstacle_initialization(self):
        """Test obstacle is initialized correctly."""
        self.assertEqual(self.obstacle.x, 100)
        self.assertEqual(self.obstacle.y, -600)
        self.assertEqual(self.obstacle.speed, 5)

    def test_obstacle_update_normal(self):
        """Test obstacle update when not passing screen."""
        initial_y = self.obstacle.y
        result = self.obstacle.update()
        self.assertEqual(self.obstacle.y, initial_y + 5)
        self.assertFalse(result)

    def test_obstacle_update_passed_screen(self):
        """Test obstacle update when passing screen."""
        self.obstacle.y = 650  # Past DISPLAY_HEIGHT (600)
        with patch("random.randrange", return_value=50):
            result = self.obstacle.update()
        self.assertTrue(result)
        self.assertEqual(self.obstacle.y, -40)  # Reset to -obstacle_height
        self.assertEqual(self.obstacle.x, 50)  # New random x position

    def test_obstacle_collision_detection_hit(self):
        """Test collision detection when car hits obstacle."""
        car = Mock()
        car.x = 100
        car.y = 50

        self.obstacle.x = 100
        self.obstacle.y = 50

        collision = self.obstacle.check_collision(car)
        self.assertTrue(collision)

    def test_obstacle_collision_detection_miss(self):
        """Test collision detection when car misses obstacle."""
        car = Mock()
        car.x = 200
        car.y = 50

        self.obstacle.x = 50
        self.obstacle.y = 20

        collision = self.obstacle.check_collision(car)
        self.assertFalse(collision)


class TestAssetManager(unittest.TestCase):
    """Test cases for the AssetManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock os.path functions
        self.patcher_abspath = patch("os.path.abspath", return_value="/test/path")
        self.patcher_dirname = patch("os.path.dirname", return_value="/test")
        self.patcher_abspath.start()
        self.patcher_dirname.start()

        # Create mock ImageData objects
        from asset_loader import ImageData

        mock_image = Mock()
        mock_image.get_rect.return_value = Mock(size=(50, 50))
        mock_image_data = ImageData(mock_image, (50, 50))

        # Mock asset_loader functions
        self.patcher_load_image = patch(
            "index.asset_loader.load_image", return_value=mock_image_data
        )
        self.patcher_load_sound = patch("index.asset_loader.load_sound", return_value=Mock())
        self.patcher_load_music = patch("index.asset_loader.load_music")

        self.patcher_load_image.start()
        self.patcher_load_sound.start()
        self.patcher_load_music.start()

        # Store a mock for log_error that can be checked in tests
        self.mock_log_error = Mock()

        with patch("builtins.open", unittest.mock.mock_open(read_data="100")):
            self.asset_manager = AssetManager()

    def tearDown(self):
        """Clean up patchers."""
        self.patcher_load_image.stop()
        self.patcher_load_sound.stop()
        self.patcher_load_music.stop()
        self.patcher_abspath.stop()
        self.patcher_dirname.stop()

    def test_get_high_score_valid_file(self):
        """Test reading valid high score from file."""
        with patch("builtins.open", unittest.mock.mock_open(read_data="150")):
            score = self.asset_manager.get_high_score()
            self.assertEqual(score, 150)

    def test_get_high_score_empty_file(self):
        """Test reading empty high score file."""
        with patch("builtins.open", unittest.mock.mock_open(read_data="")):
            score = self.asset_manager.get_high_score()
            self.assertEqual(score, 0)

    def test_get_high_score_file_not_found(self):
        """Test handling missing high score file."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            score = self.asset_manager.get_high_score()
            self.assertEqual(score, 0)

    def test_get_high_score_invalid_content(self):
        """Test handling invalid high score file content."""
        with patch("builtins.open", unittest.mock.mock_open(read_data="invalid")):
            score = self.asset_manager.get_high_score()
            self.assertEqual(score, 0)

    def test_update_high_score_success(self):
        """Test updating high score successfully."""
        mock_file = unittest.mock.mock_open()
        with patch("builtins.open", mock_file):
            self.asset_manager.update_high_score(250)
            mock_file().write.assert_called_once_with("250")

    def test_update_high_score_io_error(self):
        """Test handling IO error when updating high score."""
        # Test that IOError is caught and handled gracefully (doesn't crash)
        with patch("builtins.open", side_effect=IOError):
            # This should not raise an exception
            try:
                self.asset_manager.update_high_score(250)
            except Exception as e:
                self.fail(f"update_high_score raised {type(e).__name__} unexpectedly: {e}")


class TestTextManager(unittest.TestCase):
    """Test cases for the TextManager class."""

    def test_text_objects(self):
        """Test text object creation."""
        mock_font = Mock()
        mock_surface = Mock()
        mock_rect = Mock()
        mock_surface.get_rect.return_value = mock_rect
        mock_font.render.return_value = mock_surface

        result = TextManager.text_objects("Test", mock_font, (255, 255, 255))

        self.assertEqual(result, (mock_surface, mock_rect))
        mock_font.render.assert_called_once_with("Test", True, (255, 255, 255))


class TestGameState(unittest.TestCase):
    """Test cases for the GameState class."""

    def test_game_state_constants(self):
        """Test game state constants are defined correctly."""
        self.assertEqual(GameState.INTRO, 0)
        self.assertEqual(GameState.DIFFICULTY_SELECT, 1)
        self.assertEqual(GameState.PLAYING, 2)
        self.assertEqual(GameState.PAUSED, 3)
        self.assertEqual(GameState.CRASHED, 4)
        self.assertEqual(GameState.QUIT, 5)


if __name__ == "__main__":
    unittest.main()

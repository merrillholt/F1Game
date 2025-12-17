import pygame
import time
import random
import os
from typing import Tuple

from constants import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    FPS,
    BUTTON_START_X,
    NEW_GAME_Y,
    QUIT_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    CAR_SPEED,
    OBSTACLE_START_Y,
    CAR_START_X_RATIO,
    CAR_START_Y_RATIO,
    COLLISION_Y_TOLERANCE,
    COLLISION_X_TOLERANCE,
    BLACK,
    WHITE,
    RED,
    RED_LIGHT,
    LIGHT_BLUE,
    GRAY,
    GREEN,
    GREEN_LIGHT,
    BLUE,
    ASSET_FILES,
    LARGE_FONT_SIZE,
    MEDIUM_FONT_SIZE,
    SMALL_FONT_SIZE,
    BUTTON_FONT_SIZE,
    DEFAULT_FONT,
    COUNTDOWN_DELAY,
    TITLE_ANIMATION_SPEED,
    TEXTURE_OFFSET,
)
from logger import (
    log_info,
    log_error,
    log_debug,
    log_game_event,
    log_collision,
)
from difficulty import difficulty_manager
from powerups import powerup_manager
from asset_loader import asset_loader

# Initialize pygame
pygame.init()


class AssetManager:
    """Handles loading and managing game assets."""

    def __init__(self):
        """Initialize assets with proper path handling."""
        log_info("Initializing AssetManager")
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Load images
        self.load_images()

        # Load sounds
        self.load_sounds()

        log_info("AssetManager initialization complete")

    def load_images(self) -> None:
        """Load all game image assets."""
        # Load car images
        car_data = asset_loader.load_image(os.path.join(self.base_path, ASSET_FILES["car"]))
        self.car_img = car_data.image
        self.car_width = car_data.width
        self.car_height = car_data.height

        car_left_data = asset_loader.load_image(
            os.path.join(self.base_path, ASSET_FILES["car_left"])
        )
        self.car_left = car_left_data.image
        self.car_left_width = car_left_data.width
        self.car_left_height = car_left_data.height

        car_right_data = asset_loader.load_image(
            os.path.join(self.base_path, ASSET_FILES["car_right"])
        )
        self.car_right = car_right_data.image
        self.car_right_width = car_right_data.width
        self.car_right_height = car_right_data.height

        # Load obstacle image
        obstacle_data = asset_loader.load_image(
            os.path.join(self.base_path, ASSET_FILES["obstacle"])
        )
        self.obstacle_img = obstacle_data.image
        self.obstacle_width = obstacle_data.width
        self.obstacle_height = obstacle_data.height

        # Load texture image
        texture_data = asset_loader.load_image(os.path.join(self.base_path, ASSET_FILES["texture"]))
        self.texture = texture_data.image
        self.texture_width = texture_data.width
        self.texture_height = texture_data.height

        # Load background images
        background_data = asset_loader.load_image(
            os.path.join(self.base_path, ASSET_FILES["background"])
        )
        self.background = background_data.image
        self.background_rect = self.background.get_rect()

        background_still_data = asset_loader.load_image(
            os.path.join(self.base_path, ASSET_FILES["background_still"])
        )
        self.background_still = background_still_data.image

    def load_sounds(self) -> None:
        """Load all game sound assets."""
        self.intro_1 = asset_loader.load_sound(os.path.join(self.base_path, ASSET_FILES["intro_1"]))
        self.intro_2 = asset_loader.load_sound(os.path.join(self.base_path, ASSET_FILES["intro_2"]))
        self.crash_sound = asset_loader.load_sound(
            os.path.join(self.base_path, ASSET_FILES["crash_sound"])
        )
        self.ignition = asset_loader.load_sound(
            os.path.join(self.base_path, ASSET_FILES["ignition"])
        )
        asset_loader.load_music(os.path.join(self.base_path, ASSET_FILES["running"]))

    def get_high_score(self) -> int:
        """Read high score from file."""
        try:
            with open(os.path.join(self.base_path, ASSET_FILES["high_score"]), "r") as hs_file:
                return int(hs_file.read().strip() or "0")
        except (FileNotFoundError, ValueError) as e:
            log_debug(f"High score file not found or invalid: {e}")
            return 0

    def update_high_score(self, score: int) -> None:
        """Update the high score file."""
        try:
            with open(os.path.join(self.base_path, ASSET_FILES["high_score"]), "w") as hs_file:
                hs_file.write(str(score))
        except IOError as e:
            log_error("Could not write high score to file", e)


class Car:
    """Player's car with position and movement information."""

    def __init__(self, assets: AssetManager):
        """Initialize car with starting position."""
        self.assets = assets
        self.x = DISPLAY_WIDTH * CAR_START_X_RATIO
        self.y = DISPLAY_HEIGHT * CAR_START_Y_RATIO
        self.x_change = 0
        self.direction = 0  # 0: straight, -1: left, 1: right

    def update(self) -> None:
        """Update car position based on current movement."""
        self.x += self.x_change

    def render(self, display) -> None:
        """Render car on screen with appropriate direction sprite."""
        car_image = self._get_car_image()
        display.blit(car_image, (self.x, self.y))

    def _get_car_image(self):
        """Get the appropriate car image based on direction."""
        if self.direction == -1:
            return self.assets.car_left
        elif self.direction == 1:
            return self.assets.car_right
        return self.assets.car_img

    def move_left(self) -> None:
        """Move car left."""
        self.x_change = -CAR_SPEED
        self.direction = -1

    def move_right(self) -> None:
        """Move car right."""
        self.x_change = CAR_SPEED
        self.direction = 1

    def stop_moving(self) -> None:
        """Stop car movement."""
        self.x_change = 0
        self.direction = 0

    def is_out_of_bounds(self) -> bool:
        """Check if car is out of screen bounds."""
        return self.x > DISPLAY_WIDTH - self.assets.car_width or self.x < 0


class Obstacle:
    """Game obstacle that player must avoid."""

    def __init__(self, assets: AssetManager):
        """Initialize obstacle with random starting position."""
        self.assets = assets
        margin = 8
        self.x = random.randrange(margin, DISPLAY_WIDTH - assets.obstacle_width - margin)
        self.y: float = float(OBSTACLE_START_Y)
        self.speed = difficulty_manager.get_obstacle_speed()

    def update(self) -> bool:
        """Update obstacle position and check if it passed the screen.

        Returns:
            bool: True if obstacle passed the screen, False otherwise
        """
        self.y += self.speed
        if self.y > DISPLAY_HEIGHT:
            self.reset()
            return True
        return False

    def reset(self) -> None:
        """Reset obstacle to top of screen at random x position."""
        self.y = 0 - self.assets.obstacle_height
        self.x = random.randrange(0, DISPLAY_WIDTH)

    def render(self, display) -> None:
        """Render obstacle on screen."""
        display.blit(self.assets.obstacle_img, (self.x, self.y))

    def check_collision(self, car: Car) -> bool:
        """Check if obstacle collides with car.

        Args:
            car: The player car to check for collision

        Returns:
            bool: True if collision detected, False otherwise
        """
        if (
            car.y < self.y + self.assets.obstacle_height - COLLISION_Y_TOLERANCE
            and car.x > self.x - self.assets.car_width - COLLISION_X_TOLERANCE
            and car.x < self.x + self.assets.obstacle_width - COLLISION_X_TOLERANCE
        ):
            return True
        return False


class TextManager:
    """Handles rendering text in the game."""

    @staticmethod
    def text_objects(text: str, font, color: Tuple[int, int, int]) -> Tuple:
        """Create text surface and rectangle.

        Args:
            text: The text to render
            font: The pygame font to use
            color: RGB color tuple

        Returns:
            tuple: (TextSurface, TextRect)
        """
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    @staticmethod
    def display_score(display, count: int, high_score: int, speed: float) -> None:
        """Display score, high score and speed on screen.

        Args:
            display: The pygame display to render on
            count: Current score
            high_score: Current high score
            speed: Current speed
        """
        font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
        score = font.render(f"Dodged: {count}", True, LIGHT_BLUE)
        highscore = font.render(f"High Score: {high_score}", True, LIGHT_BLUE)
        speed_text = font.render(f"Speed: {speed}Km/h", True, LIGHT_BLUE)
        display.blit(score, (10, 0))
        display.blit(highscore, (10, 27))
        display.blit(speed_text, (DISPLAY_WIDTH - 125, 0))

    @staticmethod
    def message_display(
        display,
        text: str,
        shift_x: int,
        shift_y: int,
        color: Tuple[int, int, int],
        sleep_time: float,
    ) -> None:
        """Display a centered message on screen.

        Args:
            display: The pygame display to render on
            text: The text to display
            shift_x: X-axis shift from center
            shift_y: Y-axis shift from center
            color: RGB color tuple
            sleep_time: Time to display message in seconds
        """
        large_text = pygame.font.Font(DEFAULT_FONT, LARGE_FONT_SIZE)
        text_surf, text_rect = TextManager.text_objects(text, large_text, color)
        text_rect.center = ((DISPLAY_WIDTH / 2 - shift_x), (DISPLAY_HEIGHT / 2 - shift_y))
        display.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(sleep_time)

    @staticmethod
    def title_msg(display, shift_x: int, shift_y: int, color: Tuple[int, int, int]) -> None:
        """Display game title message.

        Args:
            display: The pygame display to render on
            shift_x: X-axis shift from center
            shift_y: Y-axis shift from center
            color: RGB color tuple
        """
        large_text = pygame.font.Font(DEFAULT_FONT, MEDIUM_FONT_SIZE)
        text_surf, text_rect = TextManager.text_objects("F1 Racing Game", large_text, color)
        text_rect.center = ((DISPLAY_WIDTH / 2 - shift_x), (DISPLAY_HEIGHT / 3 - shift_y))
        display.blit(text_surf, text_rect)
        time.sleep(0.15)
        pygame.display.update()


class Button:
    """Interactive button for UI elements."""

    @staticmethod
    def create(
        display,
        msg: str,
        x: int,
        y: int,
        w: int,
        h: int,
        inactive_color: Tuple[int, int, int],
        active_color: Tuple[int, int, int],
    ) -> bool:
        """Create an interactive button and check if it's clicked.

        Args:
            display: The pygame display to render on
            msg: Button text
            x: X position
            y: Y position
            w: Width
            h: Height
            inactive_color: Button color when not hovered
            active_color: Button color when hovered

        Returns:
            bool: True if button was clicked, False otherwise
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        is_hovered = x + w > mouse[0] > x and y + h > mouse[1] > y
        button_color = active_color if is_hovered else inactive_color

        pygame.draw.rect(display, button_color, (x, y, w, h))

        if is_hovered and click[0] == 1:
            return True

        small_text = pygame.font.Font(DEFAULT_FONT, BUTTON_FONT_SIZE)
        text_surf, text_rect = TextManager.text_objects(msg, small_text, WHITE)
        text_rect.center = ((x + w / 2), (y + h / 2))
        display.blit(text_surf, text_rect)
        return False


class GameState:
    """Enum-like class to track game states."""

    INTRO = 0
    DIFFICULTY_SELECT = 1
    PLAYING = 2
    PAUSED = 3
    CRASHED = 4
    QUIT = 5


class Game:
    """Main game class that manages the game state."""

    def __init__(self):
        """Initialize game components and state."""
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("F1 Racing Game")
        self.clock = pygame.time.Clock()

        self.assets = AssetManager()
        self.car = Car(self.assets)
        self.obstacle = Obstacle(self.assets)

        self.dodged = 0
        self.high_score = self.assets.get_high_score()
        self.game_exit = False
        self.track_y = 0
        self.state = GameState.INTRO

    def render_texture(self, y_pos: float) -> None:
        """Render scrolling texture for background.

        Args:
            y_pos: Current Y position of texture
        """
        texture_positions = [y_pos - TEXTURE_OFFSET, y_pos, y_pos + TEXTURE_OFFSET]
        for pos in texture_positions:
            self.display.blit(self.assets.texture, (0, pos))

    def title_animation(self) -> None:
        """Display title animation sequence."""
        height_anim: float = float(DISPLAY_HEIGHT)
        pygame.mixer.Sound.play(self.assets.intro_1)

        while height_anim > -600:
            self.display.fill(WHITE)
            obstacle_x = DISPLAY_WIDTH / 2 - self.assets.obstacle_width / 2
            self.display.blit(self.assets.obstacle_img, (obstacle_x, height_anim))
            height_anim -= TITLE_ANIMATION_SPEED
            pygame.display.update()

        TextManager.title_msg(self.display, 0, 0, BLACK)
        time.sleep(0.1)
        pygame.mixer.Sound.play(self.assets.intro_2)

    def countdown(self) -> None:
        """Display 3-2-1-GO countdown before starting game."""
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(self.assets.ignition)

        for count in range(3, -1, -1):
            self.display.blit(self.assets.background, self.assets.background_rect)
            self.car.render(self.display)

            if count == 0:
                TextManager.message_display(self.display, "GO!", 0, 0, GREEN, COUNTDOWN_DELAY)
                pygame.mixer.music.play(-1)
            else:
                TextManager.message_display(self.display, str(count), 0, 0, RED, COUNTDOWN_DELAY)

        self.clock.tick(15)

    def pause_game(self) -> None:
        """Pause the game until user resumes."""
        pygame.mixer.music.pause()
        self.state = GameState.PAUSED

        while self.state == GameState.PAUSED:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    self.state = GameState.QUIT
                    return

                TextManager.message_display(self.display, "Paused", 0, 0, BLUE, 1.5)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.music.unpause()
                    self.state = GameState.PLAYING
                    return

            pygame.display.update()
            self.clock.tick(15)

    def crash(self) -> None:
        """Handle game over after crash."""
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(self.assets.crash_sound)
        TextManager.message_display(self.display, "YOU CRASHED", 0, 0, RED, 0)
        self.state = GameState.CRASHED

        while self.state == GameState.CRASHED:
            play_again = Button.create(
                self.display,
                "Play Again",
                BUTTON_START_X,
                NEW_GAME_Y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                LIGHT_BLUE,
                GREEN,
            )

            quit_game = Button.create(
                self.display,
                "Quit",
                BUTTON_START_X,
                QUIT_Y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                RED_LIGHT,
                RED,
            )

            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or quit_game
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                ):
                    self.state = GameState.QUIT
                    return

                if play_again or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.reset_game()
                    self.state = GameState.PLAYING
                    self.countdown()
                    return

            pygame.display.update()
            self.clock.tick(15)

    def reset_game(self) -> None:
        """Reset game state for a new game."""
        self.car = Car(self.assets)
        self.obstacle = Obstacle(self.assets)
        self.dodged = 0
        self.game_exit = False
        powerup_manager.clear_all()

    def show_intro(self) -> None:
        """Show game introduction screen."""
        self.display.fill(WHITE)
        self.title_animation()
        self.state = GameState.INTRO

        while self.state == GameState.INTRO:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    self.state = GameState.QUIT
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.state = GameState.DIFFICULTY_SELECT
                    return

            play = Button.create(
                self.display,
                "New game",
                BUTTON_START_X,
                NEW_GAME_Y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                LIGHT_BLUE,
                BLUE,
            )

            quit_game = Button.create(
                self.display,
                "Quit",
                BUTTON_START_X,
                QUIT_Y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                RED_LIGHT,
                RED,
            )

            if play:
                self.state = GameState.DIFFICULTY_SELECT
                return

            if quit_game:
                self.state = GameState.QUIT
                return

            pygame.display.update()
            menu_fps = 15
            self.clock.tick(menu_fps)

    def show_difficulty_select(self) -> None:
        """Show difficulty selection screen."""
        self.state = GameState.DIFFICULTY_SELECT

        while self.state == GameState.DIFFICULTY_SELECT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    self.state = GameState.INTRO
                    return

            self.display.blit(self.assets.background_still, (0, 0))

            # Title
            title_font = pygame.font.Font(DEFAULT_FONT, MEDIUM_FONT_SIZE)
            title_surf, title_rect = TextManager.text_objects(
                "Select Difficulty", title_font, WHITE
            )
            title_rect.center = (DISPLAY_WIDTH // 2, 150)
            self.display.blit(title_surf, title_rect)

            # Difficulty buttons
            button_y_start = 220
            button_spacing = 70

            difficulties = difficulty_manager.get_available_difficulties()
            current_diff = difficulty_manager.get_difficulty()

            for i, diff in enumerate(difficulties):
                y_pos = button_y_start + (i * button_spacing)

                # Highlight current difficulty
                if diff == current_diff:
                    button_color = GREEN
                    hover_color = GREEN_LIGHT
                else:
                    button_color = LIGHT_BLUE
                    hover_color = BLUE

                if Button.create(
                    self.display,
                    diff.capitalize(),
                    BUTTON_START_X,
                    y_pos,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT,
                    button_color,
                    hover_color,
                ):
                    difficulty_manager.set_difficulty(diff)
                    self.state = GameState.PLAYING
                    return

            # Back button
            if Button.create(
                self.display,
                "Back",
                BUTTON_START_X,
                button_y_start + (len(difficulties) * button_spacing),
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                GRAY,
                RED,
            ):
                self.state = GameState.INTRO
                return

            # Show difficulty description
            desc = difficulty_manager.get_difficulty_description()
            desc_font = pygame.font.Font(DEFAULT_FONT, 16)
            desc_lines = self._wrap_text(desc, desc_font, DISPLAY_WIDTH - 40)

            y_offset = button_y_start + ((len(difficulties) + 1) * button_spacing) + 20
            for line in desc_lines:
                desc_surf, desc_rect = TextManager.text_objects(line, desc_font, WHITE)
                desc_rect.center = (DISPLAY_WIDTH // 2, y_offset)
                self.display.blit(desc_surf, desc_rect)
                y_offset += 20

            pygame.display.update()
            menu_fps = 15
            self.clock.tick(menu_fps)

    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """Wrap text to fit within specified width."""
        words = text.split(" ")
        lines = []
        current_line: list[str] = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def render_powerups(self) -> None:
        """Render power-ups on screen."""
        for powerup in powerup_manager.get_powerups():
            color = powerup.properties.get("color", WHITE)
            pygame.draw.rect(
                self.display, color, (powerup.x, powerup.y, powerup.width, powerup.height)
            )

            # Add a simple border
            pygame.draw.rect(
                self.display, WHITE, (powerup.x, powerup.y, powerup.width, powerup.height), 2
            )

    def render_active_powerups(self) -> None:
        """Render active power-ups indicator."""
        active_powerups = powerup_manager.get_active_powerups()
        if not active_powerups:
            return

        y_offset = 55  # Start below score
        font = pygame.font.SysFont(None, 18)

        for powerup in active_powerups:
            remaining = powerup.get_remaining_time()
            text = f"{powerup.type.replace('_', ' ').title()}: {remaining:.1f}s"
            color = powerup.properties.get("color", WHITE)

            text_surf = font.render(text, True, color)
            self.display.blit(text_surf, (10, y_offset))
            y_offset += 20

    def handle_events(self) -> None:
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.state = GameState.QUIT
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.car.move_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.car.move_right()
                if event.key == pygame.K_SPACE:
                    self.pause_game()

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    self.car.stop_moving()

    def update_game_state(self) -> None:
        """Update positions and check for collisions."""
        self.car.update()

        # Update power-ups
        powerup_manager.update(
            self.car.x, self.car.y, self.assets.car_width, self.assets.car_height
        )

        # Check boundary collision
        if self.car.is_out_of_bounds():
            self.state = GameState.CRASHED
            self.crash()
            return

        # Update obstacle and check if passed
        if self.obstacle.update():
            self.dodged += 1
            self.obstacle.speed += difficulty_manager.get_speed_increment()
            difficulty_manager.adjust_for_score(self.dodged)

            # Spawn power-up chance
            powerup_manager.spawn_powerup(self.obstacle.x, self.obstacle.y)

        # Check obstacle collision (unless shielded)
        if self.obstacle.check_collision(self.car) and not powerup_manager.is_shielded():
            log_collision(
                (self.car.x, self.car.y), (self.obstacle.x, self.obstacle.y), self.obstacle.speed
            )
            self.state = GameState.CRASHED
            self.crash()
            return

        # Update high score if needed
        if self.dodged > self.high_score:
            self.high_score = self.dodged
            self.assets.update_high_score(self.dodged)
            log_game_event("New high score achieved", {"score": self.dodged})

    def render(self) -> None:
        """Render all game elements."""
        # Background and texture
        self.display.blit(self.assets.background, self.assets.background_rect)
        self.render_texture(self.obstacle.y)

        # Game objects
        self.obstacle.render(self.display)
        self.car.render(self.display)

        # Render power-ups
        self.render_powerups()

        # UI elements
        TextManager.display_score(self.display, self.dodged, self.high_score, self.obstacle.speed)
        self.render_active_powerups()

        pygame.display.update()

    def game_loop(self) -> None:
        """Main game loop."""
        pygame.mixer.music.play(-1)
        self.countdown()

        while self.state == GameState.PLAYING:
            self.handle_events()
            if self.state == GameState.QUIT:
                break

            self.update_game_state()
            self.render()
            self.clock.tick(FPS)

    def run(self) -> None:
        """Run the complete game flow."""
        self.show_intro()

        if self.state == GameState.DIFFICULTY_SELECT:
            self.show_difficulty_select()

        if self.state == GameState.PLAYING:
            self.game_loop()


def main():
    """Main function to start the game."""
    log_info("Starting F1 Racing Game")
    try:
        game = Game()
        game.run()
    except Exception as e:
        log_error("Game crashed with exception", e)
        raise
    finally:
        pygame.quit()
        log_info("Game shutdown complete")
        quit()


if __name__ == "__main__":
    main()

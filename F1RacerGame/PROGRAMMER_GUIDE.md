# F1 Racing Game - Technical Documentation

## Overview
F1 Racing Game is a vertical scrolling driving game built with Pygame where the player controls a car to avoid obstacles. The game features keyboard controls, collision detection, score tracking, and persistent high scores.

## Architecture

### Core Components
- **Game**: Main controller class managing game loop, state transitions, and overall flow
- **AssetManager**: Handles loading and managing images, sounds, and file operations
- **Car**: Player-controlled entity with position tracking and movement logic
- **Obstacle**: Dynamic entities that the player must avoid to score points
- **TextManager**: Utility class for rendering text elements
- **Button**: UI component for creating interactive buttons
- **GameState**: Enum-like class defining game states (INTRO, PLAYING, PAUSED, CRASHED, QUIT)

### Game Flow
1. Game initialization loads assets and sets up initial state
2. Game loop runs at 60 FPS, handling:
   - Input processing (keyboard/mouse events)
   - State updates (position calculations, collision detection)
   - Rendering (background, objects, UI elements)
3. State transitions between intro, playing, paused, crashed, and quit states

## Technical Details

### Display and Coordinate System
- Screen size: 400×600 pixels
- Origin (0,0) is top-left corner
- Positive y-axis points downward
- Car positioned at 40% width, 60% height (default)
- Button dimensions: 242×50 pixels

### Physics and Movement
- Car movement: 10 pixels per frame (left/right)
- Obstacle initial speed: 5 pixels per frame (downward)
- Obstacle speed increases by 1 pixel each time player successfully dodges
- Simple rectangle-based collision detection

### Asset Management
- Images: car sprites (straight, left, right), obstacles, background, textures
- Audio: sound effects (intro, crash, ignition), background music
- File I/O: Reading/writing high score to file

### Input Handling
- Keyboard controls:
  - Left Arrow/A: Move left
  - Right Arrow/D: Move right
  - Space: Pause game / Continue / Play again (context dependent)
  - Escape: Quit game
- Mouse controls:
  - Click buttons in menus

### Game States
1. **INTRO (0)**: Title screen with animated intro and menu buttons
2. **PLAYING (1)**: Main gameplay with active car movement and obstacle avoidance
3. **PAUSED (2)**: Temporarily halts gameplay until resumed with spacebar
4. **CRASHED (3)**: Game over state showing score and offering replay/quit options
5. **QUIT (4)**: Terminal state initiating program exit

### Score System
- Score increments when obstacle passes bottom of screen
- High score persisted to disk (`high_score.txt`)
- Displayed along with current speed during gameplay

## Implementation Notes

### Main Game Loop Pattern
```python
# Simplified game loop
while state == GameState.PLAYING:
    handle_events()    # Process input
    update_game_state() # Update game objects
    render()           # Render frame
    clock.tick(60)     # Maintain 60 FPS
```

### Collision Detection
```python
# Simplified collision logic
if (car.y < obstacle.y + obstacle_height - 15 and 
    car.x > obstacle.x - car_width - 5 and 
    car.x < obstacle.x + obstacle_width - 5):
    # Collision detected
```

### Performance Considerations
- Asset loading occurs only at initialization
- Minimal CPU usage in steady state
- No memory leaks from repeated asset loading
- Uses Pygame's optimized sprite blitting for rendering

## Extension Points
- Multiple obstacles could be added by extending Obstacle class to list management
- Different car abilities could be implemented through Car class extensions
- Power-ups could be added as new game objects following similar patterns
- Level progression system could modify obstacle patterns/speeds
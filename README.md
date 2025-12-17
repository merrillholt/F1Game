# F1 Racing Game 🏎️

A comprehensive Formula 1 racing game built with Python and Pygame, featuring multiple difficulty levels, power-ups, obstacle variety, and professional development practices.

## 🎮 Features

- **Multiple Difficulty Levels**: Easy, Normal, and Hard modes with dynamic scaling
- **Power-Up System**: Shield, Slow Motion, and Speed Boost effects
- **Varied Obstacles**: 5 different vehicle types with unique properties
- **Professional Architecture**: Modular design with configuration management
- **Comprehensive Testing**: Unit tests with mocked dependencies
- **Structured Logging**: File and console output with game event tracking

## 🚀 Quick Start

### Method 0: uv (fastest)
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt  # optional for tooling
cd F1RacerGame && python index.py
```

### Method 1: Using Setup Script (Recommended)
```bash
# Clone and setup in one command
./setup_env.sh
source venv/bin/activate
cd F1RacerGame && python index.py
```

### Method 2: Using Make Commands
```bash
# Setup everything
make setup

# Run the game
make run

# Run tests
make test
```

### Method 3: Manual Setup
```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Run the game
cd F1RacerGame && python index.py
```

## 📁 Project Structure

```
F1Game/
├── README.md
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── pyproject.toml           # Modern Python project configuration
├── setup.cfg                # Additional tool configuration
├── Makefile                 # Development commands
├── setup_env.sh            # Virtual environment setup script
├── activate.sh             # Quick activation script
├── .python-version         # Python version specification
├── .gitignore              # Comprehensive ignore patterns
├── F1RacerGame/            # Game source code
│   ├── index.py            # Main game entry point
│   ├── constants.py        # Game constants and configuration
│   ├── config.py           # JSON-based configuration management
│   ├── logger.py           # Structured logging system
│   ├── difficulty.py       # Difficulty level management
│   ├── powerups.py         # Power-up system
│   ├── obstacles.py        # Multiple obstacle types
│   └── assets/             # Game images and sounds
├── tests/                  # Unit tests
│   ├── test_simple.py      # Core game logic tests
│   └── test_game_logic.py  # Comprehensive test suite
└── .venv/                  # Virtual environment (created by uv)
```

## 🛠️ Development

### Virtual Environment Best Practices

This project follows Python virtual environment best practices:

1. **Isolated Dependencies**: All dependencies in separate `venv/` directory
2. **Version Control**: Virtual environment excluded from git
3. **Python Version**: Specified in `.python-version` file
4. **Dependency Management**: Separate production and development requirements
5. **Modern Configuration**: Uses `pyproject.toml` for tool configuration

### Development Commands

```bash
# Setup development environment
make dev-setup

# Code quality
make format          # Format code with black
make lint           # Lint code with flake8
make test           # Run all tests

# Maintenance
make clean          # Clean generated files
make clean-all      # Clean everything including venv
make status         # Check environment status
```

### Manual Development Setup

```bash
# Activate environment
source .venv/bin/activate

# Install development dependencies
uv pip install -r requirements-dev.txt

# Run tests with coverage
pytest tests/ --cov=F1RacerGame --cov-report=html

# Format code
black F1RacerGame/ tests/

# Lint code
flake8 F1RacerGame/ tests/

# Type checking
mypy F1RacerGame/
```

## 🎯 Game Controls

- **Left Arrow / A**: Move left
- **Right Arrow / D**: Move right
- **Space**: Pause/Resume game
- **Escape**: Quit game

## 🏆 Game Features

### Difficulty Levels
- **Easy**: Slower obstacles, gentler increases
- **Normal**: Balanced gameplay
- **Hard**: Fast obstacles, quick progression

### Power-Ups
- **Shield** (Blue): Temporary invincibility
- **Slow Motion** (Green): Reduces obstacle speed
- **Speed Boost** (Red): Increases movement speed

### Obstacle Types
- **Normal Car**: Standard obstacle
- **Truck**: Larger, slower, more points
- **Sports Car**: Faster, high value
- **Motorcycle**: Small and quick
- **Bus**: Largest obstacle, highest points

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=F1RacerGame --cov-report=html

# Run specific test file
pytest tests/test_simple.py -v
```

## 📋 Requirements

- Python 3.8+
- pygame 2.6.0+
- See `requirements.txt` for complete list

## 🔧 Configuration

The game supports JSON-based configuration in `F1RacerGame/game_config.json`:

```json
{
  "graphics": {
    "display_width": 400,
    "display_height": 600,
    "fps": 60
  },
  "gameplay": {
    "difficulty": "normal",
    "enable_powerups": true
  }
}
```

## 📝 Logging

Game events are logged to `F1RacerGame/logs/` with different levels:
- Game events and state changes
- Performance metrics
- Error tracking
- Score milestones

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Setup development environment: `make dev-setup`
4. Make changes and add tests
5. Run quality checks: `make format lint test`
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Virtual Environment Status**: ✅ Following Python best practices
**Code Quality**: ✅ Black formatting, flake8 linting, mypy type checking
**Testing**: ✅ Comprehensive test suite with pytest
**Documentation**: ✅ Complete setup and usage instructions

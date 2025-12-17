# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Run Commands
- Run game: `python index.py`
- Debug with increased verbosity: `python -m index --debug`
- Run with profiling: `python -m cProfile -o profile_results.txt index.py`

## Code Style Guidelines
- **Imports**: Order as 1) stdlib, 2) third-party (pygame), 3) local modules; use typing imports
- **Types**: Use type hints for all function parameters and return types
- **Naming**:
  - Classes: PascalCase (e.g., `AssetManager`)
  - Functions/Methods: snake_case (e.g., `update_high_score`)
  - Variables: snake_case (e.g., `display_width`)
  - Constants: ALL_CAPS (e.g., `DISPLAY_WIDTH`, `BLACK`)
- **Documentation**: Use docstrings for classes and methods describing purpose and parameters
- **Error Handling**: Use try/except blocks for file operations with specific exceptions
- **Path Handling**: Always use `os.path.join()` for cross-platform compatibility
- **OOP Structure**: Follow class-based design pattern established in codebase

## Architecture Patterns
- Separate game components by responsibility (rendering, assets, UI, game logic)
- Use manager classes to handle related functionality (e.g., AssetManager, TextManager)
- Maintain clean separation between game state and rendering logic
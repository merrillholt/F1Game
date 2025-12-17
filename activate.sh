#!/bin/bash
# activate.sh - Quick activation script for F1 Racing Game virtual environment
# Usage: source activate.sh

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

VENV_DIR=".venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Virtual environment not found at ${VENV_DIR}${NC}"
    echo -e "${YELLOW}💡 Run ./setup_env.sh to create the uv virtual environment${NC}"
    return 1 2>/dev/null || exit 1
fi

# Activate virtual environment
echo -e "${GREEN}🔌 Activating F1 Racing Game virtual environment (.venv)...${NC}"
source "$VENV_DIR/bin/activate"

# Display useful information
echo -e "${GREEN}✅ Virtual environment activated!${NC}"
echo -e "${YELLOW}🐍 Python: $(python --version)${NC}"
echo -e "${YELLOW}📍 Location: $(which python)${NC}"
echo -e ""
echo -e "${GREEN}🎮 Quick commands:${NC}"
echo -e "   ${YELLOW}Run game:${NC}     cd F1RacerGame && python index.py"
echo -e "   ${YELLOW}Run tests:${NC}    python -m pytest tests/ -v"
echo -e "   ${YELLOW}Format code:${NC}  black F1RacerGame/"
echo -e "   ${YELLOW}Lint code:${NC}    flake8 F1RacerGame/"
echo -e "   ${YELLOW}Deactivate:${NC}   deactivate"

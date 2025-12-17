#!/bin/bash
# setup_env.sh - Virtual Environment Setup Script for F1 Racing Game
# This script follows Python virtual environment best practices

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="F1 Racing Game"
PYTHON_VERSION="3.8"
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
DEV_REQUIREMENTS_FILE="requirements-dev.txt"

echo -e "${BLUE}🏎️  Setting up ${PROJECT_NAME} development environment...${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv is not installed or not on PATH. Install via \`pip install uv\` or download from https://github.com/astral-sh/uv${NC}"
    exit 1
fi

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists at ${VENV_DIR}${NC}"
    echo -e "${YELLOW}   Do you want to recreate it? (y/N): ${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  Recreating virtual environment...${NC}"
        uv venv --clear --python "python${PYTHON_VERSION}"
    else
        echo -e "${GREEN}✅ Using existing virtual environment${NC}"
        source "$VENV_DIR/bin/activate"
        echo -e "${GREEN}🔍 Checking installed packages (uv pip list)...${NC}"
        uv pip list
        exit 0
    fi
fi

# Create virtual environment
echo -e "${BLUE}📦 Creating virtual environment...${NC}"
uv venv --python "python${PYTHON_VERSION}"

# Activate virtual environment
echo -e "${BLUE}🔌 Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Install requirements if file exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo -e "${BLUE}📋 Installing dependencies from ${REQUIREMENTS_FILE}...${NC}"
    uv pip install -r "$REQUIREMENTS_FILE"
else
    echo -e "${YELLOW}⚠️  No ${REQUIREMENTS_FILE} found. Installing basic dependencies...${NC}"
    uv pip install pygame pytest black flake8
fi

# Optional: dev requirements
if [ -f "$DEV_REQUIREMENTS_FILE" ]; then
    echo -e "${BLUE}🛠️  Installing development dependencies from ${DEV_REQUIREMENTS_FILE}...${NC}"
    if ! uv pip install -r "$DEV_REQUIREMENTS_FILE"; then
        echo -e "${YELLOW}⚠️  Development dependencies were not fully installed (see error above).${NC}"
    fi
fi

# Verify installation
echo -e "${GREEN}🔍 Verifying installation...${NC}"
uv pip list

echo -e "${GREEN}✅ Virtual environment setup complete!${NC}"
echo -e "${BLUE}📝 Usage:${NC}"
echo -e "   ${YELLOW}Activate:${NC}   source .venv/bin/activate"
echo -e "   ${YELLOW}Deactivate:${NC} deactivate"
echo -e "   ${YELLOW}Run game:${NC}   cd F1RacerGame && python index.py"
echo -e "   ${YELLOW}Run tests:${NC}  python -m pytest tests/"
echo -e ""
echo -e "${GREEN}🎮 Environment is ready for ${PROJECT_NAME} development!${NC}"

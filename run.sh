#!/bin/bash

set -e

# =========================
# Check Python 3.11
# =========================

if ! command -v python3.11 &> /dev/null
then
    echo "Python 3.11 is required but was not found."

    echo "Python 3.11 is required but was not found."
    echo ""

    echo "Install instructions:"

    echo "Ubuntu/Debian:"
    echo "  sudo apt install python3.11 python3.11-venv"

    echo ""
    echo "Fedora:"
    echo "  sudo dnf install python3.11"

    echo ""
    echo "macOS (Homebrew):"
    echo "  brew install python@3.11"

    echo ""
    echo "Then rerun the script."

    exit 1

fi

# =========================
# Check .env File
# =========================

if [ ! -f ".env" ]; then
    echo ".env file not found."
    echo "Please create a .env file using .env.example"
    exit 1
fi

# =========================
# Create Virtual Environment
# =========================

if [ ! -f "venvpy311/bin/activate" ]; then

    echo "Creating Python 3.11 virtual environment..."

    rm -rf venvpy311

    python3.11 -m venv venvpy311

fi

# =========================
# Activate Virtual Environment
# =========================

echo "Activating virtual environment..."

source venvpy311/bin/activate

# =========================
# Verify Activation
# =========================

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# =========================
# Install Dependencies
# =========================

echo "Installing dependencies..."

pip install --upgrade pip
pip install -r requirements.txt

# =========================
# Start Application
# =========================

echo "Starting Streamlit application..."

python -m streamlit run app.py
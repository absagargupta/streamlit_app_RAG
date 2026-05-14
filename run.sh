#!/bin/bash

if ! command -v python3.11 &> /dev/null
then
    echo "Python 3.11 is required but was not found."
    echo "Please install Python 3.11 and rerun the script."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo ".env file not found."
    echo "Please create a .env file using .env.example"
    exit 1
fi

if [ ! -d "venvpy311" ]; then
    echo "Creating Python 3.11 virtual environment..."
    python3.11 -m venv venvpy311
fi

echo "Activating virtual environment..."

source venvpy311/bin/activate

echo "Installing dependencies..."

pip install --upgrade pip
pip install -r requirements.txt

echo "Starting Streamlit application..."

python -m streamlit run app.py
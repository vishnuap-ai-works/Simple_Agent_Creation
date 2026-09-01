#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running the application..."
python agent_with_tools.py


#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Find a stable python version to avoid build issues with missing pre-compiled wheels
PYTHON_CMD="python3"
for py in python3.12 python3.11 python3.10; do
    if command -v $py &> /dev/null; then
        PYTHON_CMD=$py
        break
    fi
done

echo "Using $PYTHON_CMD for virtual environment"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running the application..."
python agent_with_tools.py

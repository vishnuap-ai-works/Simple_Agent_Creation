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

echo "Starting Autogen Agent..."

# Uncomment and set your API keys here if they are not already set in your environment
# export OPENAI_API_KEY="your_openai_api_key"
# export OPENAI_BASE_URL="your_openai_base_url"
# export SERPAPI_API_KEY="your_serpapi_api_key"
# export OPENAI_MODEL_NAME="gpt-4o"

python "agent_with_tools.py"

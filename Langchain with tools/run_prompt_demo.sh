#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run agent_with_tools.sh first to set it up, or create a venv manually."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running the Prompt Template demo application..."
python prompt_template_demo.py

#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting ZCB Pricing Tool Setup..."

# Create a virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating a new Python virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install or update requirements
echo "Installing dependencies from requirements.txt..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --default-timeout=100 --no-cache-dir
echo "Dependencies installed."

# Run the Streamlit application
echo "Launching the application in your default browser..."
# Streamlit automatically opens the browser by default
streamlit run src/main_page.py

# Deactivate the environment when Streamlit is closed
deactivate
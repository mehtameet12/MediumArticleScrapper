#!/bin/bash

# Navigate to the project directory (if not already there)
cd "$(dirname "$0")"

# Check if the virtual environment exists
if [ ! -d "mediumArticle/bin" ]; then
    echo "Creating virtual environment..."
    python -m venv mediumArticle
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source mediumArticle/bin/activate

# Install Python packages from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model 'en_core_web_sm'..."
python -m spacy download en_core_web_sm

echo "Setup complete! Virtual environment is activated."
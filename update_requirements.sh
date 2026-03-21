#!/bin/bash
# Activate virtual environment
source venv/bin/activate

# Install pipreqs if not installed
pip install --upgrade pipreqs

# Generate requirements.txt based on actual imports
pipreqs . --force

# Deactivate venv
deactivate

echo "requirements.txt updated!"
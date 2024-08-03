#!/bin/bash
# Update package list and install necessary libraries
apt-get update && apt-get install -y libgl1-mesa-glx

# Activate virtual environment
source /home/site/wwwroot/venv/bin/activate

# Start the application
gunicorn --chdir /home/site/wwwroot run:app
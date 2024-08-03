#!/bin/bash
# Update package list and install necessary libraries
apt-get update && apt-get install -y libgl1-mesa-glx

# Start the application
gunicorn --chdir /home/site/wwwroot run:app

import os
from ultralytics import YOLO

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the best.pt file
model_path = os.path.join(current_dir, 'best.pt')

# Load your YOLOv8 model
model = YOLO(model_path)

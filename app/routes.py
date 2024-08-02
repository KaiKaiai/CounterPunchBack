from flask import request, jsonify
from app import app
from app.models import model
import base64
import cv2
import numpy as np

def decode_image(image_base64):
    image_data = base64.b64decode(image_base64.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json
    image = decode_image(data['image'])
    results = model(image)

    # Do something with the results
    # For example, you can return the number of detected objects
    return jsonify({'detections': len(results)})

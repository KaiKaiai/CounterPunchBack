from flask import Blueprint, render_template, Response, request, jsonify
from extensions import db  # Import db from app.py
from datetime import datetime
from sqlalchemy import desc
import base64
import cv2
import numpy as np
from models import Match, FighterScore, Fighter
from inference_sdk import InferenceHTTPClient
main = Blueprint('main', __name__)

# Initialize InferenceHTTPClient
CLIENT = InferenceHTTPClient(api_url="https://detect.roboflow.com",
                             api_key="IhnzMIPA02sn9csVky59")

def decode_image(image_base64):
    image_data = base64.b64decode(image_base64.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def detect_objects(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    try:
        response = CLIENT.infer(img_base64, model_id="boxing-lelg6/3")
    except Exception as e:
        print(f"Error during inference: {e}")
        return frame
    
    for detection in response.get('predictions', []):
        try:
            x = detection['x']
            y = detection['y']
            width = detection['width']
            height = detection['height']
            
            x0 = int(x)
            y0 = int(y)
            x1 = int(x + width)
            y1 = int(y + height)
            
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            label = detection.get('class', 'object')
            confidence = detection.get('confidence', 0)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        except KeyError as e:
            print(f"KeyError: {e} in detection: {detection}")
        except ValueError as e:
            print(f"ValueError: {e} in detection: {detection}")
    
    return frame

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = detect_objects(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@main.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json
    image = decode_image(data['image'])
    results = CLIENT.infer(image, model_id="boxing-lelg6/3")
    return jsonify({'detections': results})

@main.route('/fighter', methods=['POST'])
def create_fighter():
    data = request.json
    new_fighter = Fighter(name=data['name'], country=data['country'], avatarURL=data['avatarURL'])
    db.session.add(new_fighter)
    db.session.commit()
    return jsonify({"id": new_fighter.id}), 201

@main.route('/match', methods=['POST'])
def create_match():
    data = request.json
    new_match = Match(
        title=data['title'],
        datetime=datetime.fromisoformat(data['datetime']),
        fighter1_id=data['fighter1']['id'],
        fighter2_id=data['fighter2']['id']
    )
    new_match.fighter1_score = FighterScore(thrown=0, hits=0)
    new_match.fighter2_score = FighterScore(thrown=0, hits=0)
    db.session.add(new_match)
    db.session.commit()
    return jsonify({"id": new_match.id}), 201

@main.route('/match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get_or_404(match_id)
    return jsonify({
        "id": match.id,
        "title": match.title,
        "datetime": match.datetime.isoformat(),
        "fighter1": {
            "id": match.fighter1.id,
            "name": match.fighter1.name,
            "country": match.fighter1.country,
            "avatarURL": match.fighter1.avatarURL
        },
        "fighter2": {
            "id": match.fighter2.id,
            "name": match.fighter2.name,
            "country": match.fighter2.country,
            "avatarURL": match.fighter2.avatarURL
        },
        "scores": {
            "fighter1": {
                "thrown": match.fighter1_score.thrown,
                "hits": match.fighter1_score.hits
            },
            "fighter2": {
                "thrown": match.fighter2_score.thrown,
                "hits": match.fighter2_score.hits
            }
        }
    })

@main.route('/match/<int:match_id>/score', methods=['PUT'])
def update_score(match_id):
    match = Match.query.get_or_404(match_id)
    data = request.json
    match.fighter1_score.thrown = data['scores']['fighter1']['thrown']
    match.fighter1_score.hits = data['scores']['fighter1']['hits']
    match.fighter2_score.thrown = data['scores']['fighter2']['thrown']
    match.fighter2_score.hits = data['scores']['fighter2']['hits']
    db.session.commit()
    return jsonify({"message": "Score updated successfully"}), 200

@main.route('/matches/recent', methods=['GET'])
def get_recent_matches():
    recent_matches = Match.query.order_by(desc(Match.datetime)).limit(5).all()
    matches_data = []
    for match in recent_matches:
        matches_data.append({
            "id": match.id,
            "title": match.title,
            "datetime": match.datetime.isoformat(),
            "fighter1": {
                "id": match.fighter1.id,
                "name": match.fighter1.name,
                "country": match.fighter1.country,
                "avatarURL": match.fighter1.avatarURL
            },
            "fighter2": {
                "id": match.fighter2.id,
                "name": match.fighter2.name,
                "country": match.fighter2.country,
                "avatarURL": match.fighter2.avatarURL
            },
            "scores": {
                "fighter1": {
                    "thrown": match.fighter1_score.thrown,
                    "hits": match.fighter1_score.hits
                },
                "fighter2": {
                    "thrown": match.fighter2_score.thrown,
                    "hits": match.fighter2_score.hits
                }
            }
        })
    return jsonify(matches_data), 200

@main.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
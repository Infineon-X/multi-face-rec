from flask import Flask, request, jsonify
import face_recognition
import pickle
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

# Load encodings (Vercel will include this file)
encodings_path = os.path.join(os.path.dirname(__file__), '..', 'encodings.pkl')

try:
    with open(encodings_path, "rb") as f:
        encodings = pickle.load(f)
    print(f"✅ Loaded {len(encodings['encodings'])} face encodings")
except Exception as e:
    print(f"❌ Error loading encodings: {e}")
    encodings = None

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """Face recognition endpoint"""
    
    if encodings is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded'
        }), 500
    
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image provided'
            }), 400
        
        image_file = request.files['image']
        image = Image.open(image_file.stream)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image_array = np.array(image)
        
        # Detect faces
        face_locations = face_recognition.face_locations(image_array)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        results = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(
                encodings["encodings"], 
                face_encoding,
                tolerance=0.6
            )
            
            name = "Unknown"
            confidence = 0
            
            if True in matches:
                face_distances = face_recognition.face_distance(
                    encodings["encodings"], 
                    face_encoding
                )
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = encodings["names"][best_match_index]
                    confidence = (1 - face_distances[best_match_index]) * 100
            
            results.append({
                'name': name,
                'confidence': float(confidence),
                'location': {
                    'top': int(top),
                    'right': int(right),
                    'bottom': int(bottom),
                    'left': int(left)
                }
            })
        
        return jsonify({
            'success': True,
            'faces': results,
            'total_faces': len(results),
            'image_size': {
                'width': image.width,
                'height': image.height
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# For Vercel serverless function
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)

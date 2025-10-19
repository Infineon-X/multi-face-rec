from flask import jsonify
import pickle
import os

def handler(request, response):
    """Health check endpoint for Vercel"""
    
    encodings_path = os.path.join(os.path.dirname(__file__), '..', 'encodings.pkl')
    
    try:
        with open(encodings_path, "rb") as f:
            encodings = pickle.load(f)
        
        return jsonify({
            'status': 'healthy',
            'faces_loaded': len(encodings['encodings']),
            'known_people': list(set(encodings['names']))
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

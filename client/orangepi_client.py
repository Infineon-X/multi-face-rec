#!/usr/bin/env python3

import requests
import cv2
import time
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Railway API endpoint
API_URL = os.getenv('API_URL', 'http://localhost:5001')

print(API_URL)

def capture_and_recognize():
    """Capture image and send to API for recognition"""
    
    print("📷 Capturing image...")

    # Prepare directory for test images: always resolve relative to repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_images_dir = os.path.join(repo_root, "client", "test_images")
    os.makedirs(test_images_dir, exist_ok=True)
    
    # Capture from camera
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Let camera warm up
    time.sleep(0.5)
    
    # Capture frame
    ret, frame = camera.read()
    camera.release()
    
    if not ret:
        print("❌ Error: Could not capture image")
        return

    # Save image temporarily
    image_path = os.path.join(test_images_dir, f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    print(image_path)
    cv2.imwrite(image_path, frame)
    print(f"✅ Image captured: {image_path}")
    
    # Send to API
    print("☁️  Sending to API for recognition...")
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            response = requests.post(f"{API_URL}/recognize", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print(f"\n{'='*50}")
                print(f"🎯 Recognition Results")
                print(f"{'='*50}")
                print(f"Total faces detected: {result['total_faces']}")
                print(f"Image size: {result['image_size']['width']}x{result['image_size']['height']}\n")
                
                for i, face in enumerate(result['faces'], 1):
                    print(f"Face {i}:")
                    print(f"  👤 Name: {face['name']}")
                    print(f"  📊 Confidence: {face['confidence']:.1f}%")
                    print(f"  📍 Location: ({face['location']['left']}, {face['location']['top']}) "
                          f"to ({face['location']['right']}, {face['location']['bottom']})")
                    print()
                
                return result
            else:
                print(f"❌ Recognition failed: {result.get('error')}")
        else:
            print(f"❌ Server error: Status {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up temp file
        if os.path.exists(image_path):
            os.remove(image_path)

def check_health():
    """Check if API is healthy"""
    health_url = f"{API_URL}/health"
    
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"📊 Faces loaded: {data['faces_loaded']}")
            print(f"👥 Known people: {', '.join(data['known_people'])}")
        else:
            print(f"❌ API unhealthy: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach API: {e}")

def continuous_monitoring(interval=5):
    """Continuously capture and recognize at intervals"""
    
    print(f"🔄 Starting continuous monitoring (every {interval} seconds)")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            capture_and_recognize()
            print(f"\n⏳ Waiting {interval} seconds...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n👋 Stopped monitoring")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "continuous":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            continuous_monitoring(interval)
        elif sys.argv[1] == "health":
            check_health()
    else:
        capture_and_recognize()

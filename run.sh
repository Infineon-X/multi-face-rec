#!/bin/bash

echo "=========================================="
echo "Face Recognition - Orange Pi Runner"
echo "=========================================="

# Pull latest changes from GitHub
echo "📥 Pulling latest model from GitHub..."
git pull origin main

if [ $? -ne 0 ]; then
    echo "❌ Git pull failed. Check your connection."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Virtual environment activation failed."
    exit 1
fi

# Check if encodings.pkl exists
if [ ! -f "encodings.pkl" ]; then
    echo "❌ encodings.pkl not found. Please train the model first."
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "Choose an option:"
echo "1) Run face recognition on test image"
echo "2) Run real-time camera recognition"
echo "3) Exit"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo "🔍 Running recognition on test images..."
        python3 recognize.py
        ;;
    2)
        echo "📹 Starting real-time camera recognition..."
        echo "Press 'q' to quit"
        python3 realtime_recognition.py
        ;;
    3)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"

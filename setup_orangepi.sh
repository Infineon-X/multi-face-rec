#!/bin/bash

echo "=========================================="
echo "Face Recognition - Orange Pi Setup"
echo "=========================================="

# Update system
echo "📦 Updating system packages..."
sudo apt-get update

# Install dependencies
echo "📦 Installing system dependencies..."
sudo apt-get install -y build-essential cmake gfortran git wget curl \
    graphicsmagick libgraphicsmagick1-dev libatlas-base-dev \
    libavcodec-dev libavformat-dev libboost-all-dev libgtk2.0-dev \
    libjpeg-dev liblapack-dev libswscale-dev pkg-config \
    python3-dev python3-numpy python3-pip python3-venv zip

# Clone repository (if not already cloned)
if [ ! -d "face-recognition-project" ]; then
    echo "📥 Cloning repository..."
    read -p "Enter GitHub repo URL: " repo_url
    git clone $repo_url face-recognition-project
    cd face-recognition-project
else
    echo "📁 Project directory exists, entering..."
    cd face-recognition-project
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3.10 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages (this may take 15-20 hours on Orange Pi One)..."
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x run.sh
chmod +x quick_run.sh
chmod +x quick_realtime.sh
chmod +x update.sh

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  ./run.sh              - Interactive menu"
echo "  ./quick_run.sh        - Quick test image recognition"
echo "  ./quick_realtime.sh   - Quick camera recognition"
echo "  ./update.sh           - Update model only"
echo ""

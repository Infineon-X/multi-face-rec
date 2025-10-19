#!/bin/bash

# Quick realtime - pull, activate, and run camera
git pull origin main
source venv/bin/activate
python3 realtime_recognition.py

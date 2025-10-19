#!/bin/bash

# Quick run - pull, activate, and run recognition
git pull origin main
source venv/bin/activate
python3 recognize.py

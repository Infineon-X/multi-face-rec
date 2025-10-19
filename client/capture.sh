#!/bin/bash

# Set your Vercel API URL
export API_URL="https://multi-face-rec.vercel.app/api/recognize"

echo "🎯 Face Recognition Client (Vercel)"
echo "====================================="
echo ""
echo "API: $API_URL"
echo ""
echo "1) Check API health"
echo "2) Single capture"
echo "3) Continuous monitoring (every 5 sec)"
echo "4) Continuous monitoring (every 30 sec)"
echo ""
read -p "Choose option [1-4]: " choice

case $choice in
    1)
        python3 orangepi_client.py health
        ;;
    2)
        python3 orangepi_client.py
        ;;
    3)
        python3 orangepi_client.py continuous 5
        ;;
    4)
        python3 orangepi_client.py continuous 30
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

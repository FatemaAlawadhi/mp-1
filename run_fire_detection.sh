#!/bin/bash

# Print header
echo "============================================="
echo "Fire Detection System"
echo "============================================="

# Create and activate virtual environment
echo -e "\n[1/3] Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo -e "\n[2/3] Installing dependencies..."
pip install --upgrade pip
pip install numpy opencv-python

# Run fire detection
echo -e "\n[3/3] Running fire detection..."
if python fire_detection/main.py; then
    echo "Fire detection completed successfully"
else
    echo "Error during fire detection!"
    exit 1
fi

echo -e "\n============================================="
echo "Process completed successfully!"
echo "Original image saved as: figures/png/original_fire.png"
echo "Heatmap saved as: figures/png/fire_heatmap.png"
echo "=============================================" 
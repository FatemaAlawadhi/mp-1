#!/bin/bash

# Print header
echo "============================================="
echo "Drought Detection System"
echo "============================================="

# Create and activate virtual environment
echo -e "\n[1/3] Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo -e "\n[2/3] Installing dependencies..."
pip install --upgrade pip
pip install numpy opencv-python scikit-image matplotlib

# Run drought detection
echo -e "\n[3/3] Running drought detection..."
if python drought_detection/main.py; then
    echo "Drought detection completed successfully"
else
    echo "Error during drought detection!"
    exit 1
fi

echo -e "\n============================================="
echo "Process completed successfully!"
echo "Original image saved as: figures/png/original_TCI.png"
echo "Drought visualization saved as: figures/png/drought_visualization.png"
echo "Drought severity heatmap saved as: figures/png/drought_severity_heatmap.png"
echo "Drought mask saved as: figures/png/drought_mask.png"
echo "============================================="

#!/bin/bash

# Print header
echo "============================================="
echo "Satellite Image Enhancement and Copper Detection"
echo "============================================="

# Create and activate virtual environment
echo -e "\n[1/5] Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install packages in batches
echo -e "\n[2/5] Installing dependencies..."
echo "Installing basic packages..."
pip install --upgrade pip
pip install numpy opencv-python scikit-image imagecodecs pywavelets

echo "Installing PyTorch..."
pip install torch torchvision

echo "Installing remaining packages..."
pip install tifffile matplotlib pandas scikit-learn

# Create necessary directories
echo -e "\n[3/5] Creating directory structure..."
mkdir -p figures
mkdir -p image_enhancement/models
mkdir -p copper_detection/models

# Check if input image exists
if [ ! -f "figures/TCI_COG.tiff" ]; then
    echo "Error: Input image 'figures/TCI_COG.tiff' not found!"
    exit 1
fi

# Run image enhancement
echo -e "\n[4/5] Running image enhancement..."
if python image_enhancement/main.py; then
    echo "Image enhancement completed successfully"
else
    echo "Error during image enhancement!"
    echo "Please check if all dependencies are installed correctly."
    echo "Try running: pip install pywavelets"
    exit 1
fi

# Run copper detection
echo -e "\n[5/5] Running copper detection..."
if python copper_detection/main.py; then
    echo "Copper detection completed successfully"
else
    echo "Error during copper detection!"
    exit 1
fi

# Convert TIFF images to PNG
echo -e "\n[6/6] Converting images to PNG format..."
if python utils/convert_to_png.py; then
    echo "Image conversion completed successfully"
else
    echo "Error during image conversion!"
    exit 1
fi

echo -e "\n============================================="
echo "Process completed successfully!"
echo "Enhanced image saved as: figures/enhanced_TCI_COG.tiff"
echo "Copper mask saved as: figures/copper_mask_TCI_COG.tiff"
echo "PNG versions saved in: figures/png/"
echo "=============================================" 
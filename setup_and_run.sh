#!/bin/bash

# Print header
echo "============================================="
echo "Satellite Image Enhancement"
echo "============================================="

# Create and activate virtual environment
echo -e "\n[1/4] Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install packages in batches
echo -e "\n[2/4] Installing dependencies..."
echo "Installing basic packages..."
pip install --upgrade pip
pip install numpy opencv-python scikit-image imagecodecs pywavelets

echo "Installing PyTorch..."
pip install torch torchvision

echo "Installing remaining packages..."
pip install tifffile matplotlib pandas scikit-learn

# Create necessary directories
echo -e "\n[3/4] Creating directory structure..."
mkdir -p figures
mkdir -p image_enhancement/models

# Check if input image exists
if [ ! -f "figures/TCI_COG.tiff" ]; then
    echo "Error: Input image 'figures/TCI_COG.tiff' not found!"
    exit 1
fi

# Run image enhancement
echo -e "\n[4/4] Running image enhancement..."
if python image_enhancement/main.py; then
    echo "Image enhancement completed successfully"
else
    echo "Error during image enhancement!"
    echo "Please check if all dependencies are installed correctly."
    echo "Try running: pip install pywavelets"
    exit 1
fi

# Convert TIFF images to PNG
echo -e "\n[5/5] Converting images to PNG format..."
if python utils/convert_to_png.py; then
    echo "Image conversion completed successfully"
else
    echo "Error during image conversion!"
    exit 1
fi

echo -e "\n============================================="
echo "Process completed successfully!"
echo "Enhanced image saved as: figures/enhanced_TCI_COG.tiff"
echo "PNG versions saved in: figures/png/"
echo "=============================================" 
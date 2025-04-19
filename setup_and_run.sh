#!/bin/bash

# Print header
echo "============================================="
echo "Satellite Image Processing Suite"
echo "============================================="

# Create and activate virtual environment
echo -e "\n[1/6] Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install packages in batches
echo -e "\n[2/6] Installing dependencies..."
echo "Installing basic packages..."
pip install --upgrade pip
pip install numpy opencv-python scikit-image imagecodecs pywavelets

echo "Installing PyTorch..."
pip install torch torchvision

echo "Installing remaining packages..."
pip install tifffile matplotlib pandas scikit-learn

# Create necessary directories
echo -e "\n[3/6] Creating directory structure..."
mkdir -p figures
mkdir -p image_enhancement/models
mkdir -p carbon_detection/models
mkdir -p fire_detection/models
mkdir -p drought_detection/models

# Download TCI_COG.tiff from Open Cosmos API if not present
if [ ! -f "figures/TCI_COG.tiff" ]; then
    echo "Downloading TCI_COG.tiff from Open Cosmos..."
    curl -L -o figures/TCI_COG.tiff "https://app.open-cosmos.com/api/data/v0/storage/full/hammer/l1b/2025/03/26/HAMMER_L1B_000001841_20250326105943_20250326105951_EFE6F97D/TCI_COG.tiff"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download TCI_COG.tiff!"
        exit 1
    fi
else
    echo "figures/TCI_COG.tiff already exists. Skipping download."
fi

# Fetch project data from Open Cosmos API
echo "Fetching project data from Open Cosmos API... (Token is already set in fetch_project_data.py)"
python3 fetch_project_data.py

# Ensure PYTHONPATH includes project root for all scripts
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Train and run image enhancement
echo -e "\n[4/6] Running image enhancement..."
# First train the TIFF enhancement model
if python image_enhancement/models/train_model.py; then
    echo "TIFF enhancement model trained successfully"
else
    echo "Error during model training!"
    exit 1
fi

# Run image enhancement with trained model
if python image_enhancement/main.py; then
    echo "Image enhancement completed successfully"
else
    echo "Error during image enhancement!"
    echo "Please check if all dependencies are installed correctly."
    echo "Try running: pip install pywavelets"
    exit 1
fi

echo "Step 2: Carbon Detection"
if python carbon_detection/main.py; then
    echo "Carbon detection completed successfully"
else
    echo "Error during carbon detection!"
    exit 1
fi

echo "Step 3: Fire Detection"
if python fire_detection/main.py; then
    echo "Fire detection completed successfully"
else
    echo "Error during fire detection!"
    exit 1
fi

echo "Step 4: Drought Detection"
cd drought_detection
if python main.py; then
    cd ..
    echo "Drought detection completed successfully"
else
    cd ..
    echo "Error during drought detection!"
    exit 1
fi

# Convert TIFF images to PNG
echo -e "\n[5/6] Converting images to PNG format..."
if python utils/convert_to_png.py; then
    echo "Image conversion completed successfully"
else
    echo "Error during image conversion!"
    exit 1
fi

echo -e "\n============================================="
echo "Process completed successfully!"
echo "Enhanced image saved as: figures/enhanced_TCI_COG.tiff"
echo "Carbon detection results saved in: figures/carbon_detection/"
echo "Fire detection results saved in: figures/fire_detection/"
echo "Drought detection results saved in: figures/drought_detection/"
echo "PNG versions saved in: figures/png/"
echo "============================================="
cal
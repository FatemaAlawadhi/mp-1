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
    TIFF_URL="https://app.open-cosmos.com/api/data/v0/storage/full/hammer/l1b/2025/03/26/HAMMER_L1B_000001841_20250326105943_20250326105951_EFE6F97D/TCI_COG.tiff"
    if [ -f ".oc_cookie" ]; then
        COOKIE=$(cat .oc_cookie)
        echo "Using cookies from .oc_cookie file for download."
        curl -L -H "Cookie: $COOKIE" -o figures/TCI_COG.tiff "$TIFF_URL"
    else
        echo "Using Bearer token for download."
        TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJEVTFPRFExTURZd09VWXpOMFV6UTBWRE5EZEJRVFJHTUVZMk1FTkdNa0pHUmtZMVJqQkdPQSJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLm9wZW4tY29zbW9zLmNvbS8iLCJzdWIiOiJhdXRoMHw2ODAyMDg4NmQ3YzA0Yjk3NDBiMDczNGEiLCJhdWQiOlsiaHR0cHM6Ly9iZWVhcHAub3Blbi1jb3Ntb3MuY29tIiwiaHR0cHM6Ly9vcGVuY29zbW9zLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3NDUwNDk5MzIsImV4cCI6MTc0NTEzNjMzMiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtc2Qgb3BzIGRhdGEgaGlsIHBvcnRhbCB1c2VyIHN1YmplY3QgcmVsYXRpb25zaGlwIHJvbGUgbWlzc2lvbiBwcm9ncmFtbWUgb3JnYW5pc2F0aW9uIGVwaGVtZXJpcyBvZmZsaW5lX2FjY2VzcyIsImF6cCI6InR0Zm1qdXV4QTNaWUs0SmtVeTRjRUluNDhrZnFrckV6In0.bE0buiYvMb6BC_-mBK8dA4uqolVdNOZ1Zndfg_i_KX9fbwnJw-YGveK7btISkAQcDaV3KC6gWReEqaq-9OMJ1Fs9wbq5f1LvyQ2TW6ZmxlZt9UXfMZy7qADRUeUaq-ETvcwBNJIsKG7oyqcEbKAVAMcibFHurzjD7hcm0vP-X6P2bH3_RCHhTpvPX1RbaqrUGSnJpzzRqjyJ9pZtwoTqlQOofIstPXb0sv6Cq5kfb822rfeQb0ab3oiCBWUjOK-dPd4iwJLmwSheNyOrovVLYbYrJi7oYVZB4S4Pg0qWtde-B6J1EL94lyWz8Up9h1taf7ZXx038AG1UiMaOGcERoQ"
        curl -L -H "Authorization: Bearer $TOKEN" -o figures/TCI_COG.tiff "$TIFF_URL"
    fi
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download TCI_COG.tiff!"
        exit 1
    fi
else
    echo "figures/TCI_COG.tiff already exists. Skipping download."
fi

# Fetch project data from Open Cosmos API
echo "Fetching project data from Open Cosmos API... [Token is already set in fetch_project_data.py]"
python3 fetch_project_data.py

# Ensure PYTHONPATH includes project root for all scripts
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Train and run image enhancement
echo -e "\n[4/6] Running image enhancement..."
# First train the TIFF enhancement model
if python image_enhancement/models/train_model.py; then
    echo "TIFF enhancement model trained successfully"
else
    echo "Error during TIFF enhancement model training!"
    exit 1
fi

if python image_enhancement/models/train_model.py; then
    echo "TIFF enhancement model trained successfully"
else
    echo "Error during TIFF enhancement model training!"
    exit 1
fi

if python image_enhancement/main.py; then
    echo "Image enhancement completed successfully"
else
    echo "Error during image enhancement!"
    echo "Please check if all dependencies are installed correctly."
    echo "Try running: pip install pywavelets"
    exit 1
fi

# Ensure enhanced_enhanced_TCI_COG.tiff exists
# if [ ! -f "figures/enhanced_enhanced_TCI_COG.tiff" ]; then
#     echo "enhanced_enhanced_TCI_COG.tiff not found. Running enhancement again on enhanced_TCI_COG.tiff..."
#     # Run enhancement again on the enhanced image
#     if python image_enhancement/main.py figures/enhanced_TCI_COG.tiff; then
#         echo "enhanced_enhanced_TCI_COG.tiff created successfully."
#     else
#         echo "Error: Could not create enhanced_enhanced_TCI_COG.tiff."
#         exit 1
#     fi
# fi

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
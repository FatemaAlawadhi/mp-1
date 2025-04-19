import os
from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).parent
FIGURES_DIR = BASE_DIR.parent / "figures"

# Input/Output file names
INPUT_IMAGE = "TCI_COG.tiff"

# Drought detection parameters
DROUGHT_PARAMS = {
    "ndvi_threshold": 0.3,       # Threshold for low vegetation (potential drought)
    "color_weight": 0.3,         # Weight for color-based detection
    "ndvi_weight": 0.7,          # Weight for NDVI-based detection
    "drought_threshold": 0.6,    # Threshold for classifying as drought
    "visualization_alpha": 0.6   # Transparency for visualization overlay
}

# If we had multispectral data, we would use these bands
# But for RGB-only images, we'll use approximations
BAND_INDICES = {
    "red": 0,
    "green": 1,
    "blue": 2,
    # NIR would be here if available
}
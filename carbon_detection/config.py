import os
from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).parent
FIGURES_DIR = BASE_DIR.parent / "figures"
UTILS_DIR = BASE_DIR / "utils"

# Input/Output file names
INPUT_IMAGE = "enhanced_TCI_COG.tiff"  # Using enhanced image as input
CARBON_MASK = "cARBON_mask_TCI_COG.tiff"

# Copper detection parameters
CARBON_DETECTION = {
    "spectral_bands": {
        "red": (600, 700),    # nm
        "green": (500, 600),  # nm
        "blue": (400, 500)    # nm
    },
    "threshold": 0.7,         # Classification threshold
    "min_area": 100,          # Minimum area for copper detection (pixels)
    "n_clusters": 2           # Number of clusters for K-means
} 
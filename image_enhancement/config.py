import os
from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).parent
FIGURES_DIR = BASE_DIR.parent / "figures"
UTILS_DIR = BASE_DIR / "utils"

# Input/Output file names
INPUT_IMAGE = "TCI_COG.tiff"
ENHANCED_IMAGE = "enhanced_TCI_COG.tiff"

# Image processing parameters
DENOISE_PARAMS = {
    "method": "wavelet",  # Options: "wavelet" or "nlmeans"
    "sigma": 0.1,         # Noise standard deviation
    "wavelet": 'db1',     # Wavelet type
    "mode": 'soft'        # Thresholding mode
}

ENHANCEMENT_PARAMS = {
    "upscale_factor": 4,
    "contrast_stretch": True,
    "sharpening_kernel": [[-1, -1, -1],
                         [-1,  9, -1],
                         [-1, -1, -1]]
}

# Model paths
MODEL_DIR = BASE_DIR / "models"
REALESRGAN_MODEL = MODEL_DIR / "RealESRGAN_x4plus.pth" 
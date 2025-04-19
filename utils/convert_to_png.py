import os
from pathlib import Path
import tifffile
import cv2
import numpy as np

def convert_tiff_to_png(input_path, output_path):
    """Convert TIFF image to PNG format."""
    # Read TIFF image
    image = tifffile.imread(input_path)
    
    # Normalize image to 0-255 range if needed
    if image.dtype != np.uint8:
        # Normalize to 0-1 range
        normalized = (image - np.min(image)) / (np.max(image) - np.min(image))
        # Convert to 0-255 range
        image = (normalized * 255).astype(np.uint8)
    
    # Save as PNG
    cv2.imwrite(output_path, image)
    print(f"Converted {input_path} to {output_path}")

def main():
    # Create output directory
    output_dir = Path("figures/png")
    output_dir.mkdir(exist_ok=True)
    
    # List of files to convert
    files_to_convert = [
        "TCI_COG.tiff",
        "enhanced_TCI_COG.tiff",
        "enhanced_enhanced_TCI_COG.tiff",
        "CARBON_mask_TCI_COG.tiff"
    ]
    
    # Convert each file
    for filename in files_to_convert:
        input_path = Path("figures") / filename
        if input_path.exists():
            output_path = output_dir / f"{Path(filename).stem}.png"
            convert_tiff_to_png(input_path, output_path)
        else:
            print(f"Warning: {input_path} not found!")

if __name__ == "__main__":
    main() 
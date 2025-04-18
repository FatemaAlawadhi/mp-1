import os
from pathlib import Path
from config import *
from utils.carbon_detection import (
    load_image,
    save_image,
    process_image
)

def main():
    # Create output directory if it doesn't exist
    FIGURES_DIR.mkdir(exist_ok=True)
    
    # Load enhanced image
    input_path = FIGURES_DIR / INPUT_IMAGE
    print(f"Loading enhanced image from {input_path}")
    image = load_image(input_path)
    
    # Process image for copper detection
    print("Processing image for carbon detection...")
    carbon_mask = process_image(image, CARBON_DETECTION)
    
    # Save copper mask
    output_path = FIGURES_DIR / CARBON_MASK
    print(f"Saving copper mask to {output_path}")
    save_image(carbon_mask, output_path)
    
    print("carbon detection complete!")

if __name__ == "__main__":
    main() 
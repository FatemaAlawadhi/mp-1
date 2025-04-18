import os
from pathlib import Path
from config import *
from utils.copper_detection import (
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
    print("Processing image for copper detection...")
    copper_mask = process_image(image, COPPER_DETECTION)
    
    # Save copper mask
    output_path = FIGURES_DIR / COPPER_MASK
    print(f"Saving copper mask to {output_path}")
    save_image(copper_mask, output_path)
    
    print("Copper detection complete!")

if __name__ == "__main__":
    main() 
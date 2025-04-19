import os
import numpy as np
from pathlib import Path
from config import *
from utils.carbon_detection import (
    load_image,
    save_image,
    process_image,
    create_carbon_heatmap
)
from utils.load_project_data import load_project_data

def main():
    # Load project data from API
    project_data = load_project_data()
    if project_data is not None:
        print("[INFO] Project data loaded from project_data.json. Keys:", list(project_data.keys()))
    else:
        print("[WARN] Project data not available. Proceeding without API data.")

    # Create output directory if it doesn't exist
    FIGURES_DIR.mkdir(exist_ok=True)
    carbon_dir = FIGURES_DIR / "carbon_detection"
    carbon_dir.mkdir(exist_ok=True)
    png_dir = FIGURES_DIR / "png"
    png_dir.mkdir(exist_ok=True)
    
    # Load enhanced image
    input_path = FIGURES_DIR / INPUT_IMAGE
    print(f"Loading enhanced image from {input_path}")
    image = load_image(input_path)
    
    # Process image for carbon detection
    print("Processing image for carbon detection...")
    classified, mask, image_norm, original_image = process_image(image, CARBON_DETECTION)
    
    # Save carbon mask
    output_path = FIGURES_DIR / CARBON_MASK
    print(f"Saving carbon mask to {output_path}")
    save_image(classified, output_path)
    
    # Create and save carbon heatmap (similar to drought severity heatmap)
    heatmap_path = png_dir / "carbon_heatmap.png"
    print(f"Creating carbon heatmap at {heatmap_path}")
    create_carbon_heatmap(image_norm, mask, heatmap_path, CARBON_DETECTION['heatmap_colormap'])
    
    # Save raw mask for visualization
    mask_path = png_dir / "carbon_mask.png"
    print(f"Saving carbon mask to {mask_path}")
    save_image(mask, mask_path)
    
    # Calculate carbon coverage statistics
    carbon_pixels = np.sum(mask > 0)
    total_pixels = mask.size
    carbon_percentage = (carbon_pixels / total_pixels) * 100
    
    print("Carbon detection complete!")
    print(f"Carbon coverage: {carbon_percentage:.2f}% of the image")
    print(f"Carbon mask saved to {output_path}")
    print(f"Carbon heatmap saved to {heatmap_path}")

if __name__ == "__main__":
    main()
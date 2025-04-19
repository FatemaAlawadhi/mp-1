import os
import gc
from pathlib import Path
from config import *
from utils.image_processing import (
    load_image,
    save_image,
    preprocess_image,
    upscale_image,
    sharpen_image
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
    
    try:
        # Load input image
        input_path = FIGURES_DIR / INPUT_IMAGE
        print(f"Loading image from {input_path}")
        image = load_image(input_path, max_size=2048)  # Limit maximum dimension to 2048 pixels
        
        # Preprocess image
        print("Preprocessing image...")
        preprocessed = preprocess_image(image, DENOISE_PARAMS)
        
        # Free memory
        del image
        gc.collect()
        
        # Upscale image
        print("Upscaling image...")
        upscaled = upscale_image(preprocessed, scale_factor=ENHANCEMENT_PARAMS['upscale_factor'])
        
        # Free memory
        del preprocessed
        gc.collect()
        
        # Sharpen image
        print("Sharpening image...")
        sharpened = sharpen_image(upscaled, ENHANCEMENT_PARAMS['sharpening_kernel'])
        
        # Free memory
        del upscaled
        gc.collect()
        
        # Save enhanced image
        output_path = FIGURES_DIR / ENHANCED_IMAGE
        print(f"Saving enhanced image to {output_path}")
        save_image(sharpened, output_path)
        
        print("Image enhancement complete!")
        
    except Exception as e:
        print(f"Error during image processing: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
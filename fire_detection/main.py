import cv2
import numpy as np
import os
from pathlib import Path
from skimage import io

def create_heatmap(image):
    # Convert to float32 for processing
    img_float = image.astype(np.float32)
    
    # Calculate intensity based on RGB values
    # Enhanced fire detection using multiple color ratios
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]
    
    # Calculate multiple fire indicators
    # 1. Red dominance ratio
    red_ratio = red_channel / (green_channel + blue_channel + 1)
    
    # 2. Red-Green difference
    rg_diff = red_channel - green_channel
    
    # 3. Red-Blue difference
    rb_diff = red_channel - blue_channel
    
    # 4. Combined intensity (weighted sum of indicators)
    intensity = (2 * red_ratio + rg_diff + rb_diff) / 4
    
    # Normalize intensity to 0-1 range
    intensity = np.clip(intensity, 0, 1)
    
    # Apply threshold to identify fire regions
    fire_mask = intensity > 0.6
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5,5), np.uint8)
    fire_mask = cv2.morphologyEx(fire_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
    
    # Create heatmap using yellow to red colormap
    heatmap = np.zeros_like(image)
    
    # Yellow (255, 255, 0) to Red (255, 0, 0)
    heatmap[:, :, 0] = 255  # Red channel always 255
    heatmap[:, :, 1] = 255 * (1 - intensity)  # Green channel decreases with intensity
    heatmap[:, :, 2] = 0  # Blue channel always 0
    
    # Blend original image with heatmap
    alpha = 0.5  # Transparency of heatmap
    result = cv2.addWeighted(image, 1 - alpha, heatmap.astype(np.uint8), alpha, 0)
    
    # Overlay fire regions with higher intensity
    result[fire_mask > 0] = [255, 0, 0]  # Mark detected fire regions in red
    
    return result, intensity, fire_mask

def main():
    # Create figures directory if it doesn't exist
    os.makedirs('figures', exist_ok=True)
    os.makedirs('figures/png', exist_ok=True)
    
    # Read input image
    input_path = 'figures/TCI_COG.tiff'
    if not os.path.exists(input_path):
        print(f"Error: Input image {input_path} not found!")
        return
    
    # Read the TIFF image using skimage
    image = io.imread(input_path)
    
    # Convert to RGB if needed (some TIFFs might be in different color spaces)
    if len(image.shape) == 2:  # If grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:  # If RGBA
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # Create heatmap
    heatmap_image, intensity, fire_mask = create_heatmap(image)
    
    # Save original and heatmap as PNG
    cv2.imwrite('figures/png/original_TCI.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.imwrite('figures/png/fire_heatmap.png', cv2.cvtColor(heatmap_image, cv2.COLOR_RGB2BGR))
    cv2.imwrite('figures/png/fire_mask.png', fire_mask * 255)
    
    # Calculate and print fire statistics
    fire_pixels = np.sum(fire_mask)
    total_pixels = fire_mask.size
    fire_percentage = (fire_pixels / total_pixels) * 100
    
    print("Fire detection completed successfully!")
    print(f"Fire coverage: {fire_percentage:.2f}% of the image")
    print("Original image saved as: figures/png/original_TCI.png")
    print("Heatmap saved as: figures/png/fire_heatmap.png")
    print("Fire mask saved as: figures/png/fire_mask.png")

if __name__ == "__main__":
    main() 
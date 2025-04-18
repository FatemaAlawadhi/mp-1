import cv2
import numpy as np
import os
from pathlib import Path

def create_heatmap(image):
    # Convert to float32 for processing
    img_float = image.astype(np.float32)
    
    # Calculate intensity based on RGB values
    # Higher red values and lower green/blue values indicate potential fire
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]
    
    # Calculate fire intensity (higher values = more likely fire)
    # Formula: (2*R - G - B) / (R + G + B + 1)
    intensity = (2 * red_channel - green_channel - blue_channel) / (red_channel + green_channel + blue_channel + 1)
    
    # Normalize intensity to 0-1 range
    intensity = np.clip(intensity, 0, 1)
    
    # Create heatmap using yellow to red colormap
    heatmap = np.zeros_like(image)
    
    # Yellow (255, 255, 0) to Red (255, 0, 0)
    heatmap[:, :, 0] = 255  # Red channel always 255
    heatmap[:, :, 1] = 255 * (1 - intensity)  # Green channel decreases with intensity
    heatmap[:, :, 2] = 0  # Blue channel always 0
    
    # Blend original image with heatmap
    alpha = 0.5  # Transparency of heatmap
    result = cv2.addWeighted(image, 1 - alpha, heatmap.astype(np.uint8), alpha, 0)
    
    return result, intensity

def main():
    # Create figures directory if it doesn't exist
    os.makedirs('figures', exist_ok=True)
    os.makedirs('figures/png', exist_ok=True)
    
    # Read input image
    input_path = 'figures/fire.png'
    if not os.path.exists(input_path):
        print(f"Error: Input image {input_path} not found!")
        return
    
    # Read the PNG image
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    
    # Create heatmap
    heatmap_image, intensity = create_heatmap(image)
    
    # Save original and heatmap as PNG
    cv2.imwrite('figures/png/original_fire.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.imwrite('figures/png/fire_heatmap.png', cv2.cvtColor(heatmap_image, cv2.COLOR_RGB2BGR))
    
    print("Fire detection completed successfully!")
    print("Original image saved as: figures/png/original_fire.png")
    print("Heatmap saved as: figures/png/fire_heatmap.png")

if __name__ == "__main__":
    main() 
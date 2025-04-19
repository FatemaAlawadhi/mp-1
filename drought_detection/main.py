import cv2
import numpy as np
import os
from pathlib import Path
from skimage import io
import matplotlib.pyplot as plt
from config import DROUGHT_PARAMS, FIGURES_DIR, INPUT_IMAGE  # Use relative import instead
def calculate_ndvi_approximation(image):
    """
    Calculate an approximation of NDVI using RGB channels.
    This is a simplified approach since true NDVI requires NIR band.
    """
    # Extract channels
    red_channel = image[:, :, 0].astype(float)
    green_channel = image[:, :, 1].astype(float)
    blue_channel = image[:, :, 2].astype(float)
    
    # Calculate pseudo-NDVI (using green as NIR approximation)
    # True NDVI = (NIR - Red) / (NIR + Red)
    # Pseudo-NDVI = (Green - Red) / (Green + Red)
    epsilon = 1e-10  # Avoid division by zero
    pseudo_ndvi = (green_channel - red_channel) / (green_channel + red_channel + epsilon)
    
    # Normalize to 0-1 range
    pseudo_ndvi = (pseudo_ndvi + 1) / 2
    
    return pseudo_ndvi

def detect_drought(image):
    """
    Detect potential drought areas based on vegetation indices and color analysis.
    Returns a drought severity map and mask of potential drought areas.
    """
    # Calculate pseudo-NDVI
    pseudo_ndvi = calculate_ndvi_approximation(image)
    
    # Calculate color-based dryness index
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hue = img_hsv[:, :, 0].astype(float) / 179.0  # Normalize to 0-1
    saturation = img_hsv[:, :, 1].astype(float) / 255.0
    value = img_hsv[:, :, 2].astype(float) / 255.0
    
    # Brown/yellow colors have hue around 0.05-0.15 (normalized)
    # High value, medium-low saturation indicates dry soil/vegetation
    brown_mask = ((hue >= 0.05) & (hue <= 0.15) & (saturation >= 0.2) & (value >= 0.4))
    
    # Combine indices for drought detection
    # Low NDVI and brown/yellow color indicates potential drought
    drought_severity = (1 - pseudo_ndvi) * DROUGHT_PARAMS["ndvi_weight"] + brown_mask.astype(float) * DROUGHT_PARAMS["color_weight"]
    
    # Threshold for drought areas
    drought_mask = drought_severity > DROUGHT_PARAMS["drought_threshold"]
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    drought_mask = cv2.morphologyEx(drought_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    drought_mask = cv2.morphologyEx(drought_mask, cv2.MORPH_CLOSE, kernel)
    
    # Create drought visualization
    drought_viz = np.zeros_like(image)
    
    # Use a color gradient from yellow to brown for severity
    drought_viz[:, :, 0] = np.clip(150 + 105 * drought_severity, 0, 255)  # R
    drought_viz[:, :, 1] = np.clip(150 - 150 * drought_severity, 0, 255)  # G
    drought_viz[:, :, 2] = np.zeros_like(drought_severity)  # B
    
    # Blend original image with drought visualization
    alpha = DROUGHT_PARAMS["visualization_alpha"]
    result = cv2.addWeighted(image, 1 - alpha, drought_viz.astype(np.uint8), alpha, 0)
    
    # Highlight severe drought areas
    result[drought_mask > 0] = [165, 42, 42]  # Mark detected severe drought in brown
    
    return result, drought_severity, drought_mask

def main():
    # Create output directories if they don't exist
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR / "png", exist_ok=True)
    os.makedirs(FIGURES_DIR / "drought_detection", exist_ok=True)
    
    # Read input image
    input_path = FIGURES_DIR / INPUT_IMAGE
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
    
    # Detect drought
    drought_image, drought_severity, drought_mask = detect_drought(image)
    
    # Save original and drought visualization as PNG
    cv2.imwrite(str(FIGURES_DIR / "png" / "original_TCI.png"), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.imwrite(str(FIGURES_DIR / "png" / "drought_visualization.png"), cv2.cvtColor(drought_image, cv2.COLOR_RGB2BGR))
    
    # Save drought severity as heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(drought_severity, cmap='YlOrBr')
    plt.colorbar(label='Drought Severity')
    plt.title('Drought Severity Index')
    plt.savefig(str(FIGURES_DIR / "png" / "drought_severity_heatmap.png"))
    plt.close()
    
    # Save drought mask
    cv2.imwrite(str(FIGURES_DIR / "png" / "drought_mask.png"), drought_mask * 255)
    
    # Calculate and print drought statistics
    drought_pixels = np.sum(drought_mask)
    total_pixels = drought_mask.size
    drought_percentage = (drought_pixels / total_pixels) * 100
    
    print("Drought detection completed successfully!")
    print(f"Potential drought coverage: {drought_percentage:.2f}% of the image")
    print("Original image saved as: figures/png/original_TCI.png")
    print("Drought visualization saved as: figures/png/drought_visualization.png")
    print("Drought severity heatmap saved as: figures/png/drought_severity_heatmap.png")
    print("Drought mask saved as: figures/png/drought_mask.png")

if __name__ == "__main__":
    main()
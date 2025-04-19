import numpy as np
from skimage import measure
from sklearn.cluster import KMeans
import tifffile
import matplotlib.pyplot as plt
import cv2

def load_image(image_path):
    """Load image using tifffile for TIFF images."""
    return tifffile.imread(image_path)

def save_image(image, output_path):
    """Save image using tifffile for TIFF images."""
    tifffile.imwrite(output_path, image)

def extract_spectral_features(image, spectral_bands):
    """Extract spectral features from the image."""
    features = []
    
    # For grayscale images, we'll use intensity values
    if len(image.shape) == 2:  # Grayscale image
        features.extend([
            np.mean(image),
            np.std(image),
            np.percentile(image, 25),  # First quartile
            np.percentile(image, 75)   # Third quartile
        ])
    else:  # RGB image
        for band_name, (start, end) in spectral_bands.items():
            band_data = image[:, :, :]  # All channels
            features.extend([
                np.mean(band_data),
                np.std(band_data)
            ])
    
    return np.array(features)

def detect_carbon_regions(image, threshold=0.5, min_area=50):
    """Detect carbon-rich regions in the image."""
    # Convert image to appropriate format if needed
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    
    # Normalize image
    image_norm = (image - np.min(image)) / (np.max(image) - np.min(image))
    
    # Apply threshold
    binary = image_norm > threshold
    
    # Find connected components
    labels = measure.label(binary)
    
    # Filter regions by area
    regions = measure.regionprops(labels)
    valid_regions = [r for r in regions if r.area >= min_area]
    
    # Create mask
    mask = np.zeros_like(image, dtype=np.uint8)
    for region in valid_regions:
        mask[labels == region.label] = 255
    
    return mask, image_norm  # Return normalized image for heatmap

def classify_carbon_regions(image, n_clusters=3):
    """Classify regions using K-means clustering."""
    # Reshape image for clustering
    h, w = image.shape[:2]
    X = image.reshape(-1, 1)
    
    # Apply K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    
    # Reshape back to image
    return labels.reshape(h, w)

def create_carbon_heatmap(image_norm, mask, output_path, colormap='YlOrBr'):
    """
    Create a standalone heatmap visualization of carbon regions,
    similar to the drought severity heatmap.
    """
    # Create a heatmap where the intensity is based on the normalized image values
    # but only in regions where the mask is positive
    heatmap_data = np.zeros_like(image_norm)
    heatmap_data[mask > 0] = image_norm[mask > 0]
    
    # Create the heatmap visualization
    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap_data, cmap=colormap)
    plt.colorbar(label='Carbon Intensity')
    plt.title('Carbon Concentration Heatmap')
    plt.axis('off')  # Hide axes for cleaner visualization
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return heatmap_data

def process_image(image, params):
    """Complete carbon detection pipeline."""
    # Extract spectral features
    features = extract_spectral_features(image, params['spectral_bands'])
    
    # Detect carbon regions
    mask, image_norm = detect_carbon_regions(
        image,
        threshold=params['threshold'],
        min_area=params['min_area']
    )
    
    # Classify regions
    classified = classify_carbon_regions(
        mask,
        n_clusters=params['n_clusters']
    )
    
    return classified, mask, image_norm, image  # Return original image too
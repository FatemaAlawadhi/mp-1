import cv2
import numpy as np
from skimage import exposure, restoration
import tifffile

def load_image(image_path, max_size=2048):
    """Load image using tifffile for TIFF images and resize if too large."""
    image = tifffile.imread(image_path)
    
    # Get current dimensions
    height, width = image.shape[:2]
    
    # Calculate scaling factor if image is too large
    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        new_height = int(height * scale)
        new_width = int(width * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return image

def save_image(image, output_path):
    """Save image using tifffile for TIFF images."""
    tifffile.imwrite(output_path, image)

def convert_to_grayscale(image):
    """Convert RGB image to grayscale."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image

def denoise_image(image, method='wavelet', **kwargs):
    """Denoise image using specified method."""
    if method == 'wavelet':
        # Extract wavelet-specific parameters
        sigma = kwargs.pop('sigma', 0.1)
        wavelet = kwargs.pop('wavelet', 'db1')
        mode = kwargs.pop('mode', 'soft')
        
        # Process in chunks if image is large
        if image.size > 1000000:  # 1 million pixels
            chunks = np.array_split(image, 4)  # Split into 4 chunks
            denoised_chunks = []
            for chunk in chunks:
                denoised = restoration.denoise_wavelet(
                    chunk,
                    sigma=sigma,
                    wavelet=wavelet,
                    mode=mode,
                    channel_axis=None,
                    **kwargs
                )
                denoised_chunks.append(denoised)
            return np.concatenate(denoised_chunks)
        else:
            return restoration.denoise_wavelet(
                image,
                sigma=sigma,
                wavelet=wavelet,
                mode=mode,
                channel_axis=None,
                **kwargs
            )
    elif method == 'nlmeans':
        return cv2.fastNlMeansDenoising(image, None, **kwargs)
    else:
        raise ValueError(f"Unknown denoising method: {method}")

def enhance_contrast(image):
    """Enhance image contrast using histogram equalization."""
    return exposure.rescale_intensity(image)

def sharpen_image(image, kernel):
    """Sharpen image using specified kernel."""
    return cv2.filter2D(image, -1, np.array(kernel))

import os
import sys

# Add the project root directory to Python path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from image_enhancement.utils.esrgan import ESRGANUpscaler
from image_enhancement.config import REALESRGAN_MODEL, ESRGAN_PARAMS
from pathlib import Path

_esrgan_instance = None

def get_esrgan():
    """Singleton pattern to reuse ESRGAN model instance."""
    global _esrgan_instance
    if _esrgan_instance is None:
        _esrgan_instance = ESRGANUpscaler(REALESRGAN_MODEL)
    return _esrgan_instance

def upscale_image(image, scale_factor=4):
    """Upscale image using Real-ESRGAN."""
    try:
        # Get ESRGAN instance
        upscaler = get_esrgan()
        
        # Use ESRGAN for upscaling
        return upscaler.upscale(
            image,
            tile_size=ESRGAN_PARAMS["tile_size"],
            tile_padding=ESRGAN_PARAMS["tile_padding"]
        )
    except RuntimeError as e:
        print(f"Error: {str(e)}")
        raise

def preprocess_image(image, denoise_params):
    """Complete preprocessing pipeline."""
    # Convert to grayscale
    gray = convert_to_grayscale(image)
    
    # Denoise
    denoised = denoise_image(gray, **denoise_params)
    
    # Enhance contrast
    enhanced = enhance_contrast(denoised)
    
    return enhanced

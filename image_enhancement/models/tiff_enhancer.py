import cv2
import numpy as np
from skimage import exposure, restoration
from skimage.filters import unsharp_mask

class TIFFEnhancer:
    def __init__(self, denoise_weight=0.1, contrast_limit=0.3, sharpness=1.0):
        self.denoise_weight = denoise_weight
        self.contrast_limit = contrast_limit
        self.sharpness = sharpness
        
    def enhance_tiff(self, image):
        """
        Enhance a TIFF image using multiple image processing techniques
        Args:
            image: Input numpy array
        Returns:
            Enhanced image as numpy array
        """
        # Ensure float32 format
        image = image.astype(np.float32)
        
        # Normalize to [0, 1]
        image = (image - image.min()) / (image.max() - image.min())
        
        # Apply denoising
        denoised = restoration.denoise_wavelet(image, 
                                             sigma=self.denoise_weight,
                                             mode='soft',
                                             wavelet='db1',
                                             channel_axis=None)
        
        # Enhance contrast using adaptive histogram equalization
        enhanced = exposure.equalize_adapthist(denoised, 
                                             clip_limit=self.contrast_limit)
        
        # Apply unsharp masking for sharpness
        sharpened = unsharp_mask(enhanced, 
                                radius=1, 
                                amount=self.sharpness)
        
        return sharpened

def prepare_image(image):
    """
    Prepare image for enhancement
    Args:
        image: Input numpy array
    Returns:
        Normalized numpy array
    """
    # Convert to float32
    image = image.astype(np.float32)
    # Normalize to [0, 1]
    image = (image - image.min()) / (image.max() - image.min())
    return image

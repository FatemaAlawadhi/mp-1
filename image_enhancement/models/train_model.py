import os
import tifffile
import numpy as np
from tiff_enhancer import TIFFEnhancer

def enhance_images(input_dir='figures'):
    """Process all TIFF images in the input directory"""
    # Initialize enhancer
    enhancer = TIFFEnhancer(denoise_weight=0.1, contrast_limit=0.3, sharpness=1.0)
    
    # Get all TIFF files
    tiff_files = [f for f in os.listdir(input_dir) if f.endswith('.tiff')]
    
    if not tiff_files:
        print(f"No TIFF files found in {input_dir}")
        return
    
    print(f"Found {len(tiff_files)} TIFF files to process")
    
    # Process each file
    for filename in tiff_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(input_dir, f'enhanced_{filename}')
        
        print(f"Processing {filename}...")
        
        # Load and enhance image
        try:
            image = tifffile.imread(input_path)
            enhanced = enhancer.enhance_tiff(image)
            
            # Save enhanced image
            tifffile.imwrite(output_path, 
                           (enhanced * 65535).astype(np.uint16))  # Convert back to 16-bit
            print(f"Saved enhanced image to {output_path}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == '__main__':
    enhance_images()

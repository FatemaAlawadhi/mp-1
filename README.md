# Satellite Image Enhancement and Carbon Detection

This project focuses on enhancing satellite imagery and detecting Carbon-rich areas using advanced image processing techniques.

## Project Structure
```
.
├── figures/                 # Input/output images
├── image_enhancement/      # Image enhancement module
│   ├── utils/             # Enhancement utilities
│   ├── config.py          # Enhancement parameters
│   └── main.py           # Enhancement pipeline
├── Carbon_detection/      # Carbon detection module
│   ├── utils/            # Detection utilities
│   ├── config.py         # Detection parameters
│   └── main.py          # Detection pipeline
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Features
1. Image Enhancement Module
   - Grayscale conversion
   - Denoising using wavelet transform
   - Super-resolution using Real-ESRGAN
   - Contrast enhancement
   - Edge sharpening
   
2. Carbon Detection Module
   - Spectral analysis
   - Feature extraction
   - Classification
   - Region detection

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download Real-ESRGAN model:
```bash
python image_enhancement/scripts/download_models.py
```

## Usage
1. Place your input image in the `figures` directory
2. Run the enhancement pipeline:
```bash
python image_enhancement/main.py
```
3. Run the Carbon detection pipeline:
```bash
python Carbon_detection/main.py
```

## Output
The processed images will be saved in the `figures` directory with appropriate naming conventions:
- Enhanced image: `enhanced_TCI_COG.tiff`
- Carbon detection mask: `Carbon_mask_TCI_COG.tiff`

## Dependencies
- OpenCV
- scikit-image
- PyTorch
- Real-ESRGAN
- NumPy
- Matplotlib
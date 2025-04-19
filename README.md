# Satellite Image Analysis and Environmental Monitoring

This project focuses on analyzing satellite imagery for environmental monitoring, including drought detection, fire detection, and carbon detection using advanced image processing techniques.

## Project Structure
```
.
├── image_enhancement/      # Image enhancement module
├── drought_detection/      # Drought detection module
├── fire_detection/        # Fire detection module
├── carbon_detection/      # Carbon detection module
├── utils/                 # Shared utilities
├── requirements.txt       # Project dependencies
├── setup_and_run.sh      # Setup and run script (Linux/Mac)
├── setup_and_run.bat     # Setup and run script (Windows)
├── run_drought_detection.sh  # Drought detection script
├── run_fire_detection.sh     # Fire detection script
└── README.md             # Project documentation
```

## Features
1. Image Enhancement Module
   - Image preprocessing
   - Quality improvement
   - Feature enhancement

2. Drought Detection Module
   - Vegetation analysis
   - Soil moisture assessment
   - Drought severity classification

3. Fire Detection Module
   - Thermal anomaly detection
   - Smoke plume identification
   - Fire risk assessment

4. Carbon Detection Module
   - Spectral analysis
   - Carbon-rich area identification
   - Environmental impact assessment

## Setup
1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Run the setup script:
- On Linux/Mac:
```bash
./setup_and_run.sh
```
- On Windows:
```bash
setup_and_run.bat
```

3. The setup script will:
   - Create a virtual environment
   - Install required dependencies
   - Download necessary models
   - Configure the environment

## Usage
1. Run drought detection:
```bash
./run_drought_detection.sh
```

2. Run fire detection:
```bash
./run_fire_detection.sh
```

3. Run carbon detection:
```bash
python carbon_detection/main.py
```

## Output
The processed results will be saved in their respective module directories with appropriate naming conventions and formats.

## Dependencies
- OpenCV
- scikit-image
- PyTorch
- NumPy
- Matplotlib
- TensorFlow
- GDAL
- Rasterio
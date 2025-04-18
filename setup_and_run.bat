@echo off
setlocal enabledelayedexpansion

:: Print header
echo =============================================
echo Satellite Image Enhancement, Carbon and Fire Detection
echo =============================================

:: Create and activate virtual environment
echo.
echo [1/5] Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Install packages in batches
echo.
echo [2/5] Installing dependencies...
echo Installing basic packages...
pip install --upgrade pip
pip install numpy opencv-python scikit-image imagecodecs pywavelets

echo Installing PyTorch...
pip install torch torchvision

echo Installing remaining packages...
pip install tifffile matplotlib pandas scikit-learn

:: Create necessary directories
echo.
echo [3/5] Creating directory structure...
if not exist figures mkdir figures
if not exist image_enhancement\models mkdir image_enhancement\models
if not exist Carbon_detection\models mkdir Carbon_detection\models
if not exist fire_detection\models mkdir fire_detection\models

:: Check if input image exists
if not exist "figures\TCI_COG.tiff" (
    echo Error: Input image 'figures\TCI_COG.tiff' not found!
    exit /b 1
)

:: Run image enhancement
echo.
echo [4/7] Running image enhancement...
python image_enhancement\main.py
if errorlevel 1 (
    echo Error during image enhancement!
    echo Please check if all dependencies are installed correctly.
    echo Try running: pip install pywavelets
    exit /b 1
) else (
    echo Image enhancement completed successfully
)

:: Run Carbon detection
echo.
echo [5/7] Running Carbon detection...
python carbon_detection\main.py
if errorlevel 1 (
    echo Error during Carbon detection!
    exit /b 1
) else (
    echo Carbon detection completed successfully
)

:: Run Fire detection
echo.
echo [6/7] Running Fire detection...
python fire_detection\main.py
if errorlevel 1 (
    echo Error during Fire detection!
    exit /b 1
) else (
    echo Fire detection completed successfully
)

:: Convert TIFF images to PNG
echo.
echo [7/7] Converting images to PNG format...
python utils\convert_to_png.py
if errorlevel 1 (
    echo Error during image conversion!
    exit /b 1
) else (
    echo Image conversion completed successfully
)

echo.
echo =============================================
echo Process completed successfully!
echo Enhanced image saved as: figures\enhanced_TCI_COG.tiff
echo Carbon mask saved as: figures\Carbon_mask_TCI_COG.tiff
echo Fire mask saved as: figures\Fire_mask_TCI_COG.tiff
echo PNG versions saved in: figures\png\
echo =============================================

endlocal
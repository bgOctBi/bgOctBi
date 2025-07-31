#!/bin/bash

echo "PDF Batch Cropper - Setup Script"
echo "================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv pdf_cropper_env

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    echo "On Ubuntu/Debian systems, try: sudo apt install python3-venv"
    echo "On other systems, ensure you have the venv module available."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source pdf_cropper_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install PyMuPDF Pillow

if [ $? -eq 0 ]; then
    echo ""
    echo "Setup complete!"
    echo ""
    echo "To use the PDF cropper:"
    echo "1. Activate the virtual environment:"
    echo "   source pdf_cropper_env/bin/activate"
    echo ""
    echo "2. Run the GUI version:"
    echo "   python pdf_crop_gui.py"
    echo ""
    echo "3. Or run the command line version:"
    echo "   python pdf_crop_batch.py --help"
    echo ""
    echo "4. To deactivate the virtual environment when done:"
    echo "   deactivate"
else
    echo "Failed to install dependencies."
    echo "Please check your internet connection and try again."
    exit 1
fi
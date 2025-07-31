# PDF Batch Cropper - Quick Start Guide

Get started with the PDF Batch Cropper in just a few minutes!

## 🚀 Quick Setup

### Option 1: Automatic Setup (Recommended)
```bash
# Run the setup script
./setup.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv pdf_cropper_env
source pdf_cropper_env/bin/activate

# Install dependencies
pip install PyMuPDF Pillow
```

### Option 3: System-wide Installation
```bash
# Install dependencies system-wide (use with caution)
pip install --break-system-packages PyMuPDF Pillow
```

## 🧪 Test Installation
```bash
python test_cropper.py
```

## 📁 Basic Usage

### 1. GUI Version (Easiest)
```bash
python pdf_crop_gui.py
```

1. Click "Browse" to select your input folder with PDF files
2. Click "Browse" to select where to save cropped images
3. Enter your crop coordinates (e.g., 100, 100, 400, 300)
4. Click "Start Processing"

### 2. Command Line Version
```bash
# Basic usage: crop rectangle from (100,100) to (400,300)
python pdf_crop_batch.py ./input_pdfs ./output_images 100 100 400 300

# Crop specific pages only
python pdf_crop_batch.py ./input_pdfs ./output_images 100 100 400 300 --pages 1,2,3

# Save as JPEG with higher DPI
python pdf_crop_batch.py ./input_pdfs ./output_images 100 100 400 300 --format jpg --dpi 600
```

## 📐 Finding Coordinates

### Method 1: Use PDF Viewer
1. Open your PDF in any viewer (Adobe Reader, etc.)
2. Look for coordinate display (usually bottom-left)
3. Note coordinates of your desired rectangle corners

### Method 2: Trial and Error
1. Start with sample coordinates: `100 100 400 300`
2. Check the output image
3. Adjust coordinates as needed

### Method 3: Common Patterns
```bash
# Top-left quarter of page
100 400 300 600

# Bottom-right quarter  
300 100 500 300

# Center rectangle
200 200 400 500
```

## 📊 Coordinate Examples

For US Letter (612×792 points):
- **Full page**: `0 0 612 792`
- **Top half**: `0 396 612 792`
- **Bottom half**: `0 0 612 396`
- **Left half**: `0 0 306 792`
- **Right half**: `306 0 612 792`
- **Center 4×6 inch**: `108 180 396 612`

For A4 (595×842 points):
- **Full page**: `0 0 595 842`
- **Top half**: `0 421 595 842`
- **Bottom half**: `0 0 595 421`

## 🗂️ File Organization

```
your-project/
├── input_pdfs/          # Put your PDF files here
│   ├── document1.pdf
│   ├── document2.pdf
│   └── document3.pdf
├── output_images/       # Cropped images will be saved here
├── pdf_crop_batch.py    # Main program
├── pdf_crop_gui.py      # GUI version
└── requirements.txt     # Dependencies
```

## ⚡ Quick Tips

1. **Start small**: Test with one PDF first
2. **Use PNG**: Better quality for text/diagrams
3. **Use JPG**: Smaller files for photos
4. **Higher DPI**: Better quality, larger files
5. **Check logs**: Use GUI log window to see what's happening

## 🆘 Common Issues

**"No module named 'fitz'"**
```bash
pip install PyMuPDF
```

**"No PDF files found"**
- Check that PDF files are in the input directory
- Files must have .pdf extension

**"Crop rectangle extends beyond page"**
- Your coordinates are outside the page bounds
- Use smaller coordinate values

**GUI won't start**
```bash
# Try command line version instead
python pdf_crop_batch.py --help
```

## 💡 Examples

### Example 1: Crop headers from invoices
```bash
# Crop top 2 inches of each page
python pdf_crop_batch.py ./invoices ./headers 0 648 612 792
```

### Example 2: Extract signatures
```bash
# Crop bottom-right corner where signatures usually are
python pdf_crop_batch.py ./contracts ./signatures 400 0 612 150
```

### Example 3: Extract tables
```bash
# Crop middle section where tables are located
python pdf_crop_batch.py ./reports ./tables 50 200 550 600
```

## 🎯 Next Steps

1. **Read the full README**: `PDF_Cropper_README.md`
2. **See more examples**: `python example_usage.py`
3. **Get help**: `python pdf_crop_batch.py --help`

---

**Need more help?** Check the full documentation in `PDF_Cropper_README.md`
# PDF Batch Cropper

A Python program that automatically crops rectangular areas from PDF files and saves them as images. The same rectangular coordinates are applied to all PDF files in the batch.

## Features

- **Batch Processing**: Process multiple PDF files at once
- **Flexible Cropping**: Define custom rectangular crop areas with precise coordinates
- **Multiple Output Formats**: Save as PNG, JPG, or JPEG
- **Page Selection**: Process all pages or specific pages only
- **High Quality**: Configurable DPI for output images
- **GUI Interface**: Easy-to-use graphical interface
- **Command Line**: Scriptable command-line interface
- **Error Handling**: Robust error handling with detailed logging

## Installation

### Requirements

- Python 3.7 or higher
- PyMuPDF (fitz)
- Pillow (PIL)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install PyMuPDF Pillow
```

## Usage

### GUI Interface (Recommended)

Run the graphical interface for easy use:

```bash
python pdf_crop_gui.py
```

The GUI provides:
- Directory browsers for input and output folders
- Input fields for crop coordinates
- Options for page selection, format, and DPI
- Real-time logging
- Preview of settings before processing

### Command Line Interface

```bash
python pdf_crop_batch.py INPUT_DIR OUTPUT_DIR X1 Y1 X2 Y2 [OPTIONS]
```

#### Parameters

- `INPUT_DIR`: Directory containing PDF files
- `OUTPUT_DIR`: Directory to save cropped images
- `X1`, `Y1`: Top-left coordinates of crop rectangle
- `X2`, `Y2`: Bottom-right coordinates of crop rectangle

#### Options

- `--pages`: Comma-separated page numbers (1-indexed). Example: `1,2,3`
- `--format`: Output format (`png`, `jpg`, `jpeg`). Default: `png`
- `--dpi`: DPI for output images. Default: `300`
- `--verbose, -v`: Enable verbose logging

#### Examples

**Basic usage - crop all pages:**
```bash
python pdf_crop_batch.py ./input ./output 100 100 400 300
```

**Crop specific pages with custom format:**
```bash
python pdf_crop_batch.py ./input ./output 50 50 500 400 --pages 1,3,5 --format jpg --dpi 600
```

**Verbose logging:**
```bash
python pdf_crop_batch.py ./input ./output 100 100 400 300 --verbose
```

### Programmatic Usage

```python
from pdf_crop_batch import PDFCropper

# Create cropper instance
cropper = PDFCropper(
    input_dir="./input_pdfs",
    output_dir="./output_images",
    crop_coords=(100, 100, 400, 300)
)

# Process all PDFs
results = cropper.process_batch()

# Process specific pages only
results = cropper.process_batch(pages=[0, 2, 4])  # Pages 1, 3, 5

# Process with custom format
results = cropper.process_batch(output_format="jpg")
```

## Understanding Coordinates

### Coordinate System

- **Origin (0, 0)**: Bottom-left corner of the PDF page
- **X-axis**: Increases to the right
- **Y-axis**: Increases upward
- **Units**: PDF points (1/72 inch)

### Coordinate Conversion

```python
# Convert inches to points
points = inches * 72

# Convert millimeters to points
points = mm * 72 / 25.4
```

### Common Paper Sizes (in points)

- **US Letter**: 612 × 792 points
- **A4**: 595 × 842 points
- **Legal**: 612 × 1008 points

### Example Calculations

To crop a 2×3 inch rectangle starting 1 inch from the left and bottom:

```python
x1 = 1 * 72      # 72 points from left
y1 = 1 * 72      # 72 points from bottom
x2 = x1 + (2 * 72)  # 216 points (2 inches wide)
y2 = y1 + (3 * 72)  # 288 points (3 inches tall)

crop_coords = (72, 72, 216, 288)
```

## File Structure

```
pdf-batch-cropper/
├── pdf_crop_batch.py    # Main cropping engine
├── pdf_crop_gui.py      # GUI interface
├── example_usage.py     # Usage examples
├── requirements.txt     # Dependencies
└── PDF_Cropper_README.md # This file
```

## Output Files

The program generates output files with descriptive names:

- **Single page**: `filename_cropped.png`
- **Multiple pages**: `filename_page_1_cropped.png`, `filename_page_2_cropped.png`, etc.

## Error Handling

The program includes comprehensive error handling:

- **Invalid coordinates**: Automatically adjusts crop rectangle to fit within page bounds
- **Missing pages**: Skips non-existent pages with warnings
- **Corrupted PDFs**: Continues processing other files
- **Permission errors**: Reports access issues clearly

## Logging

Detailed logging provides information about:

- Files being processed
- Page dimensions and crop adjustments
- Success/failure status
- Processing statistics

## Performance Tips

1. **DPI Settings**: Higher DPI produces better quality but larger files
   - 150 DPI: Good for screen viewing
   - 300 DPI: Good for printing
   - 600 DPI: High quality for detailed work

2. **Format Selection**:
   - PNG: Best quality, larger files
   - JPG: Smaller files, slight quality loss

3. **Batch Size**: Process large batches overnight for best performance

## Troubleshooting

### Common Issues

**"No PDF files found"**
- Check that input directory contains .pdf files
- Verify directory path is correct

**"Crop rectangle extends beyond page bounds"**
- Check coordinate values against page dimensions
- Use `--verbose` flag to see page dimensions

**"Permission denied"**
- Ensure write permissions for output directory
- Close PDF files if open in other applications

**Dependencies not found**
- Run `pip install -r requirements.txt`
- Check Python version (3.7+ required)

### Getting Help

Run with `--help` for command-line options:
```bash
python pdf_crop_batch.py --help
```

## Examples

See `example_usage.py` for comprehensive examples:

```bash
python example_usage.py
```

## License

This program is free to use and modify for personal and commercial purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the examples
3. Use verbose logging to diagnose problems
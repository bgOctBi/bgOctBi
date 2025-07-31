#!/usr/bin/env python3
"""
Example usage of the PDF Batch Cropper

This script demonstrates how to use the PDFCropper class programmatically.
"""

from pdf_crop_batch import PDFCropper
from pathlib import Path

def example_basic_usage():
    """Basic example of cropping PDFs."""
    print("=== Basic PDF Cropping Example ===")
    
    # Define directories and crop coordinates
    input_dir = "input_pdfs"  # Directory containing your PDF files
    output_dir = "cropped_images"  # Directory to save cropped images
    
    # Crop rectangle coordinates (x1, y1, x2, y2)
    # These coordinates are in PDF points (1/72 inch)
    # Example: crop a rectangle from (100, 100) to (400, 300)
    crop_coords = (100, 100, 400, 300)
    
    # Create the cropper
    cropper = PDFCropper(input_dir, output_dir, crop_coords)
    
    # Process all PDFs, all pages
    results = cropper.process_batch()
    
    print(f"Processed {results['processed_files']} files")
    print(f"Total pages cropped: {results['total_pages']}")

def example_specific_pages():
    """Example of cropping specific pages only."""
    print("\n=== Specific Pages Example ===")
    
    input_dir = "input_pdfs"
    output_dir = "cropped_images_pages"
    crop_coords = (50, 50, 500, 400)
    
    cropper = PDFCropper(input_dir, output_dir, crop_coords)
    
    # Process only pages 1 and 3 (0-indexed: 0 and 2)
    specific_pages = [0, 2]  # Page 1 and Page 3
    results = cropper.process_batch(pages=specific_pages, output_format="jpg")
    
    print(f"Processed {results['processed_files']} files")
    print(f"Total pages cropped: {results['total_pages']}")

def example_single_pdf():
    """Example of processing a single PDF file."""
    print("\n=== Single PDF Example ===")
    
    input_dir = "input_pdfs"
    output_dir = "single_pdf_output"
    crop_coords = (200, 150, 600, 450)
    
    cropper = PDFCropper(input_dir, output_dir, crop_coords)
    
    # Get PDF files
    pdf_files = cropper.get_pdf_files()
    
    if pdf_files:
        # Process first PDF file only
        pdf_file = pdf_files[0]
        pages_processed = cropper.process_single_pdf(pdf_file, pages=[0], output_format="png")
        print(f"Processed {pages_processed} pages from {pdf_file.name}")
    else:
        print("No PDF files found")

def example_coordinate_calculation():
    """Example showing how to calculate coordinates."""
    print("\n=== Coordinate Calculation Tips ===")
    
    print("""
    Coordinate System:
    - Origin (0, 0) is at the bottom-left corner of the PDF page
    - X increases to the right
    - Y increases upward
    - Units are in PDF points (1/72 inch)
    
    To convert from inches to points: inches × 72
    To convert from millimeters to points: mm × 72 / 25.4
    
    Common paper sizes in points:
    - US Letter: 612 × 792 points
    - A4: 595 × 842 points
    
    Example calculations:
    - Crop 2×3 inch rectangle starting 1 inch from left and bottom:
      x1 = 1 * 72 = 72
      y1 = 1 * 72 = 72
      x2 = x1 + (2 * 72) = 216
      y2 = y1 + (3 * 72) = 288
      coordinates = (72, 72, 216, 288)
    """)

def main():
    """Run all examples."""
    print("PDF Batch Cropper - Usage Examples")
    print("=" * 40)
    
    # Note: These examples assume you have PDF files in an "input_pdfs" directory
    # Create some sample directories for demonstration
    Path("input_pdfs").mkdir(exist_ok=True)
    
    print("\nNote: Make sure you have PDF files in the 'input_pdfs' directory")
    print("and that you've installed the required dependencies:")
    print("pip install -r requirements.txt")
    
    # Run examples (commented out to avoid errors if no PDFs exist)
    # Uncomment these lines when you have PDF files to process
    
    # example_basic_usage()
    # example_specific_pages()
    # example_single_pdf()
    example_coordinate_calculation()
    
    print("\n" + "=" * 40)
    print("Examples complete!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
PDF Batch Cropper

This program automatically crops rectangular areas from PDF files and saves them as images.
The same rectangular coordinates are applied to all PDF files in the batch.

Requirements:
- PyMuPDF (fitz)
- Pillow (PIL)

Usage:
    python pdf_crop_batch.py
"""

import os
import sys
from pathlib import Path
import argparse
from typing import List, Tuple, Optional
import fitz  # PyMuPDF
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFCropper:
    """Class to handle PDF cropping operations."""
    
    def __init__(self, input_dir: str, output_dir: str, crop_coords: Tuple[float, float, float, float]):
        """
        Initialize the PDF cropper.
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save cropped images
            crop_coords: Tuple of (x1, y1, x2, y2) coordinates for cropping rectangle
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.crop_coords = crop_coords
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Input directory: {self.input_dir}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Crop coordinates: {self.crop_coords}")
    
    def get_pdf_files(self) -> List[Path]:
        """Get all PDF files from the input directory."""
        pdf_files = list(self.input_dir.glob("*.pdf"))
        pdf_files.extend(self.input_dir.glob("*.PDF"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.input_dir}")
        else:
            logger.info(f"Found {len(pdf_files)} PDF files")
            
        return pdf_files
    
    def crop_pdf_page(self, pdf_path: Path, page_num: int, output_path: Path, 
                     dpi: int = 300) -> bool:
        """
        Crop a specific page from a PDF and save as image.
        
        Args:
            pdf_path: Path to the PDF file
            page_num: Page number to crop (0-indexed)
            output_path: Path to save the cropped image
            dpi: DPI for image resolution
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Open PDF
            doc = fitz.open(pdf_path)
            
            if page_num >= len(doc):
                logger.warning(f"Page {page_num + 1} not found in {pdf_path.name}")
                doc.close()
                return False
            
            # Get the page
            page = doc[page_num]
            
            # Create crop rectangle
            x1, y1, x2, y2 = self.crop_coords
            crop_rect = fitz.Rect(x1, y1, x2, y2)
            
            # Get page dimensions for validation
            page_rect = page.rect
            logger.debug(f"Page dimensions: {page_rect}")
            logger.debug(f"Crop rectangle: {crop_rect}")
            
            # Validate crop coordinates
            if not page_rect.contains(crop_rect):
                logger.warning(f"Crop rectangle {crop_rect} extends beyond page bounds {page_rect} for {pdf_path.name}")
                # Adjust crop rectangle to fit within page
                crop_rect = crop_rect & page_rect
                logger.info(f"Adjusted crop rectangle: {crop_rect}")
            
            # Set the crop box
            page.set_cropbox(crop_rect)
            
            # Render page to image
            mat = fitz.Matrix(dpi/72, dpi/72)  # 72 is default DPI
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            
            # Save image
            img.save(output_path, quality=95, optimize=True)
            
            doc.close()
            logger.info(f"Successfully cropped page {page_num + 1} from {pdf_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error cropping {pdf_path.name}, page {page_num + 1}: {str(e)}")
            if 'doc' in locals():
                doc.close()
            return False
    
    def process_single_pdf(self, pdf_path: Path, pages: Optional[List[int]] = None,
                          output_format: str = "png") -> int:
        """
        Process a single PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            pages: List of page numbers to process (0-indexed). If None, process all pages
            output_format: Output image format (png, jpg, jpeg)
            
        Returns:
            Number of successfully processed pages
        """
        logger.info(f"Processing {pdf_path.name}")
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            doc.close()
            
            if pages is None:
                pages = list(range(total_pages))
            
            success_count = 0
            
            for page_num in pages:
                if page_num >= total_pages:
                    logger.warning(f"Page {page_num + 1} not found in {pdf_path.name} (total pages: {total_pages})")
                    continue
                
                # Generate output filename
                base_name = pdf_path.stem
                if len(pages) == 1:
                    output_filename = f"{base_name}_cropped.{output_format}"
                else:
                    output_filename = f"{base_name}_page_{page_num + 1}_cropped.{output_format}"
                
                output_path = self.output_dir / output_filename
                
                if self.crop_pdf_page(pdf_path, page_num, output_path):
                    success_count += 1
            
            logger.info(f"Completed {pdf_path.name}: {success_count}/{len(pages)} pages processed successfully")
            return success_count
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {str(e)}")
            return 0
    
    def process_batch(self, pages: Optional[List[int]] = None, 
                     output_format: str = "png") -> dict:
        """
        Process all PDF files in the input directory.
        
        Args:
            pages: List of page numbers to process (0-indexed). If None, process all pages
            output_format: Output image format (png, jpg, jpeg)
            
        Returns:
            Dictionary with processing results
        """
        pdf_files = self.get_pdf_files()
        
        if not pdf_files:
            return {"total_files": 0, "processed_files": 0, "total_pages": 0}
        
        total_pages_processed = 0
        processed_files = 0
        
        for pdf_file in pdf_files:
            pages_processed = self.process_single_pdf(pdf_file, pages, output_format)
            if pages_processed > 0:
                processed_files += 1
                total_pages_processed += pages_processed
        
        results = {
            "total_files": len(pdf_files),
            "processed_files": processed_files,
            "total_pages": total_pages_processed
        }
        
        logger.info(f"Batch processing complete: {results}")
        return results


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Batch crop rectangular areas from PDF files")
    
    parser.add_argument("input_dir", help="Directory containing PDF files")
    parser.add_argument("output_dir", help="Directory to save cropped images")
    parser.add_argument("x1", type=float, help="Left coordinate of crop rectangle")
    parser.add_argument("y1", type=float, help="Top coordinate of crop rectangle")
    parser.add_argument("x2", type=float, help="Right coordinate of crop rectangle")
    parser.add_argument("y2", type=float, help="Bottom coordinate of crop rectangle")
    
    parser.add_argument("--pages", type=str, help="Comma-separated page numbers to process (1-indexed). If not specified, all pages are processed")
    parser.add_argument("--format", choices=["png", "jpg", "jpeg"], default="png", help="Output image format")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for output images")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Parse page numbers if provided
    pages = None
    if args.pages:
        try:
            # Convert from 1-indexed to 0-indexed
            pages = [int(p.strip()) - 1 for p in args.pages.split(",")]
            pages = [p for p in pages if p >= 0]  # Filter out invalid page numbers
        except ValueError:
            logger.error("Invalid page numbers format. Use comma-separated numbers (e.g., '1,2,3')")
            sys.exit(1)
    
    # Validate coordinates
    x1, y1, x2, y2 = args.x1, args.y1, args.x2, args.y2
    if x1 >= x2 or y1 >= y2:
        logger.error("Invalid crop coordinates. x1 < x2 and y1 < y2 required.")
        sys.exit(1)
    
    # Create cropper and process files
    cropper = PDFCropper(args.input_dir, args.output_dir, (x1, y1, x2, y2))
    results = cropper.process_batch(pages, args.format)
    
    print(f"\nProcessing Summary:")
    print(f"Total PDF files found: {results['total_files']}")
    print(f"Successfully processed files: {results['processed_files']}")
    print(f"Total pages cropped: {results['total_pages']}")


if __name__ == "__main__":
    # Import io here since it's needed for the image conversion
    import io
    main()
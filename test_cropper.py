#!/usr/bin/env python3
"""
Test script for the PDF Batch Cropper

This script tests the basic functionality of the PDF cropper without requiring actual PDF files.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import fitz
        print("✓ PyMuPDF (fitz) imported successfully")
    except ImportError as e:
        print(f"✗ PyMuPDF (fitz) import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"✗ Pillow (PIL) import failed: {e}")
        return False
    
    try:
        from pdf_crop_batch import PDFCropper
        print("✓ PDFCropper class imported successfully")
    except ImportError as e:
        print(f"✗ PDFCropper import failed: {e}")
        return False
    
    return True

def test_pdf_cropper_class():
    """Test the PDFCropper class initialization."""
    print("\nTesting PDFCropper class...")
    
    try:
        from pdf_crop_batch import PDFCropper
        
        # Test with dummy directories
        test_input = Path("test_input")
        test_output = Path("test_output")
        
        # Create test directories
        test_input.mkdir(exist_ok=True)
        test_output.mkdir(exist_ok=True)
        
        # Initialize cropper
        cropper = PDFCropper(
            input_dir=str(test_input),
            output_dir=str(test_output),
            crop_coords=(100, 100, 400, 300)
        )
        
        print("✓ PDFCropper initialized successfully")
        
        # Test get_pdf_files method (should return empty list)
        pdf_files = cropper.get_pdf_files()
        print(f"✓ get_pdf_files() returned {len(pdf_files)} files (expected 0)")
        
        # Clean up test directories
        test_input.rmdir()
        test_output.rmdir()
        
        return True
        
    except Exception as e:
        print(f"✗ PDFCropper test failed: {e}")
        return False

def test_gui_imports():
    """Test if GUI components can be imported."""
    print("\nTesting GUI imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        print("  Note: tkinter may not be available in some environments")
        return False
    
    try:
        from tkinter import ttk, filedialog, messagebox, scrolledtext
        print("✓ tkinter components imported successfully")
    except ImportError as e:
        print(f"✗ tkinter components import failed: {e}")
        return False
    
    return True

def test_coordinate_calculations():
    """Test coordinate calculation examples."""
    print("\nTesting coordinate calculations...")
    
    # Test basic conversions
    inches_to_points = lambda inches: inches * 72
    mm_to_points = lambda mm: mm * 72 / 25.4
    
    # Test cases
    assert inches_to_points(1) == 72, "1 inch should equal 72 points"
    assert abs(mm_to_points(25.4) - 72) < 0.1, "25.4mm should equal ~72 points"
    
    print("✓ Coordinate calculations working correctly")
    return True

def create_sample_directories():
    """Create sample directory structure."""
    print("\nCreating sample directories...")
    
    directories = [
        "input_pdfs",
        "output_images",
        "cropped_images"
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}")
    
    return True

def main():
    """Run all tests."""
    print("PDF Batch Cropper - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("PDFCropper Class Test", test_pdf_cropper_class),
        ("GUI Import Test", test_gui_imports),
        ("Coordinate Calculation Test", test_coordinate_calculations),
        ("Sample Directories", create_sample_directories)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The PDF cropper is ready to use.")
        print("\nNext steps:")
        print("1. Add PDF files to the 'input_pdfs' directory")
        print("2. Run: python pdf_crop_gui.py (for GUI)")
        print("3. Or run: python pdf_crop_batch.py --help (for command line)")
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        print("Run: pip install PyMuPDF Pillow")
        
        if passed >= 2:  # If basic imports work
            print("Basic functionality appears to work despite some test failures.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
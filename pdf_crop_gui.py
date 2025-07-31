#!/usr/bin/env python3
"""
PDF Batch Cropper - GUI Version

A simple GUI application for batch cropping rectangular areas from PDF files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import sys
import os

# Add the current directory to sys.path to import our cropper module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_crop_batch import PDFCropper
except ImportError:
    messagebox.showerror("Error", "pdf_crop_batch.py module not found. Please ensure it's in the same directory.")
    sys.exit(1)


class PDFCropperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Batch Cropper")
        self.root.geometry("700x600")
        
        # Variables
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.x1_var = tk.DoubleVar(value=100.0)
        self.y1_var = tk.DoubleVar(value=100.0)
        self.x2_var = tk.DoubleVar(value=400.0)
        self.y2_var = tk.DoubleVar(value=300.0)
        self.pages_var = tk.StringVar()
        self.format_var = tk.StringVar(value="png")
        self.dpi_var = tk.IntVar(value=300)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Batch Cropper", font=("Arial", 16, "bold"))
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # Input directory
        ttk.Label(main_frame, text="Input Directory:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_dir, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_dir).grid(row=row, column=2, padx=5)
        row += 1
        
        # Output directory
        ttk.Label(main_frame, text="Output Directory:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_dir).grid(row=row, column=2, padx=5)
        row += 1
        
        # Crop coordinates frame
        coords_frame = ttk.LabelFrame(main_frame, text="Crop Rectangle Coordinates", padding="10")
        coords_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        coords_frame.columnconfigure(1, weight=1)
        coords_frame.columnconfigure(3, weight=1)
        row += 1
        
        # Coordinates
        ttk.Label(coords_frame, text="X1 (Left):").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Entry(coords_frame, textvariable=self.x1_var, width=15).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(coords_frame, text="Y1 (Top):").grid(row=0, column=2, sticky=tk.W, padx=5)
        ttk.Entry(coords_frame, textvariable=self.y1_var, width=15).grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Label(coords_frame, text="X2 (Right):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(coords_frame, textvariable=self.x2_var, width=15).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(coords_frame, text="Y2 (Bottom):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(coords_frame, textvariable=self.y2_var, width=15).grid(row=1, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)
        row += 1
        
        # Pages
        ttk.Label(options_frame, text="Pages (optional):").grid(row=0, column=0, sticky=tk.W, padx=5)
        pages_entry = ttk.Entry(options_frame, textvariable=self.pages_var, width=20)
        pages_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(options_frame, text="(e.g., 1,2,3 or leave empty for all)").grid(row=0, column=2, columnspan=2, sticky=tk.W, padx=5)
        
        # Format and DPI
        ttk.Label(options_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, values=["png", "jpg", "jpeg"], width=10)
        format_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        format_combo.state(['readonly'])
        
        ttk.Label(options_frame, text="DPI:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(options_frame, textvariable=self.dpi_var, width=10).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=row, column=0, columnspan=3, pady=20)
        row += 1
        
        self.process_button = ttk.Button(buttons_frame, text="Start Processing", command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.preview_button = ttk.Button(buttons_frame, text="Preview Settings", command=self.preview_settings)
        self.preview_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir.set(directory)
            self.log(f"Input directory selected: {directory}")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            self.log(f"Output directory selected: {directory}")
    
    def log(self, message):
        """Add message to log area."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log area."""
        self.log_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """Validate user inputs."""
        if not self.input_dir.get():
            messagebox.showerror("Error", "Please select an input directory.")
            return False
        
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory.")
            return False
        
        if not os.path.exists(self.input_dir.get()):
            messagebox.showerror("Error", "Input directory does not exist.")
            return False
        
        # Validate coordinates
        try:
            x1, y1, x2, y2 = self.x1_var.get(), self.y1_var.get(), self.x2_var.get(), self.y2_var.get()
            if x1 >= x2 or y1 >= y2:
                messagebox.showerror("Error", "Invalid coordinates. X1 must be less than X2, and Y1 must be less than Y2.")
                return False
        except tk.TclError:
            messagebox.showerror("Error", "Please enter valid numeric coordinates.")
            return False
        
        # Validate DPI
        try:
            dpi = self.dpi_var.get()
            if dpi <= 0:
                messagebox.showerror("Error", "DPI must be a positive number.")
                return False
        except tk.TclError:
            messagebox.showerror("Error", "Please enter a valid DPI value.")
            return False
        
        return True
    
    def preview_settings(self):
        """Show a preview of current settings."""
        if not self.validate_inputs():
            return
        
        pages_str = self.pages_var.get().strip() if self.pages_var.get().strip() else "All pages"
        
        preview_text = f"""
Current Settings:
-----------------
Input Directory: {self.input_dir.get()}
Output Directory: {self.output_dir.get()}
Crop Rectangle: ({self.x1_var.get()}, {self.y1_var.get()}) to ({self.x2_var.get()}, {self.y2_var.get()})
Pages to Process: {pages_str}
Output Format: {self.format_var.get().upper()}
DPI: {self.dpi_var.get()}

The program will:
1. Find all PDF files in the input directory
2. Crop the specified rectangular area from each page
3. Save the cropped images in the output directory
"""
        
        messagebox.showinfo("Settings Preview", preview_text)
    
    def start_processing(self):
        """Start the PDF processing in a separate thread."""
        if not self.validate_inputs():
            return
        
        self.process_button.config(state='disabled')
        self.progress.start()
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_pdfs)
        thread.daemon = True
        thread.start()
    
    def process_pdfs(self):
        """Process PDFs (runs in separate thread)."""
        try:
            self.log("Starting PDF processing...")
            
            # Parse pages if provided
            pages = None
            if self.pages_var.get().strip():
                try:
                    pages = [int(p.strip()) - 1 for p in self.pages_var.get().split(",")]
                    pages = [p for p in pages if p >= 0]
                    self.log(f"Processing specific pages: {[p+1 for p in pages]}")
                except ValueError:
                    self.log("Error: Invalid page numbers format. Processing all pages instead.")
                    pages = None
            
            # Create cropper
            coords = (self.x1_var.get(), self.y1_var.get(), self.x2_var.get(), self.y2_var.get())
            cropper = PDFCropper(self.input_dir.get(), self.output_dir.get(), coords)
            
            # Process files
            results = cropper.process_batch(pages, self.format_var.get())
            
            # Show results
            self.log(f"\nProcessing complete!")
            self.log(f"Total PDF files found: {results['total_files']}")
            self.log(f"Successfully processed files: {results['processed_files']}")
            self.log(f"Total pages cropped: {results['total_pages']}")
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Complete", 
                f"Processing finished!\n\n"
                f"Processed {results['processed_files']} out of {results['total_files']} PDF files.\n"
                f"Total pages cropped: {results['total_pages']}\n\n"
                f"Images saved to: {self.output_dir.get()}"
            ))
            
        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self.log(f"\n{error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Re-enable button and stop progress bar
            self.root.after(0, self.finish_processing)
    
    def finish_processing(self):
        """Clean up after processing is complete."""
        self.progress.stop()
        self.process_button.config(state='normal')


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = PDFCropperGUI(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
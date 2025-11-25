"""Photo Duplicate Finder

Finds and removes duplicate images based on content, not just filenames.
Uses image hashing to detect identical photos.

Requires: Pillow (PIL)

Author: David L. Couch (Splatbasset)
License: MIT
"""

import os
import hashlib
from tkinter import Tk, filedialog, messagebox
from PIL import Image

def get_image_hash(image_path):
    """Generate hash for an image based on its pixel data.
    Resizes to 256x256 and converts to RGB for consistent results."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img = img.resize((256, 256))
            return hashlib.md5(img.tobytes()).hexdigest()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def find_duplicate_images(folder_path):
    """Scan folder recursively for duplicate images.
    Returns list of tuples: [(duplicate, original), ...]
    Supports: PNG, JPG, JPEG, BMP, GIF"""
    hashes = {}
    duplicates = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                file_path = os.path.join(root, file)
                img_hash = get_image_hash(file_path)
                if img_hash:
                    # Check if we've seen this image content before
                    if img_hash in hashes:
                        # Found a duplicate - store both paths
                        duplicates.append((file_path, hashes[img_hash]))
                    else:
                        # First occurrence - record this as the original
                        hashes[img_hash] = file_path
    return duplicates

def delete_duplicates(duplicates):
    """Delete duplicate files, keeping originals.
    Returns (deleted_count, skipped_count)."""
    deleted_count = 0
    skipped_count = 0
    
    for dup1, dup2 in duplicates:
        try:
            file_to_delete = choose_file_to_delete(dup1, dup2)
            file_to_keep = dup2 if file_to_delete == dup1 else dup1
            
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)
                print(f"Deleted: {file_to_delete}")
                print(f"Kept: {file_to_keep}")
                deleted_count += 1
            else:
                print(f"File already gone: {file_to_delete}")
                skipped_count += 1
        except Exception as e:
            print(f"Error deleting {file_to_delete}: {e}")
            skipped_count += 1
    
    return deleted_count, skipped_count

def choose_file_to_delete(file1, file2):
    """Pick which duplicate to delete based on filename patterns.
    Prefers to delete files with 'Copy' or similar in the name."""
    delete_patterns = [" - Copy", " 1", "-Alienware", " copy", "Copy of"]
    
    file1_name = os.path.basename(file1)
    file2_name = os.path.basename(file2)
    
    file1_has_pattern = any(pattern in file1_name for pattern in delete_patterns)
    file2_has_pattern = any(pattern in file2_name for pattern in delete_patterns)
    
    if file1_has_pattern and not file2_has_pattern:
        return file1
    elif file2_has_pattern and not file1_has_pattern:
        return file2
    else:
        # Neither or both have patterns - delete the longer name
        return file1 if len(file1_name) >= len(file2_name) else file2

def main():
    """Main program - prompts for folder, finds duplicates, asks to delete."""
    Tk().withdraw()
    
    # Prompt user to select a folder using native file dialog
    folder_selected = filedialog.askdirectory(title="Select a folder to scan for duplicate images")

    if folder_selected:
        # Begin scanning process
        print(f"Scanning folder: {folder_selected}")
        duplicates = find_duplicate_images(folder_selected)

        if duplicates:
            print(f"\n{len(duplicates)} duplicate image pairs found:")
            for dup1, dup2 in duplicates:
                print(f" - {dup1} == {dup2}")
            
            response = messagebox.askyesno(
                "Delete Duplicates", 
                f"Found {len(duplicates)} duplicate image pairs.\n\n"
                "Do you want to delete one copy of each duplicate?"
            )
            
            if response:
                print("\nDeleting duplicates...")
                deleted_count, skipped_count = delete_duplicates(duplicates)
                
                result_msg = f"Deletion complete!\n\nDeleted: {deleted_count} files\nSkipped: {skipped_count} files"
                print(f"\n{result_msg}")
                messagebox.showinfo("Deletion Complete", result_msg)
            else:
                print("\nDeletion cancelled by user.")
        else:
            print("\nNo duplicate images found.")
            messagebox.showinfo("Scan Complete", "No duplicate images found.")
    else:
        print("No folder selected.")

if __name__ == "__main__":
    main()
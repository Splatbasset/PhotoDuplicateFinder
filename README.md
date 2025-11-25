# 📸 Photo Duplicate Finder

A lightweight Python tool that finds and removes duplicate photos based on their actual content, not just filenames.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Smart Detection** - Uses image hashing to identify duplicates by visual content
- **Recursive Scanning** - Searches through all subdirectories automatically
- **Intelligent Deletion** - Keeps originals, removes copies based on filename patterns
- **Safe & Interactive** - Shows what will be deleted before taking action
- **Multiple Formats** - Supports PNG, JPG, JPEG, BMP, and GIF files

## 🚀 Quick Start

### Prerequisites

```bash
pip install Pillow
```

### Usage

1. Run the script:
```bash
python PhotoDuplicateFinder.py
```

2. Select a folder when prompted
3. Review the list of duplicates found
4. Confirm to delete duplicates (or cancel to keep everything)

## 🔍 How It Works

The tool normalizes each image (resize to 256x256, convert to RGB) and generates an MD5 hash of the pixel data. This means:

- ✅ Identical photos with different names are detected
- ✅ Same image in different folders is found
- ✅ Fast processing even with large collections

When duplicates are found, the script intelligently chooses which to delete by:
1. Preferring to keep files without "Copy", " 1", or similar patterns
2. Keeping the file with the shorter name if no patterns match

## 📋 Example Output

```
Scanning folder: C:\Users\Photos\Vacation

3 duplicate image pairs found:
 - C:\Users\Photos\Vacation\beach.jpg == C:\Users\Photos\Vacation\beach - Copy.jpg
 - C:\Users\Photos\Vacation\sunset 1.jpg == C:\Users\Photos\Vacation\sunset.jpg
 - C:\Users\Photos\Archive\beach.jpg == C:\Users\Photos\Vacation\beach.jpg

Deletion complete!

Deleted: 3 files
Skipped: 0 files
```

## ⚠️ Important Notes

- **Permanent Deletion** - Files are permanently deleted, not moved to recycle bin
- **Backup First** - Consider backing up important photos before running
- **Review Carefully** - Always check the duplicate list before confirming deletion

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **Dependencies**: Pillow (PIL)
- **Hashing**: MD5 on normalized pixel data
- **GUI**: tkinter (included with Python)

## 📝 License

MIT License - feel free to use, modify, and distribute.

## 👤 Author

**David L. Couch (Splatbasset)**

---

Made with ❤️ for organizing photo collections

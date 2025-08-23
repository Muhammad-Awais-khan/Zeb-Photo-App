# Zeb Passport Photo Maker

Zeb Passport Photo Maker is a Windows desktop application for generating professional passport photos and PDFs. It features automatic face detection, background removal, brightness/contrast adjustment, and batch PDF export. The app is designed for personal use and is easy to operate with a modern graphical interface.

## Features

- **Automatic Face Detection:** Detects and crops faces using OpenCV and Haar cascades.
- **Background Removal:** Removes image backgrounds and optionally replaces with blue or white.
- **Brightness/Contrast Adjustment:** Fine-tune photo appearance before export.
- **PDF Export:** Generates a PDF with 9 passport-sized photos (3x3 grid) or a single JPEG.
- **Modern UI:** Simple, user-friendly interface built with Tkinter.
- **One-Click Save:** Saves output to your Documents folder and opens automatically.

## Installation

### Prerequisites
- Windows 10/11
- Python 3.10+ (recommended)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Dependencies
All required Python packages are listed in `requirements.txt`. Key packages include:
- `opencv-python-headless` (face detection)
- `rembg` (background removal)
- `Pillow` (image processing)
- `reportlab` (PDF generation)
- `tkinter` (GUI)

### Setup Steps
1. **Clone or Download the Repository:**
   ```powershell
   git clone https://github.com/Muhammad-Awais-khan/Zeb-Photo-App.git
   cd Zeb-Photo-App
   ```
2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```powershell
   python src/app.py
   ```

### Building an Executable (Optional)
To create a standalone Windows executable:
```powershell
pyinstaller --onefile --windowed --icon=src/icon.ico --add-data "src/bg.jpeg;." --add-data "src/icon.ico;." --add-data "src/haarcascade_frontalface_default.xml;." src/app.py
```
The executable will be in the `dist/` folder.

## Usage
1. **Launch the App:** Double-click the executable or run `python src/app.py`.
2. **Select Photo:** Click "Select Photo and Generate 9 Passport Pictures" and choose a JPG/PNG image.
3. **Options:**
   - *Use Blue Background*: Replace background with blue.
   - *Generate Single Picture*: Save only one passport photo (JPEG).
   - *Adjust Brightness/Contrast*: Enable and set values (0.1–3.0).
4. **Output:**
   - PDF or JPEG is saved to `Documents/Passports_Pics_PDFs`.
   - Success message shows the file path.

## File Structure
```
Zeb-Photo-App/
├── src/
│   ├── app.py                # Main GUI application
│   ├── main.py               # Image processing pipeline
│   ├── bg.jpeg               # Background image
│   ├── icon.ico              # App icon
│   ├── haarcascade_frontalface_default.xml # Face detection model
├── requirements.txt          # Python dependencies
├── info.txt                  # Setup information
├── license.txt               # License terms
├── build/                    # PyInstaller build output
```

## License
See `license.txt` for full terms. **Personal use only. Commercial use requires written permission.**

## Author
Muhammad Awais © 2025

## 📞 Support
For support or inquiries:  
- Email: **owaiskhan6605@gmail.com**  
- Phone: **+92-328-8690899**

## Support & Updates
- For bug reports or feature requests, open an issue on GitHub.
- Updates are provided only by the author.

---
**Disclaimer:** This software is provided "as is" without warranty. See `license.txt` for details.

---
[Download Zeb Photo App](https://github.com/Muhammad-Awais-khan/Zeb-Photo-App/raw/main/AppSetup.exe)

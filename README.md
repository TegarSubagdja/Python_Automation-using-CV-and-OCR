# Python Automation using CV and OCR

Automation project using Python, OpenCV, OCR (Tesseract), and screen interaction techniques for desktop automation.

This repository demonstrates two main automation approaches:

* Computer Vision (Template Matching)
* OCR Text Detection

The project also includes utility tools for:

* Creating OCR scan areas (ROI)
* Capturing object templates/icons from screen

---

# Features

## Computer Vision Automation

* Detect objects/icons on screen
* OpenCV template matching
* Real-time screen capture
* Automatic cursor movement
* Configurable matching threshold

## OCR Automation

* OCR text recognition using Tesseract
* Scan only specific screen regions (ROI)
* Text preprocessing for better accuracy
* Automatic coordinate detection
* Mouse movement to detected text

## Utility Tools

* Interactive area selector for OCR
* Interactive object/icon capture tool
* Automatic JSON ROI configuration
* Automatic template image creation

---

# Technologies Used

* Python
* OpenCV
* PyTesseract
* PyAutoGUI
* MSS
* Tkinter
* Pillow
* NumPy

---

# Library Dependencies

| Library       | Version   |
| ------------- | --------- |
| opencv-python | 4.13.0.92 |
| numpy         | 2.4.6     |
| PyAutoGUI     | 0.9.54    |
| pytesseract   | 0.3.13    |
| mss           | 10.2.0    |
| pyperclip     | 1.11.0    |

---

# Project Structure

```text id="29qk57"
project/
│
├── appCV.py
├── appOCR.py
├── MarkingAreaOCR.py
├── MarkingObject.py
├── requirements.txt
├── config_ocr.json
├── icon_target.png
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash id="6ktdgm"
git clone https://github.com/TegarSubagdja/Python_Automation-using-CV-and-OCR.git
cd Python_Automation-using-CV-and-OCR
```

---

## 2. Install Dependencies

Using requirements.txt:

```bash id="0eqbhq"
pip install -r requirements.txt
```

Example requirements.txt:

```txt id="ljg74f"
opencv-python==4.13.0.92
numpy==2.4.6
PyAutoGUI==0.9.54
pytesseract==0.3.13
mss==10.2.0
pyperclip==1.11.0
pillow
```

---

## 3. Install Tesseract OCR

Download Tesseract OCR:

https://github.com/UB-Mannheim/tesseract/wiki

Example installation path:

```text id="2x84t6"
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is not available in PATH:

```python id="nfdmkk"
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

# Computer Vision Detection

File:

```text id="l1wafh"
appCV.py
```

This module uses OpenCV Template Matching to locate an object/icon on the screen.

---

# Computer Vision Workflow

1. Load target icon image
2. Capture fullscreen screenshot
3. Convert screenshot to grayscale
4. Perform template matching
5. Find matching coordinates
6. Move cursor to detected object

---

# Template Matching Example

```python id="e9t7ls"
template = cv2.imread(
    'icon_target.png',
    cv2.IMREAD_GRAYSCALE
)

res = cv2.matchTemplate(
    screenshot_gray,
    template,
    cv2.TM_CCOEFF_NORMED
)
```

---

# Matching Threshold

```python id="0d1vlx"
threshold = 0.6
```

* Higher value → more accurate
* Lower value → easier detection but more false positives

---

# OCR Detection

File:

```text id="tvk38n"
appOCR.py
```

This module uses Tesseract OCR to detect text from a selected screen area.

---

# OCR Workflow

1. Load ROI configuration
2. Capture screenshot from ROI
3. Convert image to grayscale
4. Resize image for better OCR
5. Apply threshold preprocessing
6. Run OCR detection
7. Compare detected text
8. Move cursor to detected text

---

# OCR Preprocessing

## Grayscale

```python id="v11g3l"
gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)
```

## Resize

```python id="ekjv95"
gray = cv2.resize(
    gray,
    None,
    fx=2,
    fy=2,
    interpolation=cv2.INTER_CUBIC
)
```

## Threshold

```python id="bbl1g4"
thresh = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)[1]
```

---

# OCR Example

```python id="tnksiy"
scan_text_in_roi("rotaryp")
```

---

# ROI Configuration Tool

File:

```text id="4uvqsr"
MarkingAreaOCR.py
```

This utility helps users create OCR scan regions interactively.

---

# ROI Tool Features

* Fullscreen transparent overlay
* Drag-and-select area
* Automatically saves ROI coordinates
* Generates config_ocr.json

---

# Generated Configuration Example

```json id="wjlwmj"
{
    "x": 1020,
    "y": 152,
    "width": 899,
    "height": 874
}
```

---

# Running ROI Selector

```bash id="zmttfu"
python MarkingAreaOCR.py
```

---

# Object/Icon Capture Tool

File:

```text id="j1b6ln"
MarkingObject.py
```

This utility captures a selected screen object and saves it as template image for OpenCV matching.

---

# Object Capture Features

* Fullscreen overlay
* Drag-and-select object
* Automatic image cropping
* Save object as PNG template

---

# Generated File

```text id="qxl4yo"
icon_target.png
```

---

# Running Object Capture Tool

```bash id="g4dg0q"
python MarkingObject.py
```

---

# Running Main Applications

## Run Computer Vision Detection

```bash id="25zwnf"
python appCV.py
```

## Run OCR Detection

```bash id="p9xg0m"
python appOCR.py
```

---

# Example Output

## CV Detection

```text id="wt0b7h"
Ikon ditemukan! Titik tengah: X=1200, Y=450
```

## OCR Detection

```text id="tmgj6d"
[SUKSES] 'rotaryp' ditemukan
Confidence: 95
Koordinat: X=1450 Y=520
```

---

# Build to EXE

Install PyInstaller:

```bash id="9qzr7z"
pip install pyinstaller
```

Build application:

```bash id="khs4h7"
pyinstaller --onefile appOCR.py
```

---

# Use Cases

* Desktop automation
* RPA automation
* Marketplace automation
* UI interaction automation
* OCR workflow
* Screen monitoring
* Automated clicking system

---

# Performance Tips

* Use smaller ROI areas for faster OCR
* Use high-quality screenshots
* Increase image scale for small text
* Avoid noisy backgrounds
* Tune threshold carefully

---

# Requirements

* Python 3.10+
* Windows OS recommended
* Tesseract OCR

---

# Running Selenium 

```text
Path : "C:\ChromeAutomation"
```

```bash 
taskkill /F /IM chrome.exe
```
```bash 
mkdir "C:\ChromeAutomation\User Data"
```
```bash 
xcopy "C:\Users\kingt\AppData\Local\Google\Chrome\User Data\Profile 1" "C:\ChromeAutomation\User Data\Profile 1" /E /H /C /I /Y
```
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeAutomation\User Data" --profile-directory="Profile 1"
```

# Virtual Environment & Offline Dependencies

This project uses Python virtual environment (`venv`) to isolate dependencies and avoid conflicts with global Python packages.

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment (Windows):

```bash
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate dependency list:

```bash
pip freeze > requirements.txt
```

Download offline dependency packages:

```bash
pip download -r requirements.txt -d packages
```

Install dependencies from offline packages:

```bash
pip install --no-index --find-links=packages -r requirements.txt
```

This allows the project to be rebuilt and installed even without internet connection.

# License

This project is intended for educational and automation purposes.
"# Python_Automation-using-CV-and-OCR" 
"# Python_Automation-using-CV-and-OCR" 
"# Python_Automation-using-CV-and-OCR" 

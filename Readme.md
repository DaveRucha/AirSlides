# 🖐️ AirSlides – Gesture-Controlled Slide Narration System

**AirSlides** is a real-time, contactless presentation tool that lets you control slides and narrate them using only hand gestures — no remotes, no clicking, no touching.

Built using Python, OpenCV, Mediapipe, and gTTS, it enables a fully hygienic and intuitive presentation experience.

---

## 🚀 Features

| Gesture         | Action                         |
|-----------------|--------------------------------|
| ✋ Palm         | Next Slide                     |
| ✌️ V Sign       | Previous Slide                 |
| ☝️ Point        | Toggle Pointer (red dot)       |
| 👌 OK Sign      | Toggle Draw Mode (whiteboard)  |
| 🤘 Rock Sign    | Clear Drawing                  |
| 🤙 L Sign       | Toggle Slide Narration         |

🎤 Narration is powered by:
- **OCR** using `pytesseract`
- **Text-to-Speech** using `gTTS` + `pygame.mixer`

---

## 🛠 Installation

1. Install **Python 3.8 to 3.11** from [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Install **Tesseract OCR**:
   - Download from: https://github.com/tesseract-ocr/tesseract
   - Add its install path to your system's `PATH`

4. Install **Poppler for Windows** (for PDF conversion):
   - Download from: http://blog.alivate.com.au/poppler-windows/
   - Add the `bin/` folder to your `PATH`

---

## ▶️ How to Run

1. Launch the app:

```bash
python airslides.py
```

2. When prompted, enter the path to a **PDF file** of your slides.

3. Use hand gestures in front of your webcam to:
   - Navigate slides
   - Draw and highlight
   - Narrate the slide content out loud

---

## 💡 Why AirSlides?

- ✅ 100% Touchless
- ✅ Real-time OCR and narration
- ✅ Works offline (no internet required)
- ✅ Great for educators, demos, recordings

---

## 📦 Requirements

- Python 3.8–3.11
- Webcam
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](http://blog.alivate.com.au/poppler-windows/)
- Python packages:
  - opencv-python
  - mediapipe
  - pytesseract
  - gTTS
  - pygame
  - pdf2image
  - Pillow
  - pywinauto

---

## 👤 Author

**Created by Rucha Avinash Dave**

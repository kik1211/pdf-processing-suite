# I HATE PDF

> **Because PDFs shouldn't make you suffer.**

A lightweight, fully local web application that combines 10 essential PDF utilities into one seamless interface. No subscriptions, no cloud uploads, and no switching between five different websites just to manage your documents.

---

## Why I Built This
I was tired of dealing with online PDF tools that impose arbitrary file size limits, require premium subscriptions for basic tasks, and force you to upload sensitive documents to remote servers. **I HATE PDF** runs 100% locally on your machine, ensuring complete privacy and zero friction.

## Features
* **100% Local Processing:** Your files never leave your computer.
* **Batch Color Inversion:** Perfect for reading scanned documents or textbooks in dark mode without eye strain.
* **Page Management:** Merge, split, rotate, and rearrange pages effortlessly.
* **Image & Watermark Tools:** Precisely stamp images or add watermarks to your PDFs.
* **Compression:** Reduce file sizes for easy sharing.
* **Blank Page Insertion:** Add space exactly where you need it.

## Technology Stack
* **Backend:** Python, Flask
* **PDF Processing:** PyMuPDF (`fitz`), PyPDF2
* **Image Processing:** Pillow, NumPy
* **Frontend:** HTML5, CSS3, Vanilla JS

---

## Getting Started

### Prerequisites
* Python 3.10 or higher
* Git

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/kik1211/pdf-processing-suite.git
   cd pdf-processing-suite
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Simply double-click the `run_app.bat` file (on Windows), or run:
   ```bash
   python app.py
   ```

4. **Open in your browser:**
   Navigate to `http://127.0.0.1:5000` to start using the tools!

---

## Future Roadmap
- [ ] OCR Text Recognition
- [ ] Password Protection & Encryption
- [ ] Digital Signatures
- [ ] PDF Metadata Editor

---

## License
This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

*Built by [Kiruthik R S](https://github.com/kik1211).*

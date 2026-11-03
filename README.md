# PDF Processing Suite

A Python and Flask web application providing essential PDF document manipulation, page reordering, and batch color inversion in a unified interface.

---

## Overview

Unlike public third-party services with subscription paywalls and external file upload requirements, **PDF Processing Suite** runs directly on your own host environment.

All processing is executed on the machine hosting the Flask application. When run locally (e.g., on `localhost` or `127.0.0.1`), files remain on your local disk within the `uploads/` directory without third-party data transmission. If deployed to a remote server, uploaded files are processed and temporarily stored on that remote host.

### Key Capabilities

- **Host-Based Execution:** Uploaded files are written to the host's `uploads/` directory and processed locally via PyMuPDF (`fitz`), PyPDF2, and Pillow without external cloud API dependencies.
- **Color Inversion (Dark Mode):** Inverts document page color profiles via raster manipulation to create dark-background reading formats for scanned notes and slides. *(Note: Pages are rasterized into bitmaps, so selectable text and vector layers are converted to images).*
- **Page Management:** Reorder, merge, split, and rotate individual or batch pages through an interactive web UI.
- **Stamping & Watermarking:** Stamp custom images, transparent overlay watermarks, or text annotations at designated page coordinates.
- **Lossy Document Compression:** Reduces PDF file sizes by rasterizing pages at 100 DPI and re-encoding them as JPEG images at quality 50.
- **Blank Page Insertion:** Insert standardized blank spacer pages at designated index offsets.

---

## Technical Architecture

The application is structured into a Flask web layer and a set of underlying PDF manipulation engines:

```
[ Browser / Client ] ──( HTTP POST / Multipart )──> [ Flask Routes in app.py ]
                                                            │
                                                            ▼
                                                 [ PyMuPDF / PyPDF2 Engines ]
                                                 [ Local uploads/ Storage   ]
                                                            │
                                                            ▼
[ Browser / Client ] <──( Binary File Stream )──── [ Download / ZIP Delivery ]
```

Detailed architectural layouts, directory structures, and data flow specifications are available in the [Architecture Guide](docs/ARCHITECTURE.md).

---

## Technology Stack

- **Backend Framework:** Python 3.11+, Flask
- **Document Engine:** PyMuPDF (`fitz`), PyPDF2
- **Image Manipulation:** Pillow (PIL), NumPy
- **Frontend Layer:** Semantic HTML5, Vanilla CSS, Jinja2 Templates, JavaScript (ES6)

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kik1211/pdf-processing-suite.git
   cd pdf-processing-suite
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application:
   ```bash
   python app.py
   ```
   *(On Windows, you can also launch directly by executing `run_app.bat`)*

5. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Development & Release History

See [docs/CHANGELOG.md](docs/CHANGELOG.md) for version release notes and recent interface enhancements.

---

## License

This project is licensed under the [MIT License](LICENSE).

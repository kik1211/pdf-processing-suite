# PDF Processing Suite

A privacy-focused, fully local web application and utility suite providing essential PDF document manipulation, page reordering, and batch color inversion in a unified interface.

---

## Overview

Most web-based PDF utility services enforce file size limits, rate constraints, subscription tiers, or require uploading sensitive documents to external cloud infrastructure. 

**PDF Processing Suite** executes all operations directly on the local host using Python and PyMuPDF (`fitz`), ensuring zero data egress, sub-second page manipulation, and complete privacy for scanned notes, textbooks, and enterprise documents.

### Key Capabilities

- **100% Local Processing:** Files are processed in memory and local temporary storage with zero remote telemetry or external API calls.
- **Batch Color Inversion:** Inverts document page color profiles via raster manipulation, creating dark-mode reading formats for scanned documents and slide decks without loss of clarity.
- **Page Management:** Reorder, merge, split, and rotate individual or batch pages through an interactive web UI.
- **Stamping & Watermarking:** Stamp custom images, transparent overlay watermarks, or annotations at arbitrary page coordinates.
- **Document Compression:** Optimize embedded streams and downsample imagery to reduce file footprints for distribution.
- **Blank Page Insertion:** Insert standardized blank spacer pages at designated index offsets.

---

## Technical Architecture

The application is structured into a Flask web layer and a set of underlying PDF manipulation engines:

```
[ Browser / Client ] ──( HTTP POST / Multipart )──> [ Flask Routes in app.py ]
                                                            │
                                                            ▼
                                                 [ PyMuPDF / PyPDF2 Engines ]
                                                            │
                                                            ▼
[ Browser / Client ] <──( Binary File Stream )──── [ Temporary Output Buffer ]
```

Detailed architectural layouts, directory structures, and data flow specifications are available in the [Architecture Guide](docs/ARCHITECTURE.md).

---

## Technology Stack

- **Backend Framework:** Python 3.10+, Flask
- **Document Engine:** PyMuPDF (`fitz`), PyPDF2
- **Image Manipulation:** Pillow (PIL), NumPy
- **Frontend Layer:** Semantic HTML5, Vanilla CSS, Jinja2 Templates, JavaScript (ES6)

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
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

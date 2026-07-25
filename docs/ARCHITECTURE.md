# Architecture

High-level architecture documentation for `pdf-processing-suite`.

---

## Project Overview
`pdf-processing-suite` is a Flask-based web application and utility suite designed for processing and manipulating PDF documents.

---

## Technology Stack
- **Backend Framework**: Python / Flask
- **PDF & Image Processing**: PyMuPDF (`fitz`), PyPDF2, Pillow, NumPy
- **Frontend Layer**: HTML5, Vanilla CSS, Jinja2 Templates

---

## Folder Structure
```text
pdf-processing-suite/
├── app.py                  # Main Flask application entry point
├── run_app.bat             # Development server runner script
├── .editorconfig           # Code formatting rules
├── .gitignore              # Version control ignore rules
├── requirements.txt        # Project dependencies
├── LICENSE                 # Project license
├── README.md               # Project overview
├── inverter/               # Standalone PDF inverter CLI scripts
├── templates/              # HTML frontend templates
├── static/                 # Static CSS stylesheets and web assets
├── uploads/                # Temporary runtime file upload storage
├── docs/                   # Engineering documentation
├── screenshots/            # UI screenshots
└── assets/                 # Repository assets
```

---

## High-Level Request Flow
```text
[ Browser / Client ] ──( HTTP POST Request )──> [ Flask Routes in app.py ]
                                                           │
                                                           ▼
                                                [ Processing Modules ]
                                                           │
                                                           ▼
[ Browser / Client ] <──( Download Attachment )─── [ Temp Upload Output ]
```

import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import io
import os

# Get the folder where the script is located
folder = os.path.dirname(os.path.abspath(__file__))

# List all PDF files in the folder (ignoring already inverted ones)
pdf_files = [
    f for f in os.listdir(folder)
    if f.endswith(".pdf") and not f.endswith("_inverted.pdf")
]

if not pdf_files:
    print("❗ No PDF files found to process.")
    exit()

for input_file in pdf_files:
    input_path = os.path.join(folder, input_file)
    output_file = os.path.splitext(input_file)[0] + "_inverted.pdf"
    output_path = os.path.join(folder, output_file)

    print(f"🔄 Inverting: {input_file}")

    try:
        doc = fitz.open(input_path)
        new_doc = fitz.open()

        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            arr = np.array(img)
            inverted_arr = 255 - arr
            inverted_img = Image.fromarray(inverted_arr)

            img_stream = io.BytesIO()
            inverted_img.save(img_stream, format="PNG")
            img_stream.seek(0)

            rect = fitz.Rect(0, 0, pix.width, pix.height)
            new_page = new_doc.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=img_stream.read())

        new_doc.save(output_path)
        print(f"✅ Saved: {output_file}\n")

    except Exception as e:
        print(f"❌ Error processing {input_file}: {e}")

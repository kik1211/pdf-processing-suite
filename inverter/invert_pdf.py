import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import io

# Load your PDF
input_path = "input.pdf"
output_path = "inverted.pdf"
doc = fitz.open(input_path)

# New PDF to store inverted pages
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

# Save output
new_doc.save(output_path)
print("✅ Done! Saved as", output_path)

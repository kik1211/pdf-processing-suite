from flask import Flask, render_template, request, send_file
import os
import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
from PyPDF2 import PdfMerger  # ✅ Move import to top
import re
import zipfile
from difflib import get_close_matches
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


from zipfile import ZipFile

@app.route('/invert', methods=['GET', 'POST'])
def invert():
    if request.method == 'POST':
        files = request.files.getlist('pdf')
        if not files or files[0].filename == '':
            return 'No files selected.'

        inverted_files = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            output_name = 'inverted_' + file.filename
            output_path = os.path.join(UPLOAD_FOLDER, output_name)

            doc = fitz.open(input_path)
            new_doc = fitz.open()

            for page in doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                arr = np.array(img)
                inverted_arr = 255 - arr
                inverted_img = Image.fromarray(inverted_arr)

                img_bytes = io.BytesIO()
                inverted_img.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                rect = fitz.Rect(0, 0, pix.width, pix.height)
                new_page = new_doc.new_page(width=rect.width, height=rect.height)
                new_page.insert_image(rect, stream=img_bytes.read())

            new_doc.save(output_path)
            inverted_files.append(output_path)

        # Create zip file of all inverted PDFs
        zip_path = os.path.join(UPLOAD_FOLDER, 'inverted_pdfs.zip')
        with ZipFile(zip_path, 'w') as zipf:
            for file_path in inverted_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)  # Clean up individual files

        return send_file(zip_path, as_attachment=True)

    return render_template('invert.html')


@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        if not files or files[0].filename == '':
            return 'No files selected.'

        merger = PdfMerger()

        saved_files = []
        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            saved_files.append(path)
            merger.append(path)

        output_path = os.path.join(UPLOAD_FOLDER, 'merged_output.pdf')
        merger.write(output_path)
        merger.close()

        # Clean up temporary files
        for f in saved_files:
            os.remove(f)

        return send_file(output_path, as_attachment=True)

    return render_template('merge.html')

from zipfile import ZipFile

@app.route('/split', methods=['GET', 'POST'])
def split_pdf():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        if not files or files[0].filename == '':
            return 'No files selected.'

        split_paths = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            doc = fitz.open(input_path)

            for i in range(len(doc)):
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=i, to_page=i)

                split_name = f"{os.path.splitext(file.filename)[0]}_page{i+1}.pdf"
                split_path = os.path.join(UPLOAD_FOLDER, split_name)
                new_doc.save(split_path)
                split_paths.append(split_path)

        # Create ZIP of all split PDFs
        zip_path = os.path.join(UPLOAD_FOLDER, 'split_pages.zip')
        with ZipFile(zip_path, 'w') as zipf:
            for path in split_paths:
                zipf.write(path, os.path.basename(path))
                os.remove(path)  # Clean up individual files

        return send_file(zip_path, as_attachment=True)

    return render_template('split.html')


@app.route('/compress', methods=['GET', 'POST'])
def compress_pdf():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        if not files or files[0].filename == '':
            return 'No PDF files selected.'

        compressed_paths = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            doc = fitz.open(input_path)
            new_doc = fitz.open()

            for page in doc:
                # Render the page with reduced resolution (e.g., 100 DPI instead of default)
                pix = page.get_pixmap(dpi=100)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Compress image by lowering quality
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="JPEG", quality=50)  # Lower quality = more compression
                img_bytes.seek(0)

                rect = fitz.Rect(0, 0, pix.width, pix.height)
                new_page = new_doc.new_page(width=rect.width, height=rect.height)
                new_page.insert_image(rect, stream=img_bytes.read())

            output_filename = os.path.splitext(file.filename)[0] + "_compressed.pdf"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            new_doc.save(output_path)
            compressed_paths.append(output_path)

        # Package into a ZIP
        zip_path = os.path.join(UPLOAD_FOLDER, 'compressed_pdfs.zip')
        with ZipFile(zip_path, 'w') as zipf:
            for path in compressed_paths:
                zipf.write(path, os.path.basename(path))
                os.remove(path)  # Clean up

        return send_file(zip_path, as_attachment=True)

    return render_template('compress.html')


# Helper to convert hex to RGBA tuple with alpha
def hex_to_rgba_int(hex_color, alpha=100):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b, alpha)


@app.route('/watermark', methods=['GET', 'POST'])
def watermark_pdf():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        watermark_text = request.form.get('watermark_text')
        font_size = int(request.form.get('font_size', 20))
        font_color = request.form.get('font_color', '#000000')
        rotation = float(request.form.get('rotation', 0))
        position = request.form.get('position', 'center')
        custom_x = int(request.form.get('custom_x', 100))
        custom_y = int(request.form.get('custom_y', 100))

        if not files or not watermark_text:
            return 'Please upload PDF(s) and enter watermark text.'

        output_files = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            doc = fitz.open(input_path)

            for page in doc:
                rect = page.rect
                width, height = rect.width, rect.height

                # Determine watermark coordinates
                if position == 'top':
                    x, y = width / 2, 50
                elif position == 'center':
                    x, y = width / 2, height / 2
                elif position == 'bottom':
                    x, y = width / 2, height - 50
                else:  # custom
                    x, y = custom_x, custom_y

                # Create watermark image using PIL
                canvas_width = 1000
                canvas_height = 200
                image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
                draw = ImageDraw.Draw(image)

                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = ImageFont.load_default()

                # Use getbbox for text dimension
                bbox = font.getbbox(watermark_text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                draw.text(
                    ((canvas_width - text_width) // 2, (canvas_height - text_height) // 2),
                    watermark_text,
                    font=font,
                    fill=hex_to_rgba_int(font_color, alpha=100)
                )

                rotated_img = image.rotate(rotation, expand=True)
                img_buffer = io.BytesIO()
                rotated_img.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                # Define placement rectangle on PDF
                img_rect = fitz.Rect(
                    x - rotated_img.width / 2,
                    y - rotated_img.height / 2,
                    x + rotated_img.width / 2,
                    y + rotated_img.height / 2
                )

                page.insert_image(img_rect, stream=img_buffer.read(), overlay=True)

            # Save the final PDF
            output_filename = 'watermarked_' + file.filename
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            doc.save(output_path)
            output_files.append(output_path)

        if len(output_files) == 1:
            return send_file(output_files[0], as_attachment=True)

        # If multiple PDFs, zip them
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for filepath in output_files:
                zipf.write(filepath, os.path.basename(filepath))
        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name='watermarked_files.zip', mimetype='application/zip')

    return render_template('watermark.html')

@app.route('/rotate', methods=['GET', 'POST'])
def rotate_pdf():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        rotate_target = request.form.get('rotate_target')  # 'portrait' or 'landscape'
        angle = int(request.form.get('angle', 90))
        direction = request.form.get('direction', 'clockwise')

        if not files or not rotate_target or not direction:
            return "Please upload PDF(s) and choose rotation settings."

        # Flip angle if anticlockwise
        if direction == 'clockwise':
            angle = -angle

        output_files = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            doc = fitz.open(input_path)
            new_doc = fitz.open()

            for page in doc:
                width, height = page.rect.width, page.rect.height
                orientation = 'landscape' if width > height else 'portrait'

                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                if orientation == rotate_target:
                    img = img.rotate(angle, expand=True)

                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                rotated_width, rotated_height = img.size
                rect = fitz.Rect(0, 0, rotated_width, rotated_height)
                new_page = new_doc.new_page(width=rotated_width, height=rotated_height)
                new_page.insert_image(rect, stream=img_bytes.read())

            output_filename = f"rotated_{file.filename}"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            new_doc.save(output_path)
            output_files.append(output_path)

        if len(output_files) == 1:
            return send_file(output_files[0], as_attachment=True)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for f in output_files:
                zipf.write(f, os.path.basename(f))
        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name='rotated_pdfs.zip')

    return render_template('rotate.html')

@app.route('/add_blank', methods=['GET', 'POST'])
def add_blank():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        position = request.form.get('position')
        after_page = int(request.form.get('after_page', 0)) - 1  # user enters 1-based
        num_blanks = int(request.form.get('num_blanks', 1))

        bg_color_hex = request.form.get('bg_color', '#FFFFFF')
        bg_rgb = tuple(int(bg_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        if not files:
            return 'Please upload at least one PDF.'

        output_files = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            doc = fitz.open(input_path)

            # Get size from first page
            ref_page = doc[0]
            width = ref_page.rect.width
            height = ref_page.rect.height

            # Determine insertion point
            if position == 'start':
                insert_at = 0
            elif position == 'end':
                insert_at = len(doc)
            elif position == 'after' and 0 <= after_page < len(doc):
                insert_at = after_page + 1
            else:
                return f"Invalid page number for file: {file.filename}"

            # Create blank image and insert
            for i in range(num_blanks):
                img = Image.new("RGB", (int(width), int(height)), color=bg_rgb)
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                page_index = insert_at + i
                doc.insert_page(page_index, width=width, height=height)
                page = doc[page_index]
                rect = page.rect
                page.insert_image(rect, stream=img_buffer.read())

            # Save output
            output_path = os.path.join(UPLOAD_FOLDER, 'blanked_' + file.filename)
            doc.save(output_path)
            output_files.append(output_path)

        if len(output_files) == 1:
            return send_file(output_files[0], as_attachment=True)

        # Multiple files: return zipped
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for path in output_files:
                zipf.write(path, os.path.basename(path))
        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name='blanked_files.zip', mimetype='application/zip')

    return render_template('add_blank.html')
@app.route('/paste_image', methods=['GET', 'POST'])
def paste_image():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        image_file = request.files.get('image')
        page_number = int(request.form.get('page_number', 1)) - 1
        x = int(request.form.get('x', 0))
        y = int(request.form.get('y', 0))

        use_original_size = request.form.get('use_original_size') == 'yes'

        if not files or not image_file:
            return 'Upload at least one PDF and one image.'

        image = Image.open(image_file)

        # Calculate image dimensions
        if use_original_size:
            # Convert pixels to points (assuming 72 DPI)
            dpi = image.info.get('dpi', (72, 72))
            img_width_pt = (image.width / dpi[0]) * 72
            img_height_pt = (image.height / dpi[1]) * 72
        else:
            img_width_pt = int(request.form.get('img_width', 100))
            img_height_pt = int(request.form.get('img_height', 100))
            image = image.resize((int(img_width_pt), int(img_height_pt)))

        # Prepare image buffer
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img_data = img_buffer.read()

        output_files = []

        for file in files:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            doc = fitz.open(input_path)

            if page_number < 0 or page_number >= len(doc):
                return f"Invalid page number for {file.filename}"

            page = doc[page_number]
            rect = fitz.Rect(x, y, x + img_width_pt, y + img_height_pt)
            page.insert_image(rect, stream=img_data)

            output_path = os.path.join(UPLOAD_FOLDER, 'image_added_' + file.filename)
            doc.save(output_path)
            output_files.append(output_path)

        if len(output_files) == 1:
            return send_file(output_files[0], as_attachment=True)

        # Multiple files: zip them
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for path in output_files:
                zipf.write(path, os.path.basename(path))
        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name='pasted_images.zip', mimetype='application/zip')

    return render_template('paste_image.html')



@app.route('/edit_pages', methods=['GET', 'POST'])
def edit_pages():
    if request.method == 'POST':
        pdf_file = request.files.get('pdf')
        action = request.form.get('action')

        if not pdf_file or not action:
            return "Please upload a PDF and choose an action."

        input_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(input_path)
        doc = fitz.open(input_path)

        if action == 'remove':
            remove_str = request.form.get('remove_pages', '')
            pages_to_remove = parse_page_numbers(remove_str, len(doc))
            for i in sorted(pages_to_remove, reverse=True):
                if 0 <= i < len(doc):
                    doc.delete_page(i)

        elif action == 'cutpaste':
            cut_page = int(request.form.get('cut_page', 0)) - 1
            paste_after = int(request.form.get('paste_after_page', -1))
            if 0 <= cut_page < len(doc):
                cut_pdf = fitz.open()
                cut_pdf.insert_pdf(doc, from_page=cut_page, to_page=cut_page)
                doc.delete_page(cut_page)
                paste_at = paste_after if paste_after < len(doc) else len(doc) - 1
                doc.insert_pdf(cut_pdf, start_at=paste_at + 1)

        elif action == 'swap':
            a = int(request.form.get('page_a', 0)) - 1
            b = int(request.form.get('page_b', 0)) - 1
            if 0 <= a < len(doc) and 0 <= b < len(doc) and a != b:
                temp_a = fitz.open()
                temp_b = fitz.open()
                temp_a.insert_pdf(doc, from_page=a, to_page=a)
                temp_b.insert_pdf(doc, from_page=b, to_page=b)
                doc.delete_page(max(a, b))
                doc.delete_page(min(a, b))
                doc.insert_pdf(temp_b, start_at=min(a, b))
                doc.insert_pdf(temp_a, start_at=max(a, b))

        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='edited.pdf', mimetype='application/pdf')

    return render_template('edit_pages.html')

def parse_page_numbers(page_str, total_pages):
    result = set()
    if not page_str:
        return result
    parts = page_str.replace(' ', '').split(',')
    for part in parts:
        if '-' in part:
            start, end = part.split('-')
            result.update(range(int(start) - 1, int(end)))
        else:
            result.add(int(part) - 1)
    return [p for p in result if 0 <= p < total_pages]

@app.route('/batch_invert', methods=['GET', 'POST'])
def batch_invert():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')

        if not files:
            return "<h3>No files uploaded.</h3>"

        output_files = []

        for file in files:
            try:
                # Open uploaded file using PyMuPDF
                input_pdf = fitz.open(stream=file.read(), filetype="pdf")
                new_doc = fitz.open()

                for page in input_pdf:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # Invert the colors
                    arr = np.array(img)
                    inverted_arr = 255 - arr
                    inverted_img = Image.fromarray(inverted_arr)

                    # Convert back to PDF page
                    img_stream = io.BytesIO()
                    inverted_img.save(img_stream, format="PNG")
                    img_stream.seek(0)

                    rect = fitz.Rect(0, 0, pix.width, pix.height)
                    new_page = new_doc.new_page(width=rect.width, height=rect.height)
                    new_page.insert_image(rect, stream=img_stream.read())

                # Save final inverted PDF to memory
                buffer = io.BytesIO()
                new_doc.save(buffer)
                buffer.seek(0)
                output_files.append((file.filename.replace('.pdf', '_inverted.pdf'), buffer))

            except Exception as e:
                return f"<h3>Error processing {file.filename}: {e}</h3>"

        # Return single PDF or ZIP depending on file count
        if len(output_files) == 1:
            filename, file_buffer = output_files[0]
            return send_file(file_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
        else:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zipf:
                for filename, buffer in output_files:
                    zipf.writestr(filename, buffer.read())
            zip_buffer.seek(0)
            return send_file(zip_buffer, as_attachment=True, download_name="inverted_pdfs.zip", mimetype="application/zip")

    return render_template('batch_invert.html')

if __name__ == '__main__':
    app.run(debug=True)

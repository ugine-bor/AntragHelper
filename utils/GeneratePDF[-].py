from PyPDF2 import PdfReader, PdfWriter

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

import os
import zipfile


async def makepdf(uid, fname, lname, data):
    w, h = A4
    c = canvas.Canvas(f"userPDFdata/Data_{uid}.pdf", pagesize=A4)
    c.setFont("Helvetica", 16)
    c.drawString(50, h - 50, f"Data from {fname} {lname} (id-{uid}):")
    ypos = 34
    for k, v in data.items():
        c.drawString(50, h - 50 - ypos, f"{k}: {v}")
        ypos += 26
    c.save()


def find_text_boxes(pdf_file):
    pdf = PdfReader(pdf_file)
    text_boxes = []

    for page_num, page in enumerate(pdf.pages):
        if '/Annots' in page:
            annotations = page['/Annots']
            for annotation in annotations:
                annotation = annotation.get_object()  # Get the underlying dictionary object
                if '/Subtype' in annotation and annotation['/Subtype'] == '/Widget':
                    if '/FT' in annotation and annotation['/FT'] == '/Tx':
                        text_boxes.append(annotation)

    return text_boxes


def fill_text_boxes(pdf_file, filled_pdf_file, text_values):
    pdf = PdfReader(pdf_file)
    writer = PdfWriter()
    count = len(text_values)
    modified_annotations = []

    for page_num, page in enumerate(pdf.pages):  # for page_num, page in enumerate(pdf.pages):
        if '/Annots' in page:
            annotations = page['/Annots']
            if count != 0:
                for annotation in annotations:
                    annotation = annotation.get_object()  # Get the underlying dictionary object
                    if '/Subtype' in annotation and annotation['/Subtype'] == '/Widget':
                        if '/FT' in annotation and annotation['/FT'] == '/Tx':
                            if count == 0:
                                break
                            x = annotation['/Rect'][0]
                            y = float(annotation['/Rect'][3]) - 13

                            text = str(text_values[annotation['/TU']])
                            packet = BytesIO()

                            c = canvas.Canvas(packet)
                            c.setFont('Helvetica', 11)
                            c.drawString(x, y, text)
                            c.save()

                            packet.seek(0)
                            overlay_pdf = PdfReader(packet)
                            overlay_page = overlay_pdf.pages[0]
                            page.merge_page(overlay_page)

                            count -= 1
                            modified_annotations.append(annotation)
        writer.add_page(pdf.pages[page_num])  # Add the modified page to the writer

    with open(filled_pdf_file, 'wb') as output_file:
        writer.write(output_file)


def zip_pdf_files(folder_path, zip_filename):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        return

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            zipf.write(pdf_path, pdf_file)

    # Remove PDF files after zipping
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        os.remove(pdf_path)


async def fillpdf(uid, data, free=False):
    if not free:
        for fname in os.listdir("formulars"):
            dct = {}
            for box, v in zip(find_text_boxes(f"formulars/{fname}"), data.values()):
                dct[box['/TU']] = v
            fill_text_boxes(f"formulars/{fname}", f"UserFiles/U_{uid}/PDFs/{fname}", dct)
    else:
        dct = {}
        for box, v in zip(find_text_boxes(f"formulars/Hauptantrag.pdf"), data.values()):
            dct[box['/TU']] = v
        fill_text_boxes(f"formulars/Hauptantrag.pdf", f"UserFiles/U_{uid}/PDFs/Hauptantrag.pdf", dct)
    zip_pdf_files(folder_path=f"UserFiles/U_{uid}/PDFs", zip_filename=f"UserFiles/U_{uid}/PDFs/Filled_Docs.zip")

import os
import docx
import pdfplumber
import fitz 
import numpy as np
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def pdf_to_text(file_path):
    """Extract text from PDF using pdfplumber (best for selectable text)."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"⚠️ Error reading PDF with pdfplumber: {e}")
    return text

def fallback_pdf_to_text(file_path):
    """Fallback: Extract text from PDF using PyMuPDF (if pdfplumber fails)."""
    text = ""
    try:
        document = fitz.open(file_path)
        for page in document:
            page_text = page.get_text("text")
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"⚠️ Error reading PDF with PyMuPDF: {e}")
    return text

def ocr_pdf_to_text(file_path):
    """Extract text from image-based PDFs using PaddleOCR."""
    extracted_text = ""
    try:
        pages = convert_from_path(file_path, 300)  
        for page in pages:
            page_np = np.array(page)
            result = ocr.ocr(page_np, cls=True) 
            
            for line in result:
                for word_info in line:
                    extracted_text += word_info[1][0] + " " 
    except Exception as e:
        print(f"⚠️ Error performing OCR on PDF file '{file_path}': {e}")
    return extracted_text

def read_docx(file_path):
    """Extract text from DOCX files."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"⚠️ Error reading DOCX file: {e}")
    return text

def save_text_to_file(text, output_path):
    """Save extracted text to a .txt file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def extract_txt(file_path, output_txt_dir):
    """Extract text from PDF/DOCX and save as .txt."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == '.pdf':
        text = pdf_to_text(file_path)
        if not text.strip():
            print("ℹ️ No text extracted with pdfplumber, trying PyMuPDF...")
            text = fallback_pdf_to_text(file_path)
        if not text.strip():
            print("ℹ️ No text extracted with PyMuPDF, using PaddleOCR...")
            text = ocr_pdf_to_text(file_path)  
    elif ext == '.docx':
        text = read_docx(file_path)
    else:
        print(f"❌ Unsupported file format: {file_path}")
        return None

    if not text.strip():
        print(f"⚠️ No text extracted from {file_path}")
        return None

    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    output_txt_path = os.path.join(output_txt_dir, f"{base_filename}.txt")
    save_text_to_file(text, output_txt_path)
    print(f"✅ Saved: {output_txt_path}")

    return output_txt_path 


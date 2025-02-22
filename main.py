import os
from extract_text import extract_txt

# Directories
INPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\PDF directory"
OUTPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\processed_text"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_files():
    """Processes all PDFs and DOCX files in INPUT_DIR."""
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith((".pdf", ".docx")):
            input_path = os.path.join(INPUT_DIR, filename)
            extract_txt(input_path, OUTPUT_DIR)

if __name__ == "__main__":
    process_files()

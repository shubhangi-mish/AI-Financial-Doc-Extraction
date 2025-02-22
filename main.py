import os
from extract_text import extract_text_from_pdf

# Define input/output directories
INPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\PDF directory"
TXT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\Text directory"

# Ensure output directory exists
os.makedirs(TXT_DIR, exist_ok=True)

def process_pdfs():
    """Reads PDFs from INPUT_DIR, extracts text, and saves to OUTPUT_DIR."""
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(TXT_DIR, output_filename)

            # Extract text from PDF
            text = extract_text_from_pdf(input_path)

            # Save text to file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"✅ Processed: {filename} → {output_filename}")

if __name__ == "__main__":
    process_pdfs()

import os
from extract_text import extract_txt
from extra import save_extracted_data_as_markdown  # Updated function

# Directories
INPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\PDF directory"
OUTPUT_TEXT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\processed_text"
OUTPUT_MARKDOWN_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\extracted_tables_markdown"  # Updated

# Ensure output directories exist
os.makedirs(OUTPUT_TEXT_DIR, exist_ok=True)
os.makedirs(OUTPUT_MARKDOWN_DIR, exist_ok=True)  # Ensure Markdown output directory exists

def process_files():
    """
    1️⃣ Extracts text from PDFs/DOCX in `INPUT_DIR`
    2️⃣ Sends extracted text to LLM for financial table extraction
    3️⃣ Saves structured Markdown output in `OUTPUT_MARKDOWN_DIR`
    """
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith((".pdf", ".docx")):
            input_path = os.path.join(INPUT_DIR, filename)

            print(f"📄 Processing: {filename}")

            # Step 1: Extract Text
            output_txt_path = extract_txt(input_path, OUTPUT_TEXT_DIR)

            if output_txt_path:
                print(f"✅ Extracted text saved at: {output_txt_path}")

                # Step 2: Send Extracted Text to LLM for Markdown Table Extraction
                extracted_markdown_path = save_extracted_data_as_markdown(output_txt_path, OUTPUT_MARKDOWN_DIR)

                if extracted_markdown_path:
                    print(f"🎯 Financial data saved in Markdown format at: {extracted_markdown_path}")
                else:
                    print(f"⚠️ No financial data was extracted from {filename}")
            else:
                print(f"❌ Failed to extract text from {filename}")

if __name__ == "__main__":
    process_files()

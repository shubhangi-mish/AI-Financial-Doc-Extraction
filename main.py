import os
from extract_text import extract_txt
from extract_md_from_llm import save_extracted_data_as_markdown 
from relabelled_md import relabel_balance_sheet  

INPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\PDF directory"
OUTPUT_TEXT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\processed_text"
OUTPUT_MARKDOWN_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\extracted_tables_markdown"
OUTPUT_RELABELED_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\relabelled_markdown"
VOCAB_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\vocabulary of allowed terms.rtf"

os.makedirs(OUTPUT_TEXT_DIR, exist_ok=True)
os.makedirs(OUTPUT_MARKDOWN_DIR, exist_ok=True)
os.makedirs(OUTPUT_RELABELED_DIR, exist_ok=True)

def process_files():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith((".pdf", ".docx")):
            input_path = os.path.join(INPUT_DIR, filename)

            print(f"📄 Processing: {filename}")

            output_txt_path = extract_txt(input_path, OUTPUT_TEXT_DIR)

            if output_txt_path:
                print(f"✅ Extracted text saved at: {output_txt_path}")

                extracted_markdown_path = save_extracted_data_as_markdown(output_txt_path, OUTPUT_MARKDOWN_DIR)

                if extracted_markdown_path:
                    print(f"🎯 Financial data saved in Markdown at: {extracted_markdown_path}")

                    relabeled_markdown_path = relabel_balance_sheet(
                        extracted_markdown_path, VOCAB_FILE, OUTPUT_RELABELED_DIR
                    )

                    if relabeled_markdown_path:
                        print(f"🔄 Relabeled financial data saved at: {relabeled_markdown_path}")
                    else:
                        print(f"⚠️ Relabeling failed for {filename}")

                else:
                    print(f"⚠️ No financial data was extracted from {filename}")
            else:
                print(f"❌ Failed to extract text from {filename}")

if __name__ == "__main__":
    process_files()

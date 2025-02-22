import os
import google.generativeai as genai
from dotenv import load_dotenv
import docx2txt
import PyPDF2
from striprtf.striprtf import rtf_to_text  # New: Extract text from RTF without Pandoc

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_file(file_path):
    """Extracts text from RTF, DOCX, or PDF files."""
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".rtf":
        with open(file_path, "r", encoding="utf-8") as f:
            return rtf_to_text(f.read())  # Convert RTF to plain text
    elif ext.lower() == ".docx":
        return docx2txt.process(file_path)  # Extract text from DOCX
    elif ext.lower() == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def relabel_balance_sheet(markdown_path, vocab_path, output_dir):
    """
    Reads a Markdown file, sends it along with a vocabulary list to the LLM,
    and gets the re-labeled Balance Sheet table.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the Markdown content
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Extract text from vocabulary file
    vocab_terms = extract_text_from_file(vocab_path)

    # LLM Prompt
    prompt = f"""
    You are an AI that relabels items in this markdown using a given vocabulary.
    
    Task:
    - Re-label the extracted items by mapping them to the closest corresponding terms in the provided vocabulary list.
    - Maintain the original structure and values of the table.
    - Only update the labels.

    Vocabulary List:
    {vocab_terms}

    Original Data (in Markdown format):
    {markdown_content}

    Provide the updated table in Markdown format without any explanation.
    """

    try:
        # Initialize model properly and clear cache
        model = genai.GenerativeModel("gemini-1.5-pro")  # Ensure model is defined
        del model  # Remove any cached instance
        model = genai.GenerativeModel("gemini-1.5-pro")  # Fresh instance

        # Generate response from LLM
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 1.0, "top_p": 0.9, "max_output_tokens": 1024}
        )

        # Extract modified Markdown table
        modified_markdown = response.text

        # Save the modified markdown file
        output_filename = os.path.basename(markdown_path).replace(".md", "_relabelled.md")
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(modified_markdown)

        print(f"✅ Re-labeled Balance Sheet saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"⚠️ Error during relabeling: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    MARKDOWN_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\extracted_tables_markdown\vodafone_annual_report_reduced.md"
    VOCAB_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\vocabulary of allowed terms.rtf"  # Can be RTF, DOCX, or PDF
    OUTPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\relabelled_markdown"

    relabel_balance_sheet(MARKDOWN_FILE, VOCAB_FILE, OUTPUT_DIR)

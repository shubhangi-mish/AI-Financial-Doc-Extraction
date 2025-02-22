import os
import google.generativeai as genai
from dotenv import load_dotenv
import docx2txt
import PyPDF2
from striprtf.striprtf import rtf_to_text  

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_file(file_path):
    """Extracts text from RTF, DOCX, or PDF files."""
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".rtf":
        with open(file_path, "r", encoding="utf-8") as f:
            return rtf_to_text(f.read()) 
    elif ext.lower() == ".docx":
        return docx2txt.process(file_path) 
    elif ext.lower() == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def relabel_balance_sheet(markdown_path, vocab_path, output_dir):

    os.makedirs(output_dir, exist_ok=True)


    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()


    vocab_terms = extract_text_from_file(vocab_path)

    prompt = f"""
    You are an AI that relabels items in this markdown using a given vocabulary.
    
    Task:
    - Re-label the extracted items by mapping them to the closest corresponding terms in the provided vocabulary list.
    - Maintain the original structure and values of the table.
    - Only update the labels do not add or delete any row cloumn.

    use this example:
    Balance Sheet (Excerpt)

-----------------------

Line Item           Year 1   Year 2

Cash and Equivalents 10,000   12,000
Trade Receivables    8,000    9,000
Short-term Debt      5,000    6,000



You might produce a Markdown table such as:

Line Item                      Year 1   Year 2

Cash                           10,000   12,000
Accts Rec-Trade (Trade Debtors) 8,000   9,000
Overdraft and Short Term Debt   5,000   6,000


    Vocabulary List:
    {vocab_terms}

    Original Data (in Markdown format):
    {markdown_content}

    Provide the updated table in Markdown format without any explanation.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro") 
        del model  
        model = genai.GenerativeModel("gemini-1.5-pro")

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 1.0, "top_p": 0.9}
        )

        modified_markdown = response.text
        print(modified_markdown)

        output_filename = os.path.basename(markdown_path).replace(".md", "_relabelled.md")
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(modified_markdown)

        print(f"✅ Re-labeled Balance Sheet saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"⚠️ Error during relabeling: {e}")
        return None

if __name__ == "__main__":
    MARKDOWN_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\extracted_tables_markdown\vodafone_annual_report_reduced.md"
    VOCAB_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\vocabulary of allowed terms.rtf"  # Can be RTF, DOCX, or PDF
    OUTPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\relabelled_markdown"

    relabel_balance_sheet(MARKDOWN_FILE, VOCAB_FILE, OUTPUT_DIR)

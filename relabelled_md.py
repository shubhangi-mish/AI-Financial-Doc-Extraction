import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def load_vocabulary(vocab_path):
    """Reads the vocabulary list from a text file."""
    with open(vocab_path, "r", encoding="utf-8") as f:
        return f.read()

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

    # Load vocabulary list
    vocab_terms = load_vocabulary(vocab_path)

    # LLM Prompt
    prompt = f"""
    You are an AI that relabels financial Balance Sheet line items using a given vocabulary.
    
    Task:
    - Re-label the extracted Balance Sheet table line items by mapping them to the closest corresponding terms in the provided vocabulary list.
    - Maintain the original structure and values of the table.
    - Only update the labels.

    Vocabulary List:
    {vocab_terms}

    Original Balance Sheet (in Markdown format):
    {markdown_content}

    Provide the updated table in Markdown format without any explanation.
    """

    try:
        # Send to LLM
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

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
    MARKDOWN_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\extracted_markdown\balance_sheet.md"
    VOCAB_FILE = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\vocabulary.txt"
    OUTPUT_DIR = r"C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\relabelled_markdown"

    relabel_balance_sheet(MARKDOWN_FILE, VOCAB_FILE, OUTPUT_DIR)

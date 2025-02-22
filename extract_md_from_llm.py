import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def extract_financial_tables_markdown(text):
    
    prompt = f"""
    Extract financial tables from the given document and present them in a **tabular format** using Markdown.

    Identify:
    1. Balance Sheet
    2. Income Statement
    3. Cash Flow Statement

    Consider synonyms and closely related tables(e.g., "cash flow" could be "comprehensive income") and extract them and give them for sure.

    If any table is missing, **mention that explicitly**.

    **Output format (Markdown tables only, no extra text):**
     
    | Category  | Value |
    |-----------|-------|
    | Revenue   | $XXX  |
    | Expenses  | $XXX  |


    **Strictly return Markdown output only.**
    
    Document Text:
    {text}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        extracted_markdown = response.text.strip()
        return extracted_markdown  
    
    except Exception as e:
        print(f"⚠️ Gemini Extraction Error: {e}")
        return None

def save_extracted_data_as_markdown(output_txt_path, output_dir="extracted_tables_markdown"):
    
    if not os.path.exists(output_txt_path):
        print(f"❌ Error: File {output_txt_path} not found!")
        return None

    try:
        with open(output_txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        extracted_markdown = extract_financial_tables_markdown(text)
        
        if extracted_markdown:
            os.makedirs(output_dir, exist_ok=True)  

            filename = os.path.basename(output_txt_path).replace(".txt", ".md")
            markdown_output_path = os.path.join(output_dir, filename)

            with open(markdown_output_path, "w", encoding="utf-8") as f:
                f.write(extracted_markdown)

            print(f"✅ Financial data saved in Markdown: {markdown_output_path}")
            return markdown_output_path
        else:
            print("⚠️ No financial data extracted.")
            return None

    except Exception as e:
        print(f"❌ Error while processing the file: {e}")
        return None


save_extracted_data_as_markdown(r'C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\processed_text\vodafone_annual_report_reduced.txt')

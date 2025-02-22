import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def extract_financial_tables(text):
    """Send text to Gemini and extract financial tables in JSON format."""
    
    prompt = f"""
    Extract financial tables from the given document. Identify:
    1. Balance Sheet
    2. Income Statement
    3. Cash Flow Statement

    Consider looking for similar terms (e.g., "cash flow" may be written as "comprehensive income").
    Extract data accurately.

    If a table is missing, return `null`.

    Provide output in **strict JSON format** without any explanation:
    {{
        "balance_sheet": {{...}},
        "income_statement": {{...}},
        "cash_flow": {{...}}
    }}

    Document Text:
    {text}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        extracted_data = response.text.strip()

        # ✅ Clean unwanted text if present
        if extracted_data.startswith("json '''"):
            extracted_data = extracted_data.replace("json '''", "").replace("'''", "").strip()

        return extracted_data  # ✅ Return raw JSON text
    
    except Exception as e:
        print(f"⚠️ Gemini Extraction Error: {e}")
        return None

def save_extracted_data(output_txt_path, output_dir="extracted_tables_json"):
    """Read extracted text, send it to Gemini, and save structured JSON output."""
    
    if not os.path.exists(output_txt_path):
        print(f"❌ Error: File {output_txt_path} not found!")
        return None

    try:
        with open(output_txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        extracted_json_text = extract_financial_tables(text)
        
        if extracted_json_text:
            os.makedirs(output_dir, exist_ok=True)  # ✅ Ensure output directory exists

            # ✅ Extract filename without extension
            filename = os.path.basename(output_txt_path).replace(".txt", ".json")
            llm_output_path = os.path.join(output_dir, filename)

            # ✅ Directly save the JSON response as a file
            with open(llm_output_path, "w", encoding="utf-8") as f:
                f.write(extracted_json_text)

            print(f"✅ Financial data saved: {llm_output_path}")
            return llm_output_path
        else:
            print("⚠️ No financial data extracted.")
            return None

    except Exception as e:
        print(f"❌ Error while processing the file: {e}")
        return None


# Example Usage
save_extracted_data(r'C:\Users\Shubhangi Mishra\Desktop\Financial_extraction\processed_text\vodafone_annual_report_reduced.txt')

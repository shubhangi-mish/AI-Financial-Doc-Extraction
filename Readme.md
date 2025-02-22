# Financial Report Extraction and Relabeling

## Overview
This project automates the extraction and relabeling of financial tables from PDF and DOCX files. It leverages NLP and LLMs to extract structured financial data and map it to standardized vocabulary terms.

## Features
- Extracts text from PDFs and DOCX files.
- Uses an LLM to extract financial tables from raw text.
- Saves extracted tables in Markdown format.
- Relabels balance sheet items using a predefined vocabulary.

## Project Structure
```
Financial_extraction/
│── extract_text.py           # Extracts text from documents
│── extract_md_from_llm.py                  # Processes extracted text and saves Markdown
│── relabelled_md.py       # Relabels extracted balance sheet tables
│── main.py                   # Main script to run the pipeline
│── requirements.txt          # Required dependencies
│── README.md                 # Project documentation
│
├── PDF directory/            # Input PDFs and DOCX files
├── processed_text/           # Extracted raw text files
├── extracted_tables_markdown/ # Markdown files with extracted tables
├── relabelled_markdown/      # Relabeled Markdown tables
```

## Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd Financial_extraction
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with API keys:
   ```sh
   GEMINI_API_KEY=<your-api-key>
   ```

## Usage
1. Place PDF or DOCX files in the `PDF directory/`.
2. Run the main script:
   ```sh
   python main.py
   ```
3. Extracted text will be saved in `processed_text/`.
4. Extracted tables will be saved in `extracted_tables_markdown/`.
5. Relabeled tables will be saved in `relabelled_markdown/`.

## Requirements
- Python 3.8+
- `google-generativeai`
- `docx2txt`
- `PyPDF2`
- `striprtf`
- `python-dotenv`

Install all dependencies using:
```sh
pip install -r requirements.txt
```

## Contributing
Feel free to fork this repository, create a new branch, and submit a pull request with improvements.

## License
This project is licensed under the MIT License.

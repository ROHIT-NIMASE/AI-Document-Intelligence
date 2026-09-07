import os
from pypdf import PdfReader

RAW_DATA_DIR = "data/raw"


def extract_text_from_pdf(pdf_path, doc_name):
    """
    Opens a single PDF and extracts text from each page.
    Returns a list of dicts, one per page:
    {"document_name": ..., "page_number": ..., "text": ...}
    """
    reader = PdfReader(pdf_path)
    pages_data = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""  # extract_text() can return None
        cleaned = text.strip()

        if len(cleaned) < 10:  # arbitrary low threshold = "basically empty"
            print(f"[WARNING] {doc_name} - page {page_number} has little/no extractable text "
                  f"(possibly a scanned image page).")

        pages_data.append({
            "document_name": doc_name,
            "page_number": page_number,
            "text": cleaned
        })

    return pages_data


def load_all_pdfs(raw_dir=RAW_DATA_DIR):
    """
    Loops through every PDF in raw_dir and extracts text from all of them.
    Returns a single flat list of page-level dicts across all documents.
    """
    all_pages = []

    pdf_files = [f for f in os.listdir(raw_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"[WARNING] No PDF files found in {raw_dir}")
        return all_pages

    for filename in pdf_files:
        full_path = os.path.join(raw_dir, filename)
        print(f"Processing: {filename}")
        pages = extract_text_from_pdf(full_path, doc_name=filename)
        all_pages.extend(pages)

    return all_pages


if __name__ == "__main__":
    all_pages = load_all_pdfs()

    print(f"\nTotal pages extracted across all PDFs: {len(all_pages)}")
    if all_pages:
        print("\n--- Sample entry ---")
        print(all_pages[0])
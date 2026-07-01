from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
    except (PdfReadError, ValueError, FileNotFoundError):
        return ""

    text = ""

    try:
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        return ""

    return text
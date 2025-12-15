import os
from docx import Document
import PyPDF2

def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif ext == ".docx":
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    elif ext == ".pdf":
        text = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)

    else:
        raise ValueError("Unsupported file type. Use txt, pdf, docx.")

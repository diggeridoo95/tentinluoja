import fitz  # PyMuPDF
from typing import Union, IO

def extract_text_from_pdf(file: Union[str, bytes, bytearray, IO]):
    """
    Accepts a path (str), bytes/bytearray, or a file-like object.
    Returns extracted text from the PDF.
    """
    # If file is a path
    if isinstance(file, str):
        with fitz.open(file) as doc:
            return "".join(page.get_text("text") for page in doc)

    # File-like or raw bytes
    if hasattr(file, "read"):
        data = file.read()
        try:
            file.seek(0)
        except Exception:
            pass
    elif isinstance(file, (bytes, bytearray)):
        data = file
    else:
        raise TypeError("Unsupported file type for PDF parser")

    with fitz.open(stream=data, filetype="pdf") as doc:
        return "".join(page.get_text("text") for page in doc)

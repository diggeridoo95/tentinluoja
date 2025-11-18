import fitz  # PyMuPDF
from typing import Union, IO

def extract_text_from_pdf(file: Union[str, bytes, bytearray, IO]):
    """
    Hyödyntää PyMuPDF:ia PDF-tiedoston tekstin poimintaan.
    Funktio hyväksyy:
      - tiedostopolun (str)
      - bytes/bytearray-objektin
      - tiedostomaisen olion (hasattr(..., 'read'))
    Palauttaa koko PDF:n tekstin yhdistettynä merkkijonona.
    """
    # Jos annettu polku (str) avataan tiedosto suoraan
    if isinstance(file, str):
        with fitz.open(file) as doc:
            # Yhdistetään kaikkien sivujen tekstit
            return "".join(page.get_text("text") for page in doc)

    # Jos objekti on file-like (esim. Flaskin uploaded file)
    if hasattr(file, "read"):
        # Flaskin file.read() yleensä palauttaa bytes
        data = file.read()
        # Yritä palauttaa tiedoston alkuperäinen paikka (ei kriittistä)
        try:
            file.seek(0)
        except Exception:
            pass
    elif isinstance(file, (bytes, bytearray)):
        # Jos suoraan bytes tai bytearray
        data = file
    else:
        # Muu kuin tuettu tyyppi -> virhe
        raise TypeError("Unsupported file type for PDF parser")

    # Avataan byte-stream fitz:lla ja poimitaan sivukohtainen teksti
    with fitz.open(stream=data, filetype="pdf") as doc:
        return "".join(page.get_text("text") for page in doc)

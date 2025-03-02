import fitz
import requests
from io import BytesIO



def extract_text_from_pdf(pdf_path):
    doc = fitz.open(stream=pdf_path, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)
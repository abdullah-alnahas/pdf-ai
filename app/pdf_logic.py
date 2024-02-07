from io import BytesIO
from pdfminer.layout import LTTextContainer
from pdfminer.high_level import extract_pages

def read_and_extract_text(file_content):
    """Extracts text content from a PDF file."""
    elements = []
    for page_layout in extract_pages(BytesIO(file_content)):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                elements.append(element.get_text())
    elements = [p.strip() for p in elements]
    return [p for p in elements if p and len(p) > 1]

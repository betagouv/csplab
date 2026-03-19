import pytesseract
from pdf2image import convert_from_bytes


class TesseractPDFExtractor:
    async def extract_text(self, pdf_content: bytes) -> str:
        images = convert_from_bytes(pdf_content)
        text_parts = []

        for image in images:
            text = pytesseract.image_to_string(image, lang="fra")
            text_parts.append(text)

        return "\n".join(text_parts).strip()

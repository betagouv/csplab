import io
import logging

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from domain.interfaces.pdf_validator import IPDFValidator

logger = logging.getLogger(__name__)


class PyPDFValidator(IPDFValidator):
    async def validate_pdf(self, content: bytes) -> bool:
        try:
            pdf_stream = io.BytesIO(content)

            reader = PdfReader(pdf_stream)

            if len(reader.pages) == 0:
                logger.warning("PDF valide mais sans pages")
                return False

            _ = reader.pages[0]

            return True

        except PdfReadError as e:
            logger.warning(f"Fichier PDF invalide: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la validation PDF: {e}")
            return False

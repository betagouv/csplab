---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.18.1
  kernelspec:
    display_name: CSPLab Base (pandas, numpy, matplotlib)
    language: python
    name: csplab-base
---

```python
from dotenv import load_dotenv
import os
import pydantic
from openai import OpenAI
import os
import json
import pymupdf as fitz
import base64
import pypdf
import io
```

```python
load_dotenv()
```

```python
"""PDF text extractor interface for CV content extraction."""

from typing import Any, Dict, Protocol
from pydantic import BaseModel, HttpUrl


class IPDFTextExtractor(Protocol):
    """Interface for extracting structured content from PDF files."""

    def extract_text(self, pdf_content: bytes) -> Dict[str, Any]:
        """Extract structured content from PDF bytes.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Structured data as dict with format:
            {
                "experiences": [
                    {
                        "title": str,
                        "company": str,
                        "sector": str|None,
                        "description": str
                    }
                ],
                "skills": [str]
            }

        Raises:
            ValueError: If PDF content is invalid or corrupted
        """
        ...

    def validate_pdf(self, pdf_content: bytes, max_size_mb: int = 5) -> bool:
        """Validate PDF format and size.

        Args:
            pdf_content: PDF file content as bytes
            max_size_mb: Maximum allowed file size in MB (default 5MB)

        Returns:
            True if PDF is valid, False otherwise
        """
        ...

class OpenAIConfig(BaseModel):
    """Configuration for OpenAI API client."""

    api_key: str
    base_url: HttpUrl
    model: str
```

```python
PROMPT = """Analyse ce CV et extrait les informations suivantes au format JSON exact :
        {
          "experiences": [
            {
              "title": "titre du poste",
              "company": "nom de l'entreprise",
              "sector": "secteur d'activité ou null",
              "description": "description des responsabilités"
            }
          ],
          "skills": ["compétence1", "compétence2"]
        }

        Réponds uniquement avec le JSON, sans texte supplémentaire."""
```

```python
class OpenAIPDFExtractor(IPDFTextExtractor):
    """Implementation of PDF text extraction service using Open router API."""

    def __init__(self, config: OpenAIConfig):
        """Initialize with OpenAI configuration."""
        self.config = config
        self.client = OpenAI(api_key=config.api_key, base_url=str(config.base_url))

    def extract_text(self, pdf_content: bytes) -> Dict[str, Any]:
        """Extract structured content from PDF bytes.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Structured data as dict with format:
            {
                "experiences": [
                    {
                        "title": str,
                        "company": str,
                        "sector": str|None,
                        "description": str
                    }
                ],
                "skills": [str]
            }

        Raises:
            ValueError: If PDF content is invalid or corrupted
        """
        try:
            # Convert PDF to images using PyMuPDF
            pdf_doc = fitz.open(stream=pdf_content, filetype="pdf")
            images = []

            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                # Convert page to image (PNG)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
                img_data = pix.tobytes("png")
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                images.append(img_base64)

            pdf_doc.close()

            # Prepare messages for OpenAI API
            content = [
                {
                    "type": "text",
                    "text": PROMPT
                }
            ]

            # Add all images to the content
            for img_base64 in images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}"
                    }
                })

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=2000,
                temperature=0.1
            )

            # Parse JSON response
            response_text = response.choices[0].message.content.strip()

            # Remove potential markdown code blocks
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()

            result = json.loads(response_text)

            # Validate structure
            if not isinstance(result, dict) or 'experiences' not in result or 'skills' not in result:
                raise ValueError("Invalid response structure from API")

            return result

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            raise ValueError(f"Error processing PDF: {e}")

    def validate_pdf(self, pdf_content: bytes, max_size_mb: int = 5) -> bool:
        """Validate PDF format and size.

        Args:
            pdf_content: PDF file content as bytes
            max_size_mb: Maximum allowed file size in MB (default 5MB)

        Returns:
            True if PDF is valid, False otherwise
        """
        if not pdf_content:
            return False

        # Check file size
        size_mb = len(pdf_content) / (1024 * 1024)
        if size_mb > max_size_mb:
            return False

        # Validate PDF structure using pypdf
        try:
            pypdf.PdfReader(io.BytesIO(pdf_content))
            return True
        except pypdf.errors.PyPdfError:
            return False
```

```python
with open("data/CV_Elodie_Royant_developpeuse_Fullstack_Data_scientist.pdf", "rb") as f:
    pdf_content = f.read()
```

```python
config = OpenAIConfig(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url=HttpUrl(os.environ.get("OPENROUTER_BASE_URL")),
    model=os.environ.get("OPENROUTER_OCR_MODEL")
)
pdf_extractor = OpenAIPDFExtractor(config)
```

```python
pdf_extractor.validate_pdf(pdf_content)
```

```python
pdf_extractor.extract_text(pdf_content)
```

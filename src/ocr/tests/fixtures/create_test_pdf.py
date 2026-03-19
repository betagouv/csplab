#!/usr/bin/env python3
import os


def create_test_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "test_sample.pdf")

    # Contenu PDF minimal mais valide
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 5 0 R
>>
>>
>>
endobj

4 0 obj
<<
/Length 85
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF for OCR) Tj
0 -20 Td
(Hello World!) Tj
ET
endstream
endobj

5 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj

xref
0 6
0000000000 65535 f
0000000010 00000 n
0000000053 00000 n
0000000100 00000 n
0000000244 00000 n
0000000380 00000 n
trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
459
%%EOF"""

    # Écrire le PDF
    with open(pdf_path, "wb") as f:
        f.write(pdf_content)

    return pdf_path


if __name__ == "__main__":
    create_test_pdf()

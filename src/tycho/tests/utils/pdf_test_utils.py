"""PDF utilities for testing."""

import pymupdf


def create_minimal_valid_pdf() -> bytes:
    """Create a minimal valid PDF for testing.

    Returns:
        bytes: A valid PDF document as bytes
    """
    doc = pymupdf.open()
    page = doc.new_page()

    page.insert_text((50, 50), "Test CV Content", fontsize=12)
    page.insert_text((50, 80), "Software Engineer", fontsize=10)
    page.insert_text((50, 100), "Tech Company", fontsize=10)
    page.insert_text((50, 120), "Python, Django, PostgreSQL", fontsize=10)

    pdf_bytes = doc.tobytes()
    doc.close()

    return pdf_bytes


def create_large_pdf(size_mb: int = 6) -> bytes:
    """Create a large PDF for testing size limits.

    Args:
        size_mb: Target size in MB

    Returns:
        bytes: A large PDF document as bytes
    """
    doc = pymupdf.open()

    target_size = size_mb * 1024 * 1024
    current_size = 0
    page_count = 0

    max_pages = 100  # Safety limit
    while current_size < target_size and page_count < max_pages:
        page = doc.new_page()
        for i in range(50):
            page.insert_text(
                (50, 50 + i * 15),
                f"This is line {i} of page {page_count} with content. " * 5,
                fontsize=8,
            )
        page_count += 1

        current_bytes = doc.tobytes()
        current_size = len(current_bytes)

    pdf_bytes = doc.tobytes()
    doc.close()

    return pdf_bytes

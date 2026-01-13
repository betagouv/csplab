"""Forms for CV upload flow."""

import io
from typing import TYPE_CHECKING

import pypdf
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from django.core.files.uploadedfile import UploadedFile

CV_MAX_SIZE_MB = settings.CV_MAX_SIZE_MB
CV_MAX_SIZE_BYTES = CV_MAX_SIZE_MB * 1024 * 1024
CV_ALLOWED_CONTENT_TYPES = ["application/pdf"]
CV_ALLOWED_EXTENSIONS = [".pdf"]


class CVUploadForm(forms.Form):
    """Form for CV upload."""

    cv_file = forms.FileField(
        label="Votre CV",
        required=True,
        help_text="Taille maximale : 5 Mo. Formats supportés : PDF.",
        widget=forms.FileInput(
            attrs={
                "accept": ".pdf,application/pdf",
                "id": "file-input",
                "class": "fr-upload",
            }
        ),
    )

    def clean_cv_file(self) -> "UploadedFile":
        """Validate the uploaded CV file."""
        cv_file = self.cleaned_data.get("cv_file")

        if not cv_file:
            raise ValidationError("Veuillez sélectionner un fichier.")

        if cv_file.size > CV_MAX_SIZE_BYTES:
            raise ValidationError(
                "Le fichier dépasse la taille maximale de %(max_size)s Mo.",
                code="file_too_large",
                params={"max_size": CV_MAX_SIZE_MB},
            )

        content_type = cv_file.content_type
        if content_type not in CV_ALLOWED_CONTENT_TYPES:
            raise ValidationError(
                "Format non supporté. Seul le format PDF est accepté.",
                code="invalid_content_type",
            )

        file_name = cv_file.name.lower()
        if not any(file_name.endswith(ext) for ext in CV_ALLOWED_EXTENSIONS):
            raise ValidationError(
                "Extension non supportée. Seul le format PDF est accepté.",
                code="invalid_extension",
            )

        cv_file.seek(0)
        try:
            pypdf.PdfReader(io.BytesIO(cv_file.read()))
        except Exception:
            raise ValidationError(
                "Le fichier n'est pas un PDF valide.",
                code="invalid_pdf_signature",
            ) from None
        finally:
            cv_file.seek(0)

        return cv_file

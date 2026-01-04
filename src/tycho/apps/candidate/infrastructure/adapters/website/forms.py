"""Forms for candidate website."""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

CV_MAX_SIZE_MB = 5
CV_MAX_SIZE_BYTES = CV_MAX_SIZE_MB * 1024 * 1024
CV_ALLOWED_CONTENT_TYPES = ["application/pdf"]
CV_ALLOWED_EXTENSIONS = [".pdf"]
PDF_MAGIC_BYTES = b"%PDF-"


class CVUploadForm(forms.Form):
    """Form for CV upload."""

    cv_file = forms.FileField(
        label=_("Votre CV"),
        required=True,
        help_text=_("Format PDF uniquement, taille maximale 5 Mo"),
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".pdf,application/pdf",
                "class": "csplab-dropzone__input",
                "id": "file-input",
                "aria-label": "Sélectionner un fichier CV",
            }
        ),
    )

    def clean_cv_file(self):
        """Validate the uploaded CV file."""
        cv_file = self.cleaned_data.get("cv_file")

        if not cv_file:
            raise ValidationError(_("Veuillez sélectionner un fichier."))

        if cv_file.size > CV_MAX_SIZE_BYTES:
            raise ValidationError(
                _("Le fichier dépasse la taille maximale de %(max_size)s Mo."),
                code="file_too_large",
                params={"max_size": CV_MAX_SIZE_MB},
            )

        content_type = cv_file.content_type
        if content_type not in CV_ALLOWED_CONTENT_TYPES:
            raise ValidationError(
                _("Format non supporté. Seul le format PDF est accepté."),
                code="invalid_content_type",
            )

        file_name = cv_file.name.lower()
        if not any(file_name.endswith(ext) for ext in CV_ALLOWED_EXTENSIONS):
            raise ValidationError(
                _("Extension non supportée. Seul le format PDF est accepté."),
                code="invalid_extension",
            )

        cv_file.seek(0)
        file_header = cv_file.read(5)
        cv_file.seek(0)

        if file_header != PDF_MAGIC_BYTES:
            raise ValidationError(
                _("Le fichier n'est pas un PDF valide."),
                code="invalid_pdf_signature",
            )

        return cv_file


class CorpsSearchForm(forms.Form):
    """Form for searching Corps entities."""

    query = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "fr-input",
                "placeholder": _("Rechercher"),
                "id": "search-input",
                "type": "search",
                "aria-describedby": "search-input-messages",
            }
        ),
        label=_("Recherche"),
        help_text=_("Décrivez le type de poste ou de corps que vous recherchez"),
    )

    limit = forms.IntegerField(
        initial=10,
        min_value=1,
        max_value=50,
        required=False,
        widget=forms.HiddenInput(),
    )

    def clean_query(self):
        """Clean and validate query field."""
        query = self.cleaned_data.get("query", "").strip()
        if not query:
            raise forms.ValidationError(_("La recherche ne peut pas être vide."))
        MIN_QUERY_LENGTH = 3
        if len(query) < MIN_QUERY_LENGTH:
            raise forms.ValidationError(
                _("La recherche doit contenir au moins 3 caractères.")
            )
        return query

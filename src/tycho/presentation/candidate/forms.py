"""Forms for candidate website."""

from django import forms


class CorpsSearchForm(forms.Form):
    """Form for searching Corps entities."""

    query = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "fr-input",
                "placeholder": "Rechercher",
                "id": "search-input",
                "type": "search",
                "aria-describedby": "search-input-messages",
            }
        ),
        label="Recherche",
        help_text="Décrivez le type de poste ou de corps que vous recherchez",
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
            raise forms.ValidationError("La recherche ne peut pas être vide.")
        MIN_QUERY_LENGTH = 3
        if len(query) < MIN_QUERY_LENGTH:
            raise forms.ValidationError(
                "La recherche doit contenir au moins 3 caractères."
            )
        return query

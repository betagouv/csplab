from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SuperuserAuthenticationForm(AuthenticationForm):
    """Password login form reserved to superusers"""

    def confirm_login_allowed(self, user) -> None:
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            raise forms.ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )


class OtpTokenForm(forms.Form):
    otp_token = forms.RegexField(
        regex=r"^\d{6}$",
        label="Code à 6 chiffres",
        error_messages={"invalid": "Saisissez le code à 6 chiffres."},
        widget=forms.TextInput(
            attrs={
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "class": "fr-input",
            }
        ),
    )

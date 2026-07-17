import logging
from getpass import getpass
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.db import transaction
from referentiel.value_objects.source_type import SourceType

from config.logger_names import LoggerName
from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.users.models import UserModel


class Command(BaseCommand):
    help = "Crée un utilisateur et une source, puis rattache la source à l'utilisateur."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(LoggerName.IDENTITE.value)

    def handle(self, *args, **options):
        first_name = self._prompt("Prénom")
        last_name = self._prompt("Nom")
        email = self._prompt_email()
        password = self._prompt_password()
        source = self._prompt_source()

        with transaction.atomic():
            user = UserModel.objects.create_user(
                username=str(uuid4()),
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            source.full_clean()
            source.save()
            user.sources.add(source)

        self.logger.info(
            "✅ Utilisateur '%s' créé et rattaché à la source '%s' (source_id: %s).",
            user.email,
            source.slug,
            source.source_id,
        )

    def _prompt(self, label: str) -> str:
        value = ""
        while not value.strip():
            value = input(f"{label}: ")
        return value.strip()

    def _prompt_email(self) -> str:
        while True:
            email = self._prompt("Email")
            try:
                validate_email(email)
            except ValidationError:
                self.logger.warning("Email invalide, réessayez.")
                continue
            if UserModel.objects.filter(email=email).exists():
                self.logger.warning("Un utilisateur avec cet email existe déjà.")
                continue
            return email

    def _prompt_password(self) -> str:
        while True:
            password = getpass("Mot de passe: ")
            if not password:
                self.logger.warning("Le mot de passe ne peut pas être vide.")
                continue
            confirmation = getpass("Confirmez le mot de passe: ")
            if password != confirmation:
                self.logger.warning("Les mots de passe ne correspondent pas.")
                continue
            return password

    def _prompt_source(self) -> SourceModel:
        slug = self._prompt("Slug de la source")
        return SourceModel(slug=slug, type=SourceType.API.value)

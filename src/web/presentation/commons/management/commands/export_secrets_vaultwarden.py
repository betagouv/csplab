import os

from django.core.management.base import BaseCommand, CommandError

from application.commons.services.export_secrets_vaultwarden import (
    MissingSecretsError,
    NoteDiff,
    UnexportableEnvError,
    prepare_secrets_export,
    save_secrets_export,
)


class Command(BaseCommand):
    help = (
        "Affiche les notes Vaultwarden /{service}/{env} à mettre à jour avec les "
        "secrets Scaleway de démo ou de prod, puis enregistre l'état après "
        "confirmation."
    )

    def handle(self, *args, **options):
        try:
            export = prepare_secrets_export(os.environ.get("SCALEWAY_ENV", ""))
        except (UnexportableEnvError, MissingSecretsError) as error:
            raise CommandError(error.message) from error

        if export.last_exported_at:
            self.stdout.write(
                "Dernière mise à jour des notes : "
                f"{export.last_exported_at:%d/%m/%Y %H:%M} UTC"
            )
        else:
            self.stdout.write(
                "Aucun état enregistré : toutes les notes sont à mettre à jour."
            )
        for note in export.notes:
            self._write_note(note)

        if not export.needs_update:
            self.stdout.write("")
            self.stdout.write("Rien à recopier, état inchangé.")
            return
        if not self._confirm():
            self.stdout.write("État non enregistré, rien n'a changé.")
            return
        save_secrets_export(export)
        self.stdout.write(self.style.SUCCESS("État enregistré."))

    def _write_note(self, note: NoteDiff) -> None:
        self.stdout.write("")
        if note.is_up_to_date:
            self.stdout.write(f"{note.name} : à jour")
            return
        self.stdout.write(self.style.WARNING(f"{note.name} : à mettre à jour"))
        for label, names in (
            ("Ajoutées", note.added),
            ("Supprimées", note.removed),
            ("Modifiées", note.changed),
        ):
            if names:
                self.stdout.write(f"  {label} : {', '.join(names)}")
        self.stdout.write("--- contenu de la note ---")
        self.stdout.write(note.content)
        self.stdout.write("--- fin de la note ---")

    def _confirm(self) -> bool:
        self.stdout.write("")
        try:
            answer = input(
                "Toutes les notes à mettre à jour ont été recopiées dans "
                "Vaultwarden ? [o/N] "
            )
        except EOFError:
            return False
        return answer.strip().lower() == "o"

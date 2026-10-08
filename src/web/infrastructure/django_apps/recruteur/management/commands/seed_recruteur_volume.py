import logging

from django.core.management.base import BaseCommand, CommandError

from config.logger_names import LoggerName
from infrastructure.factories.seed_recruteur_volume import seed_recruteur_volume


class Command(BaseCommand):
    help = "Add several hundred candidatures to the recruteur seed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(LoggerName.RECRUTEUR.value)

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Supprime les candidatures en volume et les recrée.",
        )

    def handle(self, *args, **options):
        context = seed_recruteur_volume(force=options["force"])
        if context["status"] == "base_missing":
            raise CommandError(
                "Recrutements du seed absents : lancer seed_recruteur_datas d'abord."
            )
        if context["status"] == "etape_missing":
            raise CommandError(
                f"Étape « {context['etape']} » absente du recrutement "
                f"{context['reference']} : relancer seed_recruteur_datas --force."
            )
        if context["status"] == "already_seeded":
            self.logger.warning("⚠️  Volume already seeded, skipping.")
        else:
            self.logger.info(
                "✅ Seed volume terminé : %s candidatures.",
                context["nb_candidatures"],
            )

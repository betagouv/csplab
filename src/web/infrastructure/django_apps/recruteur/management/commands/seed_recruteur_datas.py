import logging

from django.core.management.base import BaseCommand

from tests.utils.seed_recruteur_datas import seed_recruteur_datas


class Command(BaseCommand):
    help = "Seed all necessary data for recruteur review apps"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help=("Supprime les données existantes et reseed depuis zéro. "),
        )

    def handle(self, *args, **options):
        force = options["force"]
        suffix = " (--force activé)" if force else ""
        self.logger.info("Seeding recruteur data...%s", suffix)
        context = seed_recruteur_datas(force=force)
        if context.get("status") == "already_seeded":
            self.logger.warning("⚠️  Data already seeded, skipping.")
        else:
            self.logger.info(
                "✅ Seed terminé : %s offres actives, %s archivées, "
                "%s candidats, %s agents.",
                context["nb_offres_actives"],
                context["nb_offres_archivees"],
                context["nb_candidats"],
                context["nb_agents"],
            )

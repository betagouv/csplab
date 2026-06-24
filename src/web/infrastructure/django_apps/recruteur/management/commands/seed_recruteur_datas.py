from django.core.management.base import BaseCommand

from tests.utils.seed_recruteur_datas import seed_recruteur_datas


class Command(BaseCommand):
    help = "Seed all necessary data for recruteur review apps"

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
        self.stdout.write(f"Seeding recruteur data...{suffix}")
        context = seed_recruteur_datas(force=force)
        if context.get("status") == "already_seeded":
            self.stdout.write(self.style.WARNING("⚠️  Data already seeded, skipping."))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Seed terminé : "
                    f"{context['nb_offres_actives']} offres actives, "
                    f"{context['nb_offres_archivees']} archivées, "
                    f"{context['nb_candidats']} candidats, "
                    f"{context['nb_agents']} agents."
                )
            )

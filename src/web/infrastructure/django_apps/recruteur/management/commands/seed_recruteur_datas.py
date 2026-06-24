from django.core.management.base import BaseCommand

from tests.utils.seed_recruteur_datas import seed_recruteur_datas


class Command(BaseCommand):
    help = "Seed all necessary data for recruteur review apps"

    def handle(self, *args, **options):
        self.stdout.write("Seeding recruteur data...")
        context = seed_recruteur_datas()
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

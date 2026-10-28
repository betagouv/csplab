from django.core.management.base import BaseCommand

from application.recruteur.services.reply_as_demo_candidates import (
    reply_as_demo_candidates,
)


class Command(BaseCommand):
    help = "Répond au nom des candidats fictifs aux messages d'agents en attente"

    def handle(self, *args, **options):
        replies = reply_as_demo_candidates()
        self.stdout.write(f"{replies} réponse(s) envoyée(s).")

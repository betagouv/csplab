# infrastructure/django_apps/shared/management/commands/seed_migration_history.py
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed users migration history to unblock InconsistentMigrationHistory"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM django_migrations WHERE app = %s", ["users"]
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied)"
                    " VALUES (%s, %s, NOW())",
                    ["users", "0001_initial"],
                )
                self.stdout.write(self.style.SUCCESS("Seeded users migration history"))
            else:
                self.stdout.write("users migrations already present, skipping")

from uuid import UUID

from django.core.management.base import BaseCommand, CommandError

from infrastructure.factories.seed_demo_organisme import seed_demo_organisme

_ERREURS = {
    "production": "Seed de démo refusé en production (SCALEWAY_ENV=prod).",
    "organisme_absent": "Organisme {organisme} introuvable ou supprimé.",
    "aucun_agent_actif": (
        "L'organisme {organisme} n'a aucun agent actif : rattacher au moins un "
        "agent avant de lancer le seed."
    ),
    "deja_seede_ailleurs": (
        "Les données de démo existent déjà sur un autre organisme "
        "({autre_organisme_id}) : rien n'a été modifié."
    ),
}


class Command(BaseCommand):
    help = "Crée un jeu de données de démo sur un organisme existant"

    def add_arguments(self, parser):
        parser.add_argument(
            "--organisme",
            type=UUID,
            required=True,
            help="UUID de l'organisme qui reçoit les données de démo.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Supprime les données de démo existantes et les recrée.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Affiche ce qui serait créé et supprimé, sans rien écrire.",
        )

    def handle(self, *args, **options):
        context = seed_demo_organisme(
            options["organisme"], force=options["force"], dry_run=options["dry_run"]
        )
        status = context["status"]
        if status in _ERREURS:
            raise CommandError(
                _ERREURS[status].format(organisme=options["organisme"], **context)
            )
        if status == "already_seeded":
            self.stdout.write(
                self.style.WARNING(
                    "Données de démo déjà présentes, rien n'a été modifié "
                    "(--force pour les recréer)."
                )
            )
            return
        if status == "dry_run":
            self.stdout.write("Simulation (--dry-run) : aucune écriture.")
            a_supprimer = context["a_supprimer"]
            self.stdout.write(
                f"À supprimer avec --force : {a_supprimer['offres']} offres, "
                f"{a_supprimer['candidatures']} candidatures, "
                f"{a_supprimer['candidats']} candidats."
            )
        self._ecrire_comptes(context["comptes"])

    def _ecrire_comptes(self, comptes):
        self.stdout.write(
            f"Offres : {comptes['offres']} ({comptes['recrutements_en_cours']} en "
            f"cours, {comptes['recrutements_archives']} archivées)."
        )
        self.stdout.write(f"Candidatures : {comptes['candidatures']}.")
        for etape, nombre in comptes["par_etape"].items():
            self.stdout.write(f"  {etape} : {nombre}")
        self.stdout.write(
            f"Notes : {comptes['notes']}, conversations : "
            f"{comptes['conversations']} (dont {comptes['conversations_lues']} lues)."
        )
